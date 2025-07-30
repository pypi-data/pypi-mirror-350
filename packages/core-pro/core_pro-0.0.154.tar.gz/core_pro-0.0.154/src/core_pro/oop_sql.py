from pathlib import Path
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor
import trino
import os
from datetime import datetime
from tqdm.auto import tqdm
from typing import Union, Optional


class DataPipeLine:
    def __init__(
        self,
        query: str | Path,
        username: str = None,
        password: str = None,
        host: str = None,
    ):
        self.query = self._process_query(query)
        self.prefix = "🤖 TRINO"
        self.username = username or os.environ.get("PRESTO_USER")
        self.password = password or os.environ.get("PRESTO_PASSWORD")
        self.host = host or os.environ.get("PRESTO_HOST")

    def debug_query(self):
        print(self.query)

    def _process_query(self, query: Union[str, Path]) -> str:
        if isinstance(query, Path):
            with open(str(query), "r") as f:
                query = f.read()
        return query

    def _time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _records_to_df(self, records, columns: list, save_path: Optional[Path] = None):
        try:
            df = pl.DataFrame(records, orient="row", schema=columns)
            # Convert decimal columns
            col_decimal = [i for i, v in dict(df.schema).items() if v == pl.Decimal]
            if col_decimal:
                df = df.with_columns(pl.col(i).cast(pl.Float64) for i in col_decimal)
        except (pl.exceptions.ComputeError, TypeError) as e:
            print(f"Errors on Polars, switch to Pandas: {e}")
            df = pd.DataFrame(records, columns=columns)

        # Save to file if path provided
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(df, pl.DataFrame):
                df.write_parquet(save_path)
            else:
                df.to_parquet(save_path, index=False, compression="zstd")
            print(f"{self._time()} {self.prefix}: File saved {save_path}")

        return f"Data shape ({df.shape[0]:,.0f}, {df.shape[1]})", df

    def _connection(self):
        return trino.dbapi.connect(
            host=self.host,
            port=443,
            user=self.username,
            catalog="hive",
            http_scheme="https",
            source=f"(50)-(vnbi-dev)-({self.username})-(jdbc)-({self.username})-(SG)",
            auth=trino.auth.BasicAuthentication(self.username, self.password),
        )

    def run_presto_to_df(
        self,
        save_path: Path = None,
        verbose: bool = True,
        overwrite: bool = False,
    ) -> pl.DataFrame | pd.DataFrame:
        # Check if file exists
        if not overwrite and save_path and save_path.exists():
            print(f"{self._time()} {self.prefix}: {save_path} already exists")
            return pl.DataFrame()

        conn = self._connection()
        cur = conn.cursor()
        memory = 0

        if verbose:
            thread = ThreadPoolExecutor(1)
            async_result = thread.submit(cur.execute, self.query)
            pbar = tqdm(total=100, unit="%", desc=f"{self.prefix} Starting")
            last_progress = 0
            while not async_result.done():
                try:
                    stats = cur.stats
                    memory = stats.get("peakMemoryBytes", 0) * 1e-9
                    state = stats.get("state", "Not Ready")
                    completed = stats.get("completedSplits", 0)
                    total = stats.get("totalSplits", 1)
                    progress = (
                        min(99, int((completed / total) * 100)) if total > 0 else 0
                    )
                    if progress > last_progress:
                        pbar.update(progress - last_progress)
                        last_progress = progress
                    pbar.set_description(
                        f"{self.prefix} {state} - Memory {memory:.1f}GB"
                    )
                except Exception:
                    pass
            pbar.update(100 - last_progress)
            pbar.close()
        else:
            try:
                cur.execute(self.query)
                memory = cur.stats.get("peakMemoryBytes", 0) * 1e-9
            except Exception as e:
                print(f"{self._time()} {self.prefix}: Error executing: {e}")
                return pl.DataFrame()

        print(f"{self._time()} {self.prefix}: Fetching Memory {memory:.1f}GB")
        try:
            records = cur.fetchall()
            columns = [col[0] for col in cur.description]
            text, df = self._records_to_df(records, columns, save_path)
            print(f"{self._time()} {self.prefix}: {text}")
            return df
        except Exception as e:
            print(f"{self._time()} {self.prefix}: {e}")
            return pl.DataFrame()


# query = """
# select item_id
# from mp_order.dwd_order_item_all_ent_df__vn_s0_live
# limit 10
# """
# DataPipeLine(query).run_presto_to_df()

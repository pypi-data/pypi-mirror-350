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
    def __init__(self, query: Union[str, Path]):
        self.query = self._process_query(query)
        self.prefix = '🤖 TRINO'

    def debug_query(self):
        print(self.query)

    def _process_query(self, query: Union[str, Path]) -> str:
        if isinstance(query, Path):
            with open(str(query), 'r') as f:
                query = f.read()
        return query

    def _time(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def _records_to_df(self, records, columns: list, save_path: Optional[Path] = None):
        # Convert records to DataFrame
        try:
            df = pl.DataFrame(records, orient='row', schema=columns)
            # Convert decimal columns
            col_decimal = [i for i, v in dict(df.schema).items() if v == pl.Decimal]
            if col_decimal:
                df = df.with_columns(pl.col(i).cast(pl.Float64) for i in col_decimal)
        except (pl.exceptions.ComputeError, TypeError) as e:
            print(f'Errors on Polars, switch to Pandas: {e}')
            df = pd.DataFrame(records, columns=columns)

        # Save to file if path provided
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(df, pl.DataFrame):
                df.write_parquet(save_path)
            else:
                df.to_parquet(save_path, index=False, compression='zstd')
            print(f"{self._time()} {self.prefix}: File saved {save_path}")

        return f"Data shape ({df.shape[0]:,.0f}, {df.shape[1]})", df

    def _connection(self):
        username, password, host = (
            os.environ["PRESTO_USER"],
            os.environ["PRESTO_PASSWORD"],
            os.environ["PRESTO_HOST"],
        )
        conn = trino.dbapi.connect(
            host=host,
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        return conn

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

        # Connect to database
        conn = self._connection()
        cur = conn.cursor()

        # Use tqdm for single query execution, not in batch
        memory = 0
        if verbose:
            thread = ThreadPoolExecutor(1)
            async_result = thread.submit(cur.execute, self.query)

            pbar = tqdm(total=100, unit="%")
            last_progress = 0

            while not async_result.done():
                try:
                    memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                    state = cur.stats.get('state', 'Not Ready')

                    # Calculate progress percentage
                    progress = 0
                    if state == "RUNNING":
                        completed = cur.stats.get('completedSplits', 0)
                        total = cur.stats.get('totalSplits', 1)  # Avoid division by zero
                        progress = min(99, int((completed / total) * 100)) if total > 0 else 0

                    # Update progress bar
                    if progress > last_progress:
                        pbar.update(progress - last_progress)
                        last_progress = progress

                    pbar.set_description(f"{self.prefix} {state} - Memory {memory:.1f}GB")
                except Exception as e:
                    tqdm.write(f"Error updating progress: {e}")

            pbar.update(100 - last_progress)
            pbar.close()
        else:
            try:
                cur.execute(self.query)
                memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
            except Exception as e:
                print(f"{self._time()} {self.prefix}: Error executing: {e}")
                return pl.DataFrame()

        print(f"{self._time()} {self.prefix}: Fetching Memory {memory:.1f}GB")
        try:
            records = cur.fetchall()
            columns = [i[0] for i in cur.description]
            text, df = self._records_to_df(records, columns, save_path)

            print(f"{self._time()} {self.prefix}: {text}")
            return df
        except Exception as e:
            print(f"{self._time()} {self.prefix}: {e}")
            return pl.DataFrame()

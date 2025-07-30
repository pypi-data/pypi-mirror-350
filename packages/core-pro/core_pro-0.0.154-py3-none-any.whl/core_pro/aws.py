import boto3
import os
from pathlib import Path
from tqdm import tqdm
import polars as pl
from rich import print
from concurrent.futures import ThreadPoolExecutor, as_completed


def polars_to_flink_type(pl_dtype):
    mapping = {
        pl.Int8: "tinyint",
        pl.Int16: "smallint",
        pl.Int32: "integer",
        pl.Int64: "bigint",
        pl.Float32: "float",
        pl.Float64: "double",
        pl.Decimal: "decimal",
        pl.Utf8: "string",
        pl.Binary: "varbinary",
        pl.Date: "date",
        pl.Time: "time",
        pl.Datetime: "timestamp",
        pl.Boolean: "boolean",
        pl.List: "array",
        pl.Struct: "struct",
    }
    return mapping.get(pl_dtype, "string")


class AWS:
    def __init__(self, bucket_name: str, verbose: bool = True):
        dict_ = {
            "endpoint_url": os.environ["AWS_ENDPOINT_URL"],
            "aws_access_key_id": os.environ["PRESTO_USER"],
            "aws_secret_access_key": os.environ["PRESTO_PASSWORD"],
        }
        self.bucket_name = bucket_name
        self.client = boto3.client("s3", **dict_)
        self.my_bucket = boto3.resource("s3", **dict_).Bucket(self.bucket_name)
        self.status = f"[green3]🐸 [AWS]:[/]"
        self.verbose = verbose

    def get_all_files(self, prefix: str = None) -> list:
        config = {"Bucket": self.bucket_name, **({"Prefix": prefix} if prefix else {})}
        paginator = self.client.get_paginator("list_objects_v2")
        return [
            obj["Key"]
            for page in paginator.paginate(**config)
            if "Contents" in page
            for obj in page["Contents"]
        ]

    def delete_file(self, keys: list):
        chunk_size = 1000
        for i in tqdm(range(0, len(keys), chunk_size), desc=f"{self.status} Remove Chunk Size"):
            chunk = keys[i : i + chunk_size]
            objects = [{"Key": key} for key in chunk]
            self.client.delete_objects(
                Bucket=self.bucket_name, Delete={"Objects": objects}
            )

    def empty_trash(self):
        lst_trash = [i for i in self.my_bucket.objects.all() if ".Trash" in i.key]
        self.delete_file(lst_trash)
        if self.verbose:
            print(f"{self.status} [Empty Trash]: {len(lst_trash)} files")

    def get_file_size(self, key: str):
        return self.my_bucket.Object(key).content_length

    def upload_single_file(self, file: Path, prefix: str = None):
        key = f"{prefix}/{file.name}" if prefix else file.name
        response = self.my_bucket.upload_file(
            str(file), Key=key, ExtraArgs={"ContentType": "application/octet-stream"}
        )
        return response

    def upload_multiple_files(
        self, file_list: list, prefix: str = None, max_workers: int = 4
    ):
        results = []
        print(f"{self.status} Uploading {len(file_list)} files to S3")
        master_progress = tqdm(total=len(file_list), unit="files")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.upload_single_file, file_path, prefix): file_path
                for file_path in file_list
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                response = future.result()
                results.append(
                    {
                        "file": str(file_path),
                        "response": response,
                    }
                )
                master_progress.update(1)

        master_progress.close()
        return results

    def download_file(self, path: Path, key: str):
        file_size = self.get_file_size(key)
        print(f"{self.status} Download {key}, size: {file_size / 1024**2:,.2f}MB")
        with tqdm(total=file_size, unit="B", unit_scale=True) as pbar:
            self.my_bucket.download_file(
                Key=key,
                Filename=path / key.split("/")[-1],
                Callback=lambda x: pbar.update(x),
            )

    def create_presigned_url(self, key: str, expiration: int = 900):
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expiration,
        )
        print(f"{self.status} [Pre-signed] {key} in {expiration / 3600}h")
        return url

    def convert_dataframe_flink_config(
        self,
        df: pl.DataFrame,
        key: str,
        table_name: str,
        file_type: str = "parquet",
    ):
        schema, table = table_name.split(".")
        polars_schema = dict(df.schema)

        # convert to flink config
        flink_schema = {
            field: polars_to_flink_type(dtype) for field, dtype in polars_schema.items()
        }
        lines = []
        for i, (k, v) in enumerate(flink_schema.items()):
            if i == 0:
                lines.append(f"{k}:{v}")
            else:
                lines.append(f", {k}: {v}")
        flink_schema = "{\n" + "\n".join(lines) + "\n}"

        # convert to sql script
        sql_schema = [
            f"{field} {polars_to_flink_type(dtype)}"
            for field, dtype in polars_schema.items()
        ]
        sql_schema = "\n\t, ".join(sql_schema)

        flink_config = f"""
env {{
    write_mode = "${{WRITE_MODE:-append}}"
}}      

source {{
    S3FileSource {{
        datasource_name = "my_s3"
        path = "s3a://{self.bucket_name}/{key}"
        format = "{file_type}"
        schema = {flink_schema}
        bucket = "{self.bucket_name}"
        # ignore-parse-errors = "true"
        # skip-first-data-row = "true"
        result_table_name = "s3FileSource"
        access_key = "${{HADOOP_USER_NAME}}"
        secret_key = "${{HADOOP_USER_RPCPASSWORD}}"
        endpoint = "{os.environ["AWS_ENDPOINT_URL"]}"
        fs.s3a.change.detection.version.required = "false"
      }}
}}

transform {{
  Sql {{
    sql = "select * from `s3FileSource`"
    result_table_name = "transformed"
  }}
}}
  
sink {{
  HiveSink {{
    source_table_name = "transformed"
    result_table_name = "hive.{table_name}"
    partition_by = ["grass_date"]
    partition_dir_expression = "grass_date=${{grass_date}}"
    save_mode = "${{write_mode}}"
  }}
}}
        """

        sql_create_table = f"""
drop table if exists {table_name}
;

create table if not exists table_name (
    {sql_schema}
)
partitioned by
    (`grass_date`) stored as PARQUET location 'ofs://oc/s3v/sg-vnbi-ops-hive/{schema}/{table}'
;        

        """
        return flink_config, sql_create_table

from src.core_pro import AWS
from pathlib import Path
import polars as pl


# config
bucket_name = 'sg-vnbi-ops-hive'
s3 = AWS(bucket_name)

# path = Path.home() / 'Downloads/Data/cx/buyer_listening/inference/2025/kompa'
# file_local = sorted([*path.glob("*.xlsx")])
# for f in file_local[:2]:
#     df = pl.read_excel(f, engine="openpyxl")
#     df.write_parquet(f.parent / f"{f.stem}.parquet")
#
# file_parquet = sorted([*path.glob("*.parquet")])
# prefix = "cx/buyer_listening/kompa"
# s3.upload_multiple_files(file_parquet, prefix)

# check file
prefix = "dev_vnbi_ops/ds_cx__item_marketplace_listening__s3"
files = s3.get_all_files(prefix=".Trash")
files = [i for i in files if "parquet" in i]
print(files)

s3.delete_file(files)
# delete
# for f in files:
#     s3.delete_file(f)

# upload
# path = Path("/media/kevin/data_4t/cx/product_review/deploy/inference/2025-03-05/export_s3")
# files = [*path.glob("*.parquet")]
# print(len(files))
#
# for f in files:
#     s3.upload_file(f, prefix)

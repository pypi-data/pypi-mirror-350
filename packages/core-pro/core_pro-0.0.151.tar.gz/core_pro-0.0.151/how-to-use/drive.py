from src.core_pro import Drive
import polars as pl

drive_id = "1HcmcQB62qb42pmJvTkkq2o-NTPl4QCkF"
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pl.DataFrame(data)
Drive().upload_file(folder_id=drive_id, data=df, name_on_drive="test.parquet")

folder_id = Drive().create_new_folder("test", parent_id=drive_id)
Drive().share_file(file_id=folder_id, email="xuankhang.do@shopee.com")

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathlib import Path
from io import BytesIO
from typing import List, Tuple, Optional
from functools import partial
from rich import print
from tqdm.auto import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential
from PIL import Image, ImageFile
import httpx
from time import time
import certifi

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_callback=lambda retry_state: None,
)
def download_image(url: str, timeout: float = 30.0):
    """Download an image with retry logic"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        with httpx.Client(verify=certifi.where(), headers=headers, follow_redirects=True, timeout=timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.content
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return None


def process_image(
        data: dict,
        output_dir: Path,
        resize_size: Optional[Tuple[int, int]] = None,
        images_per_folder: int = 1000,
) -> bool:
    """Download and process a single image."""
    idx, url = data

    # Skip empty URLs
    if not url:
        return False

    try:
        # Determine folder based on index
        folder_index = idx // images_per_folder
        start_range = folder_index * images_per_folder
        end_range = start_range + images_per_folder - 1
        batch_folder = f"batch_{start_range}_to_{end_range}"

        # Create folder if needed
        folder_path = output_dir / batch_folder
        folder_path.mkdir(exist_ok=True, parents=True)

        # Output file path
        ulr_name = url.split('/')[-1]
        output_path = folder_path / f"{idx}_{ulr_name}.jpg"

        # Skip if already downloaded
        if output_path.exists():
            return True

        # Download image
        content = download_image(url)
        if content is None:
            return False

        # Process image
        img = Image.open(BytesIO(content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        if resize_size:
            img = img.resize(resize_size, Image.Resampling.LANCZOS)

        # Save image
        img.save(output_path, "JPEG")
        return True


    except KeyboardInterrupt:
        raise

    except Exception as e:
        print(f"Critical error processing {url}: {str(e)}")
        return False


def process_batch(batch_data: List[Tuple[int, str]], **kwargs) -> List[bool]:
    """Process a batch of images using threads"""
    results = []
    with ThreadPoolExecutor(max_workers=kwargs.get("threads", 4)) as executor:
        process_func = partial(
            process_image,
            output_dir=kwargs.get("output_dir"),
            resize_size=kwargs.get("resize_size"),
            images_per_folder=kwargs.get("images_per_folder", 1000),
        )

        futures = [executor.submit(process_func, url_data) for url_data in batch_data]

        for future in futures:
            try:
                results.append(future.result())
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Batch processing failed: {str(e)}")
                results.append(False)

    return results


class ImgDownloaderThreadProcess:
    def __init__(
            self,
            output_dir: Path,
            threads_per_process: int = 4,
            resize_size: Optional[Tuple[int, int]] = None,
            batch_size: int = 100,
            images_per_folder: int = 1000,
            num_processes: Optional[int] = None,
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.threads_per_process = threads_per_process
        self.resize_size = resize_size
        self.batch_size = batch_size
        self.images_per_folder = images_per_folder
        self.num_processes = num_processes

    def run(self, data: List[Tuple[int, str]]) -> Tuple[int, int]:
        """Download images using multiple processes and threads"""
        start_time = time()
        total_urls = len(data)

        print(f"Downloading {total_urls} images with {self.num_processes} processes and {self.threads_per_process} threads per process")

        # Split data into batches
        batches = [
            data[i:i + self.batch_size]
            for i in range(0, total_urls, self.batch_size)
        ]

        process_kwargs = {
            "output_dir": self.output_dir,
            "threads": self.threads_per_process,
            "resize_size": self.resize_size,
            "images_per_folder": self.images_per_folder,
        }

        successful = 0
        with tqdm(total=total_urls, desc="Downloading") as pbar:
            try:
                with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
                    futures = [executor.submit(process_batch, batch, **process_kwargs) for batch in batches]
                    executor.shutdown(wait=False)

                    for future in as_completed(futures):
                        results = future.result()
                        batch_success = sum(results)
                        successful += batch_success
                        pbar.update(len(results))

            except KeyboardInterrupt:
                print("\n[!] Received keyboard interrupt. Shutting down...")
                executor.shutdown(cancel_futures=True)
                raise

        elapsed_time = time() - start_time
        print(f"Downloaded {successful}/{total_urls} images in {elapsed_time:.2f} seconds")

        return successful, total_urls


# Example usage
# if __name__ == "__main__":
#     import polars as pl
#     import duckdb
#     from core_pro.ultilities import make_sync_folder
#
#     path = make_sync_folder("dataset/item_matching")
#     path_image = path / "img"
#     file = path / f"data_sample_FMCG.parquet"
#     df = pl.read_parquet(file)
#
#     # download images
#     query = f"""
#     select *
#     ,concat('http://f.shopee.vn/file/', UNNEST(array_slice(string_split(images, ','), 1, 1))) image_url
#     from read_parquet('{str(path / f'{file.stem}.parquet')}')
#     order by item_id, images
#     limit 1000
#     """
#     df = duckdb.sql(query).pl().unique(["item_id"])
#
#     df = df.with_row_index("img_index")
#     run = [(i["img_index"], i["image_url"]) for i in df[["img_index", "image_url"]].to_dicts()]
#
#     downloader = ImageDownloader(
#         output_dir=path_image,
#         threads_per_process=8,
#         resize_size=(224, 224),
#         num_processes=4,
#         images_per_folder=100,
#     )
#
#     # Download images
#     successful, total = downloader.download_images(run)

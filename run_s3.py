import argparse
import logging.config
from src.s3 import download_file_from_s3, upload_file_to_s3

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("s3-pipeline")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("step", default="download",
                        choices=["download", "upload"],
                        help="'download' will download the data from S3. 'upload' will upload data to S3")
    parser.add_argument("--s3_path", default="s3://2022-msia-423-xu-ziru/raw/bodyfat.csv",
                        help="s3 data path to download or upload data")
    parser.add_argument("--local_path", default="data/raw/bodyfat.csv",
                        help="local data path to store or upload data")
    args = parser.parse_args()

    if args.step == "download":
        download_file_from_s3(args.local_path, args.s3_path)
    elif args.step == "upload":
        upload_file_to_s3(args.local_path, args.s3_path)

import os
import sys
import subprocess
import gdown


def clean_google_drive_url(url):
    if "folders/" in url:
        return url.split("?")[0]
    return url


def download_google_drive_folder(folder_url, output_dir, redundancy_check=True, quiet=False, use_cookies=False):
    folder_url = clean_google_drive_url(folder_url)
    if redundancy_check:
        if os.path.exists(output_dir) and os.listdir(output_dir):
            if not quiet:
                print(f"[INFO] Skipping download. Directory '{output_dir}' already exists and contains files.")
            return
    os.makedirs(output_dir, exist_ok=True)
    if not quiet:
        print(f"[INFO] Downloading folder from: {folder_url}")
    gdown.download_folder(url=folder_url, output=output_dir, quiet=quiet, use_cookies=use_cookies)
    if not quiet:
        print(f"[SUCCESS] Files downloaded to: {output_dir}")


def download_google_drive_file(url, output_path, redundancy_check=True, quiet=False, use_cookies=False):
    if redundancy_check:
        if os.path.exists(output_path):
            if not quiet:
                print(f"[SKIPPED] File already exists: {output_path}")
            return output_path
    downloaded_file = gdown.download(url, output=output_path, quiet=quiet, use_cookies=use_cookies)
    if downloaded_file:
        if not quiet:
            print(f"[SUCCESS] File downloaded to: {downloaded_file}")
        return downloaded_file
    else:
        if not quiet:
            print("[ERROR] Download failed.")
        return None



if __name__ == "__main__":
    FOLDER_URL = "https://drive.google.com/drive/folders/1DWsTdFlY0FDkRYSZ--xYvkLNV2PtjWuD?usp=drive_link"
    OUTPUT_DIR = "./assets"

    download_google_drive_folder(FOLDER_URL, OUTPUT_DIR)
























































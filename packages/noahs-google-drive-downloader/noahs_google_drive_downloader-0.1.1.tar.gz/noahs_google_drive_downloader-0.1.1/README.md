# Noahs Google Drive Downloader

This module provides Python functions for downloading **files** and **folders** from public Google Drive URLs using the `gdown` library with the additional option of redundancy checks and the added feature of automatically cleaning urls to match `gdown`'s expected url input format. Just use the normal link to the file or folder that you would use to open it in your web browser and it will download.

## Installation

```bash
pip install noahs_google_drive_downloader
```

---

### `download_google_drive_folder(folder_url, output_dir, redundancy_check=True, quiet=False, use_cookies=False)`

Downloads the contents of a public Google Drive **folder** to a specified local directory.

#### Parameters:
- `folder_url` (str): Public URL to the Google Drive folder.
- `output_dir` (str): Local path to save the downloaded files.
- `redundancy_check` (bool): If `True`, skips download if files already exist in `output_dir`.
- `quiet` (bool): If `True`, suppresses print statements.
- `use_cookies` (bool): Use authentication cookies for private folders (optional).

#### Example:
```python
from noahs_google_drive_downloader import download_google_drive_folder

download_google_drive_folder(
    folder_url="https://drive.google.com/drive/folders/abc123?usp=drive_link",
    output_dir="./my_folder"
)
```

---

### `download_google_drive_file(url, output_path, redundancy_check=True, quiet=False, use_cookies=False)`

Downloads a single public Google Drive **file** to a specified local path.

#### Parameters:
- `url` (str): Public file URL (e.g. `https://drive.google.com/uc?id=...`).
- `output_path` (str): Destination filepath.
- `redundancy_check` (bool): If `True`, skips download if the file already exists at `output_path`.
- `quiet` (bool): If `True`, suppresses print statements.
- `use_cookies` (bool): Use authentication cookies for private files (optional).

#### Example:
```python
from noahs_google_drive_downloader import download_google_drive_file

download_google_drive_file(
    url="https://drive.google.com/file/d/abc123/view?usp=drive_link",
    output_path="./my_folder/my_file.pdf"
)
```

---







"""Download the Kaggle MIT-BIH dataset into data/raw."""
from __future__ import annotations
import base64, json, os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile
DATASET_SLUG = "mondejar/mitbih-database"
DOWNLOAD_URL = f"https://www.kaggle.com/api/v1/datasets/download/{DATASET_SLUG}"
RAW_DIR = Path("data/raw")
ZIP_PATH = RAW_DIR / "mitbih-database.zip"
def load_credentials() -> tuple[str, str]:
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return os.environ["KAGGLE_USERNAME"], os.environ["KAGGLE_KEY"]
    token_path = Path.home() / ".kaggle" / "kaggle.json"
    if token_path.exists():
        token = json.loads(token_path.read_text())
        return token["username"], token["key"]
    raise SystemExit("Missing Kaggle credentials. Set KAGGLE_USERNAME/KAGGLE_KEY or ~/.kaggle/kaggle.json.")
def main() -> None:
    username, key = load_credentials()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    auth = base64.b64encode(f"{username}:{key}".encode()).decode()
    request = Request(DOWNLOAD_URL, headers={"Authorization": f"Basic {auth}"})
    try:
        with urlopen(request, timeout=120) as response, ZIP_PATH.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
    except HTTPError as exc:
        raise SystemExit(f"Kaggle download failed with HTTP {exc.code}. Check credentials and dataset access.") from exc
    except URLError as exc:
        raise SystemExit(f"Network error while downloading Kaggle dataset: {exc}") from exc
    with ZipFile(ZIP_PATH) as archive:
        archive.extractall(RAW_DIR)
    print(f"Downloaded and extracted {DATASET_SLUG} into {RAW_DIR}")
if __name__ == "__main__":
    main()

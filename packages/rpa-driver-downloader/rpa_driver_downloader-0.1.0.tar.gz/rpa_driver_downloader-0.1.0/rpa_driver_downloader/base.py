import json
import requests
import zipfile
import tarfile
from pathlib import Path
from abc import ABC, abstractmethod

SETTINGS_PATH = Path("settings.json")
DRIVER_DIR = Path("drivers")


class BaseDriver(ABC):
    def __init__(self):
        self.settings = self._load_or_create_settings()


    @property
    @abstractmethod
    def key_name(self):
        ...


    @abstractmethod
    def get_download_url(self) -> str:
        ...


    def path_for_the_driver(self) -> str:
        """Returns the absolute path of the driver, downloading if necessary."""
        driver_path = self.settings.get(self.key_name)

        if driver_path and Path(driver_path).exists():
            return driver_path

        print(f"🔍 Driver '{self.key_name}' not found. Downloading...")
        url = self.get_download_url()
        driver_path = self.download_and_extract(url)
        self.settings[self.key_name] = driver_path
        self._save_settings()
        return driver_path


    def _load_or_create_settings(self):
        if SETTINGS_PATH.exists():
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}


    def _save_settings(self):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)


    def download_and_extract(self, url):
        DRIVER_DIR.mkdir(exist_ok=True)
        file_name = url.split("/")[-1]
        zip_path = DRIVER_DIR / file_name

        with requests.get(url, stream=True) as r:
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        if file_name.endswith(".zip"):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(DRIVER_DIR)
        elif file_name.endswith(".tar.gz"):
            with tarfile.open(zip_path, 'r:gz') as tar_ref:
                tar_ref.extractall(DRIVER_DIR)

        zip_path.unlink()

        for item in DRIVER_DIR.iterdir():
            if item.name.startswith(self.key_name.replace("_path", "")) or "driver" in item.name:
                item.chmod(0o755)
                return str(item.resolve())

        raise FileNotFoundError("Driver extracted but not found.")
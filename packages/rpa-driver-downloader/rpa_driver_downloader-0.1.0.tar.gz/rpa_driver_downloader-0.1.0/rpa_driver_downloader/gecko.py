from .base import BaseDriver
import platform
import requests


class Gecko(BaseDriver):
    @property
    def key_name(self):
        return "geckodriver_path"


    def get_download_url(self) -> str:
        os_name = platform.system()
        api_url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
        data = requests.get(api_url).json()

        for asset in data["assets"]:
            name = asset["name"]
            if os_name == "Windows" and "win64.zip" in name:
                return asset["browser_download_url"]
            elif os_name == "Linux" and "linux64.tar.gz" in name:
                return asset["browser_download_url"]
            elif os_name == "Darwin" and "macos" in name:
                return asset["browser_download_url"]

        raise FileNotFoundError("Driver Gecko not found.")
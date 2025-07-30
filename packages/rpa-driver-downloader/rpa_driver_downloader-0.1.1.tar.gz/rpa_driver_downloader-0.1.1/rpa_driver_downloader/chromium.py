from .base import BaseDriver
import platform
import requests


class Chromium(BaseDriver):
    @property
    def key_name(self):
        return "chromiumdriver_path"


    def get_download_url(self) -> str:
        os_name = platform.system()
        base_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        data = requests.get(base_url).json()
        stable = data["channels"]["Stable"]["downloads"]["chromedriver"]

        for item in stable:
            if os_name == "Windows" and item["platform"] == "win64":
                return item["url"]
            elif os_name == "Linux" and item["platform"] == "linux64":
                return item["url"]
            elif os_name == "Darwin" and item["platform"] == "mac-x64":
                return item["url"]

        raise FileNotFoundError("Driver Chromium not found.")

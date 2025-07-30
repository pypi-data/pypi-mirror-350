from .base import BaseDriver
import platform


class Edge(BaseDriver):
    @property
    def key_name(self):
        return "edgedriver_path"


    def get_download_url(self) -> str:
        os_name = platform.system()

        version = "124.0.2478.0"
        if os_name == "Windows":
            return f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
        elif os_name == "Linux":
            return f"https://msedgedriver.azureedge.net/{version}/edgedriver_linux64.zip"
        elif os_name == "Darwin":
            return f"https://msedgedriver.azureedge.net/{version}/edgedriver_mac64.zip"

        raise FileNotFoundError("Driver Edge not found.")

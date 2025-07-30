# ⚠️ This library is currently compatible with Python versions up to 3.11.  
Python 3.12+ is not supported due to `requests` dependency using the removed `cgi` module.

# 🧩 rpa-driver-downloader

**rpa-driver-downloader** is a lightweight Python package that automatically downloads and manages the latest WebDriver binaries (Gecko, Chromium, Edge) for browser automation using **Selenium**, **BotCity**, or any other RPA tool.

Whether you're automating browsers on Linux, Windows, or macOS, this library ensures that the required driver is downloaded and ready to use — with just one line of code.

---

## 🚀 Features

- ✅ Automatic download of GeckoDriver, ChromeDriver, and EdgeDriver
- 📦 Stores drivers locally inside a `/drivers/` folder
- 🔐 Saves driver paths in `settings.json` for reuse
- 🧠 Automatically detects your OS and architecture
- 🔄 Returns absolute path to use with Selenium or BotCity
- 🧪 Works well with testing and RPA environments



## 📦 Installation

```bash
pip install rpa-driver-downloader
```


## ⚙️ Usage

```bash
from rpa_driver_downloader import Gecko, Chromium, Edge

gecko_path = Gecko().path_for_the_driver()
chrome_path = Chromium().path_for_the_driver()
edge_path = Edge().path_for_the_driver()
```


## Example: Using with Selenium

```bash
from selenium import webdriver
from rpa_driver_downloader import Gecko

driver = webdriver.Firefox(executable_path=Gecko().path_for_the_driver())
driver.get("https://example.com")
```


## Example: Using with BotCity

```bash
from botcity.web import BotFirefox
from rpa_driver_downloader import Gecko

bot = BotFirefox(driver_path=Gecko().path_for_the_driver())
bot.browse("https://www.google.com")
```


## 🌐 Supported Browsers & Platforms

| Browser | Windows | Linux | macOS |
| ------- | ------- | ----- | ----- |
| Firefox | ✅       | ✅     | ✅     |
| Chrome  | ✅       | ✅     | ✅     |
| Edge    | ✅       | ✅     | ✅     |


## 📁 Project Structure

```bash
rpa-driver-downloader/
├── rpa_driver_downloader/
│   ├── __init__.py
│   ├── base.py
│   ├── gecko.py
│   ├── chromium.py
│   └── edge.py
├── settings.json          # Created automatically
├── drivers/               # Driver binaries stored here
├── setup.py
└── README.md
```


## 🤝 Contributing
Contributions, issues and feature requests are welcome!
Feel free to check the issues page or submit a pull request.


## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

rpa-driver-downloader is a Python package that automatically downloads and manages the latest Gecko, Chrome, and Edge WebDriver binaries. Designed for use with Selenium and RPA tools like BotCity, it detects the OS and ensures the correct driver is always available — no manual download required.
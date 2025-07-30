from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rpa-driver-downloader",
    version="0.1.1",
    author="Ruan Chaves Machado",
    author_email="whiterun092@gmail.com",
    description="A Python package to automatically download and manage WebDrivers for Gecko, Chrome, and Edge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/rpa-driver-downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7, <3.12',
    install_requires=[
        "requests",
    ],
    include_package_data=True,
)
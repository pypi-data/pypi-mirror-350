from pathlib import Path
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent
setup(
    name="ytp-dl",
    version="0.2.78",
    description="YouTube downloader with Mullvad VPN + optional Flask API",
    long_description=(BASE_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="dumgum82",
    author_email="dumgum42@gmail.com",
    url="https://github.com/dumgum82/ytp-dl",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=["yt-dlp>=2024.0.0","Flask>=3.0","requests>=2.31.0"],
    entry_points={
        "console_scripts":[
            "ytp-dl=ytp_dl.cli:main",
            "ytp-dl-api=ytp_dl.api:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    include_package_data=True,
)

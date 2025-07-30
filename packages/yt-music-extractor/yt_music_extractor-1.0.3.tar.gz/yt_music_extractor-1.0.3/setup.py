from setuptools import setup, find_packages
import sys
import os

# Check Python version
if sys.version_info < (3, 7):
    sys.exit('Python 3.7 or higher is required.')

# Read long description
long_description = ""
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "A Python tool to download music from YouTube with proper metadata and album art."

# Read requirements
requirements = [
    "yt-dlp>=2023.3.4",
    "moviepy>=1.0.3", 
    "mutagen>=1.46.0",
    "pillow>=9.4.0",
    "requests>=2.28.2",
    "setuptools>=67.7.2"
]

requirements_path = "requirements.txt"
if os.path.exists(requirements_path):
    with open(requirements_path, "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name="yt-music-extractor",
    version="1.0.3",
    author="Vighnesh Kontham",
    author_email="vighneshkontham@gmail.com",
    description="Download music from YouTube with proper metadata and album art, featuring parallel processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Captain-Vikram/YTMusic_To_M4A",
    packages=find_packages(),
    py_modules=["main", "config"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yt-music-extractor=main:main",
            "ytme=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    keywords="youtube, music, download, metadata, album art, yt-dlp",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)
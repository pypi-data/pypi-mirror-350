from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="requests-ss",
    version="0.1.8",
    author="wujingweilai",
    author_email="haoxuan1916@qq.com",
    description="A comprehensive web content scraping tool for text, images, audio and video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/requests_ss",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.6.2",
        "Pillow>=8.1.0",
        "audioplayer>=0.6",
        "moviepy>=1.0.3",
        "pandas>=2.2.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.5b0",
            "flake8>=3.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "html-scraper=scraper.cli:main",  # 如果有命令行接口
        ],
    },
    include_package_data=True,
    package_data={
        "scraper": ["*.txt", "*.json"],  # 包含非Python文件
    },
)

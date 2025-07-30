# Web Scraping and Data Processing Toolkit

## Overview

This Python module provides a comprehensive set of tools for web scraping, data extraction, and basic data processing. It includes functionality for handling text, images, audio, video, and tabular data from web sources.

## Installation

Ensure you have Python 3.6+ installed, then install required dependencies:

```bash
pip install requests beautifulsoup4 lxml pandas Pillow audioplayer moviepy
```

## Module Structure

### 1. `html` Class - Web Content Extraction

#### Methods:

- **`txts()`**: Extract text content from web pages with pagination support
- **`txt()`**: Basic text extraction from paragraphs or entire pages
- **`img()`**: Download images from web pages
- **`audio()`**: Extract audio files from web pages
- **`table()`**: Extract and process HTML tables

### 2. `run` Class - Direct Content Download

#### Methods:

- **`music()`**: Download audio files directly
- **`video()`**: Download video content
- **`txt()`**: Download and save text content
- **`table()`**: Extract and process HTML tables

### 3. `show` Class - Content Display

#### Methods:

- **`txt()`**: Display text content from files
- **`image()`**: Display downloaded images
- **`music()`**: Play audio files
- **`video()`**: Preview video files

### 4. Excel Utilities

- **`handle_excel()`**: Provides three modes:
  - `merge`: Combine multiple Excel files
  - `statistics`: Generate value counts for specified data
  - `duplicate`: Remove duplicates from Excel data

## Usage Examples

### Basic Text Extraction

```python
html.txt("https://example.com", mode='p', txt='output')
```

### Image Download

```python
html.img("https://example.com/gallery", img_div_class="gallery")
```

### Table Processing

```python
html.table("https://example.com/data", turn=True, arrange='price')
```

### Excel Operations

```python
handle_excel(mode='merge')  # Follow interactive prompts
```

## Features

- **User-Agent Spoofing**: All requests include browser-like headers
- **Pagination Support**: Automatically follow "next page" links
- **Flexible Content Handling**: Works with various HTML structures
- **Data Processing**: Sort and clean extracted data
- **Media Playback**: Built-in preview for images, audio and video

## Notes

1. Use this tool responsibly and respect website terms of service
2. Some methods may require additional error handling for production use
3. Media playback features need optional dependencies (Pillow, audioplayer, moviepy)

## License

This project is provided as-is without warranty. Users are responsible for complying with all applicable laws and website terms of service when using this tool.



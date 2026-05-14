# New Feed AI Crawler

A robust web crawler designed to bypass bot protection and gather data topic-wise from any website.

## Features

- **Bot Protection Bypass**: Uses Playwright with Stealth mode and random User-Agents.
- **Topic-wise Extraction**: Automatically groups content under page headings (H1, H2, H3).
- **JSON Output**: Saves results in a structured JSON format, keyed by website URL.
- **CLI Support**: Accept a list of URLs as command-line arguments.

## Installation

1. Install dependencies:
   ```bash
   pip install playwright playwright-stealth beautifulsoup4
   ```

2. Install the Playwright browser:
   ```bash
   playwright install chromium
   ```

   *Note: If you encounter permission issues on macOS, try:*
   ```bash
   export PLAYWRIGHT_BROWSERS_PATH=$PWD/pw-browsers
   playwright install chromium
   ```

## Usage

Run the crawler by providing a list of URLs:

```bash
python main.py https://example.com https://wikipedia.org
```

The data will be saved to `crawled_data.json`.

## Project Structure

- `crawler.py`: Core crawling logic.
- `main.py`: CLI entry point.
- `pyproject.toml`: Project dependencies and configuration.

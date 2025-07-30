# Tor Search

Search the web anonymously through the Tor network. This Python package allows you to make search queries to Google, DuckDuckGo, and Yandex via the Tor network, protecting your privacy.

## Features

- Anonymous web searching through Tor network
- Support for multiple search engines:
  - DuckDuckGo (most reliable through Tor)
  - Google
  - Yandex
- Command line interface
- Python API for integration into your own projects
- User agent rotation
- CAPTCHA detection for Yandex

## Installation

### Prerequisites

You need to have Tor running on your system:
- On Mac/Linux: `brew install tor` then `brew services start tor`
- On Ubuntu/Debian: `apt-get install tor` then `service tor start`
- On Windows: Install the Tor Browser Bundle and ensure it's running

### Install from PyPI

```bash
pip install tor-search
```

## Usage

### Command Line
```bash
# Basic search with DuckDuckGo (default)
tor-search "python programming"

# Search with Google and show 5 results
tor-search "python programming" -e google -n 5

# Search with Yandex
tor-search "machine learning" -e yandex
```

### Python Module
```bash
from tor_search import TorSearcher

# Create a searcher instance
searcher = TorSearcher()

try:
    # Connect to Tor and search
    results = searcher.search("python programming", num_results=3, engine="duckduckgo")
    
    # Process results
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['link']}")
        print(f"Snippet: {result.get('snippet', '')}")
        print()
        
    # You can perform additional searches without reconnecting
    more_results = searcher.search("machine learning", engine="google")
finally:
    # Always disconnect when done to restore original socket
    searcher.disconnect()
```

## License
MIT License

## Disclaimer
This tool is meant for legitimate privacy-focused research. Please use responsibly and respect search engines' terms of service.
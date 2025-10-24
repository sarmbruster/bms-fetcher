# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BMS Fetcher is a Python tool that fetches CSV data from the BMS Bayern web portal (https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx). The main challenge is that the CSV data cannot be downloaded directly - it requires a multi-step process:

1. Fetch the main page and extract hidden form fields
2. Parse the HTML to find the "Export" link and extract the `__EVENTTARGET` parameter from its JavaScript `__doPostBack` call
3. Send a POST request with all hidden form values and the extracted `__EVENTTARGET` parameter
4. The POST response contains the CSV data

## Architecture

The codebase is intentionally minimal with a single entry point:

- `fetch.py` - Main executable script containing all fetching logic
- `bms-fetcher/__init__.py` - Empty package file

The fetching logic uses:
- `requests.Session()` to maintain cookies between requests
- `BeautifulSoup` for HTML parsing and extracting hidden form fields
- Regex to extract the `__EVENTTARGET` value from the Export link's `href` attribute

## Development Commands

### Installation
```bash
poetry install
```

### Running the fetcher
```bash
poetry run ./fetch.py
```

The script outputs the CSV data to stdout.

### Debugging HTTP requests
The file `fetch.py:7-23` contains commented-out debugging code that enables HTTP-level logging via the `http.client` and `logging` modules. Uncomment these lines to see full REQUEST/RESPONSE headers and data for troubleshooting.

## Key Implementation Details

- The session must maintain cookies between the initial GET and the subsequent POST request
- All hidden form fields from the initial page must be included in the POST request
- The `__EVENTTARGET` parameter is extracted from the Export link's `href` attribute via regex: `__doPostBack\('([^']+)'`
- A custom User-Agent header is set to mimic a browser

## Guidelines

- When committing code to git, apply "conventional commits" (https://www.conventionalcommits.org/en/v1.0.0/) as best practice for your commit messages
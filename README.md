# BMS Fetcher

A tool to fetch the CSV file from https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx.

Since there is no direct simple way to download the csv file for that page we're using [Playwright](https://playwright.dev/python/) to simulate a browser and click on 'export' button.

## Installation

```bash
poetry install
poetry run playwright install chromium
```

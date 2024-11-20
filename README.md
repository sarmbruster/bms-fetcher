# BMS Fetcher

A tool to fetch the CSV file from https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx.

Unfortunatly that web page does not deliver the csv data directly.
Instead you need to first fetch the main page, which contains a couple of hidden form fields.
Additionally the value from the href attribute of link `Export` needs to be added as `__EVENTTARGET=ct100...ct109` (as example) to the parameters.
The combined parameters are sent together with the cookie in HTTP POST request that finally delivers the csv file.

## Installation & Usage

```bash
poetry install
poetry run ./fetch.py
```

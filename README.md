# BMS Fetcher

A tool to fetch the CSV file from https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx.

Unfortunatly that web page does not deliver the csv data directly.
Instead you need to first fetch the main page, which contains a couple of hidden form fields.
Those values need to put as payload together with `__EVENTTARGET=ctl00$ctl00$CM$CM$CtrlCourses$CtrlCoursesList$CtrlGrid$ctl11$ctl09` in a HTTP POST request.

The second request delivers the csv file finally.

## Installation & Usage

```bash
poetry install
poetry run ./fetch.py
```

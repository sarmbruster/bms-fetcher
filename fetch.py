#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.bms-fw.bayern.de/Navigation/Public/lastminute.aspx")

        with page.expect_download() as download_info:
            page.get_by_role("link", name="Export", exact=True).click()
        download = download_info.value
        download.save_as(download.suggested_filename)
        browser.close()

if __name__ == "__main__":
    main()
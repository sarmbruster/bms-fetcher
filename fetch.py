#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests, re
# import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# import re
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

def main():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
    r = s.get("https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx")
    if (r.status_code != 200):
        raise RuntimeError("Error: Could not fetch page")

    html = BeautifulSoup(r.content, "html.parser")
    hidden_inputs = html.find_all("input", type="hidden")
    hidden_values = {input_tag.get("name"): input_tag.get("value") for input_tag in hidden_inputs}

    # extract __EVENTTARGET from 'Export' link
    export_link = html.find("a", string="Export")
    if export_link:
        href = export_link.get("href")
        match = re.search(r"__doPostBack\('([^']+)'", href)
        if match:
            hidden_values["__EVENTTARGET"] = match.group(1)
        else:
            raise RuntimeError("Error: Could not extract __EVENTTARGET from href")
    else:
        raise RuntimeError("Error: Could not find export link")

    # for key, value in hidden_values.items():
    #     print(f"{key}: {value}")    
    csv = s.post("https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx", data=hidden_values)
    if (csv.status_code != 200):
        raise RuntimeError("Error: Could not fetch csv")    
    csv_lines = csv.text.splitlines()
    for line in csv_lines[:10]:
        print(line)

if __name__ == "__main__":
    main()
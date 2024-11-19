#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
# import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

def main():
    s = requests.Session()
    r = s.get("https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx")
    if (r.status_code != 200):
        raise RuntimeError("Error: Could not fetch page")

    html = BeautifulSoup(r.content, "html.parser")
    hidden_inputs = html.find_all("input", type="hidden")
    hidden_values = {input_tag.get("name"): input_tag.get("value") for input_tag in hidden_inputs}
    hidden_values["__EVENTTARGET"] ='ctl00$ctl00$CM$CM$CtrlCourses$CtrlCoursesList$CtrlGrid$ctl11$ctl09'
    csv = s.post("https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx", data=hidden_values)
    if (csv.status_code != 200):
        raise RuntimeError("Error: Could not fetch csv")    
    print(csv.text)

if __name__ == "__main__":
    main()
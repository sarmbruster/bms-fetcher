#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests, re, sys
import logging
import csv
import io

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# Redirect http.client debug output to stderr
http_client.HTTPConnection.debuglevel = 1
http_client.print = lambda *args: sys.stderr.write(" ".join(str(arg) for arg in args) + "\n")

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
            # for key, value in hidden_values.items():
            #     print(f"{key}: {value}")    
            csvFile = s.post("https://www.bms-fw.bayern.de/Navigation/Public/LastMinute.aspx", data=hidden_values)
            if (csvFile.status_code != 200):
                raise RuntimeError("Error: Could not fetch csv")

            # The server sends windows-1252 (Western European) encoded content
            # This encoding properly handles German umlauts (ü, ö, ä, ß)
            # Note: charset_normalizer may detect cp1250, but windows-1252 is correct
            csvFile.encoding = 'windows-1252'
            logging.info(f"CSV response: status_code={csvFile.status_code}, encoding={csvFile.encoding}, content_length={len(csvFile.content)}")

            csv_text = csvFile.text
            print(csv_text, file=sys.stderr)
  
            try:
                dialect = csv.Sniffer().sniff(csv_text[:1024])
                logging.info(f"Detected CSV dialect: delimiter='{dialect.delimiter}', quotechar='{dialect.quotechar}'")
            except csv.Error:
                first_line = csv_text.split('\n')[0]
                dialect = csv.excel()
                dialect.delimiter = ',' if ',' in first_line else ';'
                logging.info(f"Using default CSV dialect: delimiter='{dialect.delimiter}'")

            csv_input = io.StringIO(csv_text)
            csv_output = io.StringIO()

            reader = csv.reader(csv_input, dialect=dialect)
            writer = csv.writer(csv_output, delimiter=',')

            for row in reader:
                writer.writerow(row)

            # Output to stdout as UTF-8
            print(csv_output.getvalue(), end='')

        else:
            raise RuntimeError("Error: Could not extract __EVENTTARGET from href")
    else:
        print("Error: Could not find export link")
        #raise RuntimeError("Error: Could not find export link")

if __name__ == "__main__":
    main()

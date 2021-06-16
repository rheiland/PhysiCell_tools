# Simple search for terms in SMB2021 web pages 
# Author: Randy Heiland
from urllib.request import urlopen
import re

#pages = ["http://schedule.smb2021.org/CBBS/"]
# Demo with a few pages
pages = ["http://schedule.smb2021.org/CBBS/", \
            "http://schedule.smb2021.org/CDEV/", \
            "http://schedule.smb2021.org/DDMB/", \
            "http://schedule.smb2021.org/DDMB/", \
            "http://schedule.smb2021.org/IMMU/", \
    ]

for url in pages:
    # print(url)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    # print(html)
    string_to_find = "cyano"
    # print(" --- find ")
    found = re.findall(string_to_find, html, re.IGNORECASE)
    if found:
        print(string_to_find, "  found in " ,url)

    string_to_find = "ODE"
    found = re.findall(string_to_find, html)
    if found:
        print(string_to_find, "  found in " ,url)

    string_to_find = "boolean"
    found = re.findall(string_to_find, html, re.IGNORECASE)
    if found:
        print(string_to_find, "  found in " ,url)

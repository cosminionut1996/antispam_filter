from antispam.email_helper import Email
from email.header import decode_header
import os
import sys

try:
    folder = sys.argv[1]
except IndexError:
    print("usage: subject_format_test folder")
    exit(0)


# Go through all emails
# Get the title
# Find the encodings
# Count them and retrieve a list

encodings = dict()

for f in os.scandir(folder):
    e = Email(f.path)
    decoded_header = decode_header(e.title)
    if len(decoded_header) > 1 or decoded_header[0][1] != None:
        encoding = None
        for dh in decoded_header:
            if dh[1] == None:
                continue
            else:
                encoding = dh[1]
                print(f.path)

            if dh[1] != None and dh[1] not in encodings:
                encodings[dh[1]] = 1
            else:
                encodings[dh[1]] += 1

import pprint

pprint.pprint(encodings)

"""
{'big5': 1,
 'gb2312': 154,
 'iso-2022-jp': 303,
 'iso-8859-1': 15,
 'iso-8859-15': 2,
 'iso-8859-9': 2,
 'koi8-r': 16,
 'shift_jis': 76,
 'utf-8': 119,
 'windows-1251': 19,
 'windows-1252': 2,
 'windows-1254': 1,
 'x-sjis': 20}

{'iso-2022-jp': 3,
 'iso-8859-1': 183,
 'iso-8859-15': 7,
 'iso-8859-7': 28,
 'koi8-r': 16,
 'utf-8': 158,
 'windows-1252': 6,
 'windows-1256': 1}
"""

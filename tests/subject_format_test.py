import os
import re
import sys
from email.header import decode_header


try:
    folder = sys.argv[1]
except IndexError:
    print("usage: subject_format_test folder")
    exit(0)


weird_format = 0
err = 0
usual = 0
indented_2nd_line = 0

for f in os.scandir(folder):
    try:
        with open(f.path, 'r', encoding='utf-8', errors='ignore') as fin:
            l = fin.readline()
            try:
                l2 = fin.readline()

            except Exception:
                pass
            else:
                if re.match(r'\s+.+', l2):
                    indented_2nd_line += 1
                    # print("indented: ", l2)
    except Exception as exc:
        # print("%s\n%s", f.path, exc)
        pass
    try:
        assert l.startswith('Subject:')
    except AssertionError:
        print(f.path)
        err += 1
    else:
        # print(decode_header(l[len('Subject:'):]))
        if '=?' in l:
            weird_format += 1
            # print(l[:-1], "       ", f.path)
        else:
            usual += 1
print()
print("Weird format: ", weird_format)
print("Usual: ", usual)
print("Err: ", err)

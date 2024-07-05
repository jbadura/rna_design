#! /usr/bin/env python
import csv
import sys

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)
writer.writerow(["l1", "l2", "l3", "decision"])

for row in reader:
    if row[2] == "3-way junction":
        fields = list(map(lambda x: len(x) - 2, row[4].split("-")))
        fields.append(row[0] == "RF01739")
        writer.writerow(fields)

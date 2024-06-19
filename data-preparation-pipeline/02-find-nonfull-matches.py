#! /usr/bin/env python
import glob
import os

for path in sorted(glob.iglob("fasta/*")):
    for directory in ("dbn", "dbn-no-fold"):
        dbn = f"{directory}/{path[6:-3]}.dbn"

        if os.path.exists(dbn):
            with open(path) as f:
                lines = list(map(str.strip, f.readlines()))

            fasta_lens = {lines[i]: len(lines[i + 1]) for i in range(0, len(lines), 2)}

            with open(dbn) as f:
                lines = list(map(str.strip, f.readlines()))

            dbn_lens = {lines[i]: len(lines[i + 1]) for i in range(0, len(lines), 3)}

            for key, value in fasta_lens.items():
                if value != dbn_lens.get(key, 0):
                    print(f"rm {dbn}")
                    break

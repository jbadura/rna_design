#! /usr/bin/env python
import os
from concurrent.futures import ProcessPoolExecutor


def process_dbn(path):
    print(f"Processing {path}")
    base = os.path.basename(path).replace(".dbn", "")
    dir = os.path.dirname(path)
    os.makedirs(f"{dir}/{base}", exist_ok=True)

    with open(path) as f:
        lines = list(map(str.strip, f.readlines()))

    i = 0
    j = 1
    while i < len(lines):
        output = f"{dir}/{base}/{j:09d}.dbn"
        if not os.path.exists(output):
            with open(output, "w") as f:
                f.write(f"{lines[i]}\n{lines[i + 1]}\n{lines[i + 2]}\n")
        i += 3
        j += 1


tasks = []

with open("stats-dbn.txt") as f:
    for line in f:
        fields = line.strip().split()
        family, correct, dbn, nofold = (
            fields[0],
            int(fields[1]),
            int(fields[2]) if len(fields) >= 3 else 0,
            int(fields[3]) if len(fields) >= 4 else 0,
        )
        tasks.append((family, correct, dbn, nofold))


with ProcessPoolExecutor() as executor:
    for task in sorted(tasks, key=lambda x: x[1]):
        family, correct, dbn, nofold = task

        if dbn != correct:
            executor.submit(process_dbn, f"dbn/{family}.dbn")
        if nofold != correct:
            executor.submit(process_dbn, f"dbn-no-fold/{family}.dbn")

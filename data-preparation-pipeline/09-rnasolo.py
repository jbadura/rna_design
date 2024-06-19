#! /usr/bin/env python
import csv
import glob
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import List

import orjson
from rnapolis.common import BpSeq, Entry


@dataclass
class Strand:
    first: int
    last: int
    sequence: str
    structure: str


@dataclass
class Loop:
    base: str
    strands: List[Strand]
    sequence: str
    structure: str
    bpseq: BpSeq


loops = []

for path in glob.iglob("rnasolo-3.326/*.json"):
    base = os.path.basename(path).replace(".txt", "")

    # ignore multi-chain
    if "-" in base.split("_")[2]:
        print(f"Skipping {base} due to multi-chain", file=sys.stderr)
        continue

    with open(path) as f:
        data = orjson.loads(f.read())

    # ignore phosphorus-only structures
    if data["dotBracket"] == "":
        print(f"Skipping {base} due to phosphorus-only structure", file=sys.stderr)
        continue

    _, sequence, structure = data["dotBracket"].split()

    # ignore impossible structures
    if "()" in structure or "(.)" in structure:
        print(f"Skipping {base} due to impossible structure", file=sys.stderr)
        continue

    bpseq = BpSeq.from_string(data["bpseq"])

    for loop in data["loops"]:
        line = loop["description"]
        fields = line.split()
        strands = []

        for i in range(1, len(fields), 4):
            strands.append(
                Strand(
                    int(fields[i]),
                    int(fields[i + 1]),
                    fields[i + 2],
                    fields[i + 3],
                )
            )

        loops.append(Loop(base, strands, sequence, structure, bpseq))


def generate_csv_rows(motif):
    first = min([strand.first for strand in motif.strands])
    last = max([strand.last for strand in motif.strands])

    def fragment_structure(first, last):
        entries = [
            Entry(entry.index_, entry.sequence, entry.pair)
            for entry in motif.bpseq.entries
            if first <= entry.index_ <= last
        ]
        assert len(entries) == last - first + 1
        for entry in entries:
            if entry.pair < first or entry.pair > last:
                entry.pair = 0
            entry.index_ -= first - 1
            if entry.pair > 0:
                entry.pair -= first - 1
        # for i, entry in enumerate(entries):
        #     assert i + 1 == entry.index_
        return BpSeq(entries).dot_bracket.structure

    stems, _, _, _ = motif.bpseq.elements
    first_stem, last_stem = None, None

    for stem in stems:
        if stem.strand5p.first <= first <= stem.strand5p.last:
            first_stem = stem.strand5p.first
        if stem.strand3p.first <= last <= stem.strand3p.last:
            last_stem = stem.strand3p.last

    if first_stem is None:
        raise Exception(f"First stem not found for {motif.base}")
    if last_stem - first_stem + 1 < last - first + 1:
        raise Exception(f"First stem is after first strand for {motif.base}")

    return [
        motif.base,
        (
            "Internal loop"
            if len(motif.strands) == 2
            else f"{len(motif.strands)}-way junction"
        ),
        "-".join([strand.sequence for strand in motif.strands]),
        "-".join([strand.structure for strand in motif.strands]),
        last - first + 1,
        motif.sequence[first - 1 : last],
        fragment_structure(first, last),
        last_stem - first_stem + 1,
        motif.sequence[first_stem - 1 : last_stem],
        fragment_structure(first_stem, last_stem),
        len(motif.sequence),
        motif.sequence,
        motif.structure,
    ]


with open("loops.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "Source",
            "Type",
            "Pattern sequence",
            "Pattern structure",
            "Fragment length",
            "Fragment sequence",
            "Fragment structure",
            "Fragment length + stem",
            "Fragment sequence + stem",
            "Fragment structure + stem",
            "Whole length",
            "Whole sequence",
            "Whole structure",
        ]
    )

    with ProcessPoolExecutor() as executor:
        writer.writerows(executor.map(generate_csv_rows, loops))

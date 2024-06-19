#! /usr/bin/env python
import csv
import glob
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import List

from rnapolis.common import BpSeq, DotBracket, Entry
from tqdm import tqdm


@dataclass
class Strand:
    first: int
    last: int
    sequence: str
    structure: str


@dataclass
class Loop:
    family: str
    header: str
    strands: List[Strand]
    sequence: str
    structure: str
    bpseq: BpSeq


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
        raise Exception(f"First stem not found for {motif.family} {motif.header}")
    if last_stem - first_stem + 1 < last - first + 1:
        raise Exception(
            f"First stem is after first strand for {motif.family} {motif.header}"
        )

    return [
        motif.family,
        motif.header,
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


def extract_loops(path):
    rows = []
    family = os.path.basename(os.path.dirname(path))
    dbn = DotBracket.from_file(path.replace(".motif", ".dbn"))
    bpseq = BpSeq.from_dotbracket(dbn)

    with open(path.replace(".motif", ".dbn")) as f:
        header = f.readline().strip()

    with open(path) as f:
        for line in f:
            if line.startswith("Loop"):
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

                motif = Loop(
                    family, header, strands, dbn.sequence, dbn.structure, bpseq
                )
                rows.append(generate_csv_rows(motif))

    return rows


for variant in ("", "-no-fold"):
    with open(f"rfam{variant}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Family",
                "Header",
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
            paths = glob.glob(f"dbn{variant}/*/*.motif")
            for rows in tqdm(executor.map(extract_loops, paths), total=len(paths)):
                writer.writerows(rows)

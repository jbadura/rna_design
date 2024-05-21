#! /usr/bin/env python
import glob
import itertools
from concurrent.futures import ProcessPoolExecutor

from rnapolis.common import BpSeq, DotBracket
from tqdm import tqdm


def process_file(path):
    bpseq = BpSeq.from_dotbracket(DotBracket.from_file(path))
    stems, single_strands, hairpins, loops = bpseq.elements

    with open(path.replace(".dbn", ".motif"), "w") as f:
        for element in itertools.chain(stems, single_strands, hairpins, loops):
            f.write(f"{element}\n")


with ProcessPoolExecutor() as executor:
    paths = glob.glob("dbn*/*/*.dbn")
    for _ in tqdm(executor.map(process_file, paths), total=len(paths)):
        pass

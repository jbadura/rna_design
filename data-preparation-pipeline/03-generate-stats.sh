#! /bin/bash
(
	cd fasta
	for f in *; do paste <(echo ${f}) <(zcat ${f} | grep -c '^>') <(cat ../dbn/${f%.fa.gz}.dbn | grep -c '^>') <(cat ../dbn-no-fold/${f%.fa.gz}.dbn | grep -c '^>'); done | tee ../stats.txt
)

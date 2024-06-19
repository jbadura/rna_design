#! /bin/bash
mkdir -p fasta
(
	cd fasta
	aria2c -x 5 -i ../urls.txt
)

tar xfz rnasolo-3.326.tar.gz

#! /bin/bash
mkdir -p dbn dbn-no-fold

for fasta in fasta/*; do
	family=${fasta#fasta/}
	family=${family%.fa.gz}
	tmp1=$(mktemp --suffix=.fa)
	tmp2=$(mktemp --suffix=.fa)
	zcat ${fasta} >${tmp1}
	zcat ${fasta} >${tmp2}
	echo "rfam-folder --family ${family} --no-fold ${tmp2} > dbn-no-fold/${family}.dbn; rm ${tmp1}; mkdir -p dbn-no-fold/${family}"
	echo "rfam-folder --family ${family} ${tmp2} > dbn/${family}.dbn; rm ${tmp2}; mkdir -p dbn/${family}"
done | parallel --bar -j $(nproc)

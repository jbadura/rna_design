#! /bin/bash
generate_tasks() {
	cat stats.txt | sort -n -k 2 | awk '
        { family = substr($1, 1, 7) }
        $2 != $3 { printf("tmp=$(mktemp --suffix=.fa); zcat fasta/%s.fa.gz > ${tmp}; rfam-folder --family %s ${tmp} > dbn/%s.dbn; rm ${tmp}; mkdir -p dbn/%s\n", family, family, family, family) }
        $2 != $4 { printf("tmp=$(mktemp --suffix=.fa); zcat fasta/%s.fa.gz > ${tmp}; rfam-folder --family %s ${tmp} --no-fold > dbn-no-fold/%s.dbn; rm ${tmp}; mkdir -p dbn-no-fold/%s\n", family, family, family, family) }
    '
}

generate_tasks | parallel --bar -j $(nproc) --halt now,fail=1

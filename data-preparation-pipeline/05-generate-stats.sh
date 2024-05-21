#! /bin/bash
(
	cd dbn
	for f in *.dbn; do paste <(echo ${f/.dbn/}) <(cat ${f} | wc -l) <(find ${f/.dbn/} -type f -print0 | wc -l --files0-from=- | tail -n1 | awk '{ print $1 }') <(find ../dbn-no-fold/${f/.dbn/} -type f -print0 | wc -l --files0-from=- | tail -n1 | awk '{ print $1 }'); done | tee ../stats-dbn.txt
)

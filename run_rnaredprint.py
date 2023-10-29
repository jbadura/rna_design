import os
import sys
import subprocess

# RNARedPrint uses inputs from rnainverse

for veri, vero in [('rnainverse', 'rnaredprint'), ('rnainverse_extended', 'rnaredprint_extended')]:

    indir = f'/rna_design/inputs/{veri}'
    outdir = f'/rna_design/outputs/{vero}'

    for fn in os.listdir(indir):
        tmp = fn.split('.')[0]
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')
        seq = infile.readline().strip()
        infile.close()

        command = ['time', '/RNARedPrint/_inst/bin/RNARedPrint', '--num', '1', seq]
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()

import os
import sys
import subprocess

# RNARedPrint uses inputs from rnainverse

for veri, vero in [('rnainverse', 'rnaredprint'), ('rnainverse_extended', 'rnaredprint_extended')]:

    indir = f'inputs/{veri}'
    outdir = f'outputs/{vero}'

    for fn in os.listdir(indir):
        print(fn)
        tmp = fn.split('.')[0]
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')
        seq = infile.readline().strip()
        infile.close()

        command = ['/RNARedPrint/_inst/bin/RNARedPrint', '--num', '1', {seq}]
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()

import os
import sys
import subprocess

for ver in ['rnainverse', 'rnainverse_extended']:

    indir = f'inputs/{ver}'
    outdir = f'outputs/{ver}'

    for fn in os.listdir(indir):
        print(fn)
        tmp = fn.split('.')[0]
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')

        command = ['RNAinverse']
        subprocess.run(command, stdin=infile, stdout=outfile, stderr=errfile)
        
        infile.close()
        outfile.close()
        errfile.close()

import os
import sys
import subprocess

for ver in ['rnasfbinv', 'rnasfbinv_extended']:

    indir = f'/rna_design/inputs/{ver}'
    outdir = f'/rna_design/outputs/{ver}'

    for fn in os.listdir(indir):
        tmp = fn.split('.')[0]
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        command = ['time', 'python3', '/RNAsfbinv/RNAfbinvCL.py', '-f', f'{indir}/{fn}']
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()


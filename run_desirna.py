import os
import sys
import subprocess

indir = 'inputs/desirna'
outdir = 'outputs/desirna'

for fn in os.listdir(indir):
    print(fn)
    tmp = fn.split('.')[0]
    outfile = open(f'{outdir}/{tmp}.out', 'w')
    errfile = open(f'{outdir}/{tmp}.err', 'w')

    command = ['python3', '/DesiRNA/DesiRNA.py', '-f', f'{indir}/{fn}', '-t', '10']
    subprocess.run(command, stdout=outfile, stderr=errfile)
    
    outfile.close()
    errfile.close()


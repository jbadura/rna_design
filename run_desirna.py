import os
import sys
import subprocess

if len(sys.argv) == 3:
    range_s = int(sys.argv[1])
    range_e = int(sys.argv[2])
else:
    range_s = -1
    range_e = 10000

for ver in ['desirna', 'desirna_extended']:

    indir = f'/rna_design/inputs/{ver}'
    outdir = f'/rna_design/outputs/{ver}'

    for fn in os.listdir(indir):
        print(fn)
        tmp = fn.split('.')[0]

        if not range_s <= int(tmp) < range_e:
            continue

        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        command = ['time', 'python3', '/DesiRNA/DesiRNA.py', '-f', f'{indir}/{fn}']
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()


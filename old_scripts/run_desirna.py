import os
import sys
import subprocess

if len(sys.argv) == 3:
    range_s = int(sys.argv[1])
    range_e = int(sys.argv[2])
else:
    range_s = 0
    range_e = 20000

dirs = [('/rna_design/inputs/desirna', '/rna_design/outputs/desirna'), ('/rna_design/inputs/desirna_extended', '/rna_design/outputs/desirna_extended')]

for indir, outdir in dirs:

    to_do = os.listdir(indir)
    to_do.sort()
    to_do = to_do[range_s:range_e]
    for fn in to_do:
        print(fn)
        tmp = fn.split('.')[0]

        if os.path.isfile(f'{outdir}/{tmp}.out'):
            continue

        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        command = ['time', 'python3', '/DesiRNA/DesiRNA.py', '-f', f'{indir}/{fn}']
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()


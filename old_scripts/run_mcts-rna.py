import os
import sys
import subprocess

if len(sys.argv) == 3:
    range_s = int(sys.argv[1])
    range_e = int(sys.argv[2])
else:
    range_s = 0
    range_e = 20000

# info-rna uses inputs from rnainverse
dirs = [('/rna_design/inputs/rnainverse', '/rna_design/outputs/mcts-rna'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/mcts-rna_extended')]

for indir, outdir in dirs:

    to_do = os.listdir(indir)
    to_do.sort()
    to_do = to_do[range_s:range_e]
    for fn in to_do:
        tmp = fn.split('.')[0]
        
        if os.path.isfile(f'{outdir}/{tmp}.out'):
            continue
        
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')
        seq = infile.readline().strip()
        infile.close()

        command = ['time', 'python2', '/MCTS-RNA/MCTS-RNA.py', '-s', seq]
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()

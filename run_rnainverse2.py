import os
import sys
import subprocess

if len(sys.argv) == 3:
    range_s = int(sys.argv[1])
    range_e = int(sys.argv[2])
else:
    range_s = 0
    range_e = 20000

dirs = [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/rnainverse')]

for indir, outdir in dirs:

    to_do = os.listdir(indir)
    to_do.sort()
    to_do = to_do[range_s:range_e]
    for fn in to_do:
        tmp = fn.split('.')[0]
        
        if os.path.isfile(f'{outdir}/{tmp}.inv.out'):
            continue
        
        outfile = open(f'{outdir}/{tmp}.inv.out', 'w')
        errfile = open(f'{outdir}/{tmp}.inv.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')

        command = ['time', 'RNAinverse', '-R10']
        subprocess.run(command, stdin=infile, stdout=outfile, stderr=errfile)
        
        infile.close()
        outfile.close()
        errfile.close()

        outfile = open(f'{outdir}/{tmp}.inv.out', 'r')
        outfile2 = open(f'{outdir}/{tmp}.stripped.out', 'w')
        for l in outfile:
            seq = l.strip().split()[0]
            outfile2.write(seq + '\n')
        outfile.close()    
        outfile2.close()

        outfile = open(f'{outdir}/{tmp}.fold.out', 'w')
        errfile = open(f'{outdir}/{tmp}.fold.err', 'w')

        infile = open(f'{outdir}/{tmp}.stripped.out', 'r')
        
        command = ['time', 'RNAfold']
        subprocess.run(command, stdin=infile, stdout=outfile, stderr=errfile)
        
        infile.close()
        outfile.close()
        errfile.close()
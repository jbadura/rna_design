import os
import sys
import subprocess

for ver in ['rnainverse', 'rnainverse_extended']:

    indir = f'/rna_design/inputs/{ver}'
    outdir = f'/rna_design/outputs/{ver}'

    for fn in os.listdir(indir):
        print(fn)
        tmp = fn.split('.')[0]
        outfile = open(f'{outdir}/{tmp}.inv.out', 'w')
        errfile = open(f'{outdir}/{tmp}.inv.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')

        command = ['time', 'RNAinverse']
        subprocess.run(command, stdin=infile, stdout=outfile, stderr=errfile)
        
        infile.close()
        outfile.close()
        errfile.close()
        
        
        outfile = open(f'{outdir}/{tmp}.inv.out', 'r')
        seq = outfile.readline().strip().split()[0]
        outfile.close()
        outfile = open(f'{outdir}/{tmp}.stripped.out', 'w')
        outfile.write(seq + '\n')
        outfile.close()


        outfile = open(f'{outdir}/{tmp}.fold.out', 'w')
        errfile = open(f'{outdir}/{tmp}.fold.err', 'w')

        infile = open(f'{outdir}/{tmp}.stripped.out', 'r')
        
        command = ['time', 'RNAfold']
        subprocess.run(command, stdin=infile, stdout=outfile, stderr=errfile)
        
        infile.close()
        outfile.close()
        errfile.close()

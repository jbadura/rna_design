import os
import sys
import subprocess

def run_desirna(indir, outdir, fn, repeats=1):
    for num in range(repeats):
        tmp = fn.split('.')[0]

        if repeats > 1:
            tmp = f'{tmp}_{num}'
        
        if os.path.isfile(f'{outdir}/{tmp}.out'):
            continue

        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        command = ['time', 'python3', '/DesiRNA/DesiRNA.py', '-f', f'{indir}/{fn}']
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()
    
def run_dss_opt(indir, outdir, fn, repeats=1):
    for num in range(repeats):
        tmp = fn.split('.')[0]
        
        if repeats > 1:
            tmp = f'{tmp}_{num}'
        
        if os.path.isfile(f'{outdir}/{tmp}.out'):
            continue
        
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        infile = open(f'{indir}/{fn}', 'r')
        seq = infile.readline().strip()
        infile.close()

        command = ['time', '/dss-opt/opt-md', seq]
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()
    
def run_info_rna(indir, outdir, fn, repeats=1):
    tmp = fn.split('.')[0]
    
    if os.path.isfile(f'{outdir}/{tmp}.out'):
        return
    
    outfile = open(f'{outdir}/{tmp}.out', 'w')
    errfile = open(f'{outdir}/{tmp}.err', 'w')

    infile = open(f'{indir}/{fn}', 'r')
    seq = infile.readline().strip()
    infile.close()
    if repeats == 1:
        command = ['time', '/INFO-RNA-2.1.2/INFO-RNA-2.1.2', seq]
    else:
        command = ['time', '/INFO-RNA-2.1.2/INFO-RNA-2.1.2', seq, '-R', str(repeats)]
    subprocess.run(command, stdout=outfile, stderr=errfile)
    
    outfile.close()
    errfile.close()

def run_mcts_rna(indir, outdir, fn, repeats=1):
    tmp = fn.split('.')[0]
    
    if os.path.isfile(f'{outdir}/{tmp}.out'):
        return
    
    outfile = open(f'{outdir}/{tmp}.out', 'w')
    errfile = open(f'{outdir}/{tmp}.err', 'w')

    infile = open(f'{indir}/{fn}', 'r')
    seq = infile.readline().strip()
    infile.close()

    command = ['time', 'python2', '/MCTS-RNA/MCTS-RNA.py', '-s', seq]
    subprocess.run(command, stdout=outfile, stderr=errfile)
    
    outfile.close()
    errfile.close()

def run_rnainverse(indir, outdir, fn, repeats=1):
    tmp = fn.split('.')[0]
    
    if os.path.isfile(f'{outdir}/{tmp}.inv.out'):
        return
    
    outfile = open(f'{outdir}/{tmp}.inv.out', 'w')
    errfile = open(f'{outdir}/{tmp}.inv.err', 'w')

    infile = open(f'{indir}/{fn}', 'r')

    if repeats == 1:
        command = ['time', 'RNAinverse']
    else:
        command =  ['time', 'RNAinverse', f'-R{repeats}']
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

def run_rnaredprint(indir, outdir, fn, repeats=1):
    tmp = fn.split('.')[0]
    
    if os.path.isfile(f'{outdir}/{tmp}.out'):
        return
    
    outfile = open(f'{outdir}/{tmp}.out', 'w')
    errfile = open(f'{outdir}/{tmp}.err', 'w')

    infile = open(f'{indir}/{fn}', 'r')
    seq = infile.readline().strip()
    infile.close()

    command = ['time', '/RNARedPrint/_inst/bin/RNARedPrint', '--num', str(repeats), seq]
    subprocess.run(command, stdout=outfile, stderr=errfile)
    
    outfile.close()
    errfile.close()
    
def run_rnasfbinv(indir, outdir, fn, repeats=1):
    for num in range(repeats):
        tmp = fn.split('.')[0]
        
        if repeats > 1:
            tmp = f'{tmp}_{num}'
        
        if os.path.isfile(f'{outdir}/{tmp}.out'):
            continue
        
        outfile = open(f'{outdir}/{tmp}.out', 'w')
        errfile = open(f'{outdir}/{tmp}.err', 'w')

        command = ['time', 'python3', '/RNAsfbinv/RNAfbinvCL.py', '-f', f'{indir}/{fn}']
        subprocess.run(command, stdout=outfile, stderr=errfile)
        
        outfile.close()
        errfile.close()

ALGO = {'desirna': run_desirna, 'dss-opt': run_dss_opt, 'info-rna': run_info_rna, 'mcts-rna': run_mcts_rna, 'rnainverse': run_rnainverse, 'rnaredprint': run_rnaredprint, 'rnasfbinv': run_rnasfbinv}
DIRS = {'1':
       {'desirna': [('/rna_design/inputs/desirna', '/rna_design/outputs/desirna'), ('/rna_design/inputs/desirna_extended', '/rna_design/outputs/desirna_extended')],
        'dss-opt': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/dss-opt'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/dss-opt_extended')],
        'info-rna': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/info-rna'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/info-rna_extended')],
        'mcts-rna': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/mcts-rna'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/mcts-rna_extended')],
        'rnainverse': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/rnainverse'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/rnainverse_extended')],
        'rnaredprint': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/rnaredprint'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/rnaredprint_extended')],
        'rnasfbinv': [('/rna_design/inputs/rnasfbinv', '/rna_design/outputs/rnasfbinv'), ('/rna_design/inputs/rnasfbinv_extended', '/rna_design/outputs/rnasfbinv_extended')]},
        '2':
        {'desirna': [('/rna_design/inputs2/desirna', '/rna_design/outputs2/desirna')],
        'dss-opt': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/dss-opt')],
        'info-rna': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/info-rna')],
        'mcts-rna': '',
        'rnainverse': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/rnainverse')],
        'rnaredprint': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/rnaredprint')],
        'rnasfbinv': [('/rna_design/inputs2/rnasfbinv', '/rna_design/outputs2/rnasfbinv')]}
}

def main():
    if len(sys.argv) != 5:
        print('Usage: python3 run.py algoname start end dataset')
        exit()
    else: 
        run_algo = ALGO[sys.argv[1]]
        dirs = DIRS[sys.argv[4]][sys.argv[1]]
        range_s = int(sys.argv[1])
        range_e = int(sys.argv[2])
        repeats = 1 if sys.argv[4] == '1' else 10
    
    for indir, outdir in dirs:
        to_do = os.listdir(indir)
        to_do.sort()
        to_do = to_do[range_s:range_e]
        for fn in to_do:
            run_algo(indir, outdir, fn, repeats=repeats)
        
main()
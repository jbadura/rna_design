import os
import sys
from minineedle import needle
import subprocess

OUTDIR = '/rna_design/outputs2'

def get_needlewunsh_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        return 'NA'

    a = needle.NeedlemanWunsch(seq1, seq2)
    a.align()
    seq_score = a.get_score()
    return seq_score

def get_sequenceidentity_distance_1(seq1, seq2):
    if len(seq1) != len(seq2):
        return 'NA'

    return sum([a==b for a,b in zip(seq1, seq2)])/len(seq1)

def get_sequenceidentity_distance_2(seq1, seq2):
    if len(seq1) != len(seq2):
        return 'NA'
    return 'NA'
    LOOKUP = {'A': 1, 'U': 1, 'G': 2, 'C': 2, '?': 3}
    return sum([LOOKUP[a]==LOOKUP[b] for a,b in zip(seq1, seq2)])/len(seq1)

def get_rnapdist_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        return 'NA'

    tmp_f = open('tmp.in', 'w')
    tmp_f.write(f'{seq1}\n{seq2}')
    tmp_f.close()
    
    tmp_in = open('tmp.in', 'r')
    tmp_out = open('tmp.out', 'w')
    subprocess.run(['RNApdist'], stdout=tmp_out, stdin=tmp_in)
    tmp_in.close()
    tmp_out.close()
    
    tmp_f = open('tmp.out', 'r')
    line = tmp_f.readline()
    line = line.strip().split()
    return line[-1]

def get_rna_distance(str1, str2):
    if len(str1) != len(str2):
        return 'NA'

    tmp_f = open('tmp.in', 'w')
    tmp_f.write(f'{str1}\n{str2}')
    tmp_f.close()
    
    tmp_in = open('tmp.in', 'r')
    tmp_out = open('tmp.out', 'w')
    subprocess.run(['RNAdistance'], stdout=tmp_out, stdin=tmp_in)
    tmp_in.close()
    tmp_out.close()
    
    tmp_f = open('tmp.out', 'r')
    line = tmp_f.readline()
    line = line.strip().split()
    return line[-1]

def remove_pseudoknots(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)

def read_desirna(results):
    resdir = 'desirna'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''

            f = open(f'{OUTDIR}/{resdir}/{ID}_{i}.out', 'r')
            line = f.readline().strip()
            while not line.startswith('Closest solution:') and not line.startswith('Best solution:'):
                line = f.readline().strip()
                
            sequence = f.readline().strip()
            structure = f.readline().strip()
            
            f.close()
            results[resdir][ID].append((sequence, structure, f'{OUTDIR}/{resdir}/{ID}_{i}.out'))

def read_rnainverse(results): 
    resdir = 'rnainverse'
    results[resdir] = {}
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if not fn.endswith('.fold.out'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'{OUTDIR}/{resdir}/{fn}', 'r')
        
        for i in range(10):
            sequence = f.readline().strip()
            structure = f.readline().strip().split()[0]
            results[resdir][ID].append((sequence, structure, f'{OUTDIR}/{resdir}/{fn}'))
        f.close()

def read_rnaredprint(results):
    resdir = 'rnaredprint'
    results[resdir] = {}
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'{OUTDIR}/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        for i in range(10):
            sequence = f.readline().strip().split()[0]
            results[resdir][ID].append((sequence, structure, f'{OUTDIR}/{resdir}/{fn}'))
        f.close()

def read_rnasfbinv(results):
    resdir = 'rnasfbinv'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''
            f = open(f'{OUTDIR}/{resdir}/{ID}_{i}.out', 'r')
            
            f.readline()
            sequence = f.readline().strip()
            structure = f.readline().strip()
             
            f.close()
            results[resdir][ID].append((sequence, structure, f'{OUTDIR}/{resdir}/{ID}_{i}.out'))

def read_dss_opt(results):
    resdir = 'dss-opt'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''
            
            f = open(f'{OUTDIR}/{resdir}/{ID}_{i}.out', 'r')
            for l in f:
                l = l.strip()
                if l.startswith('vienna'):
                    structure = l.split()[-1]
                if l.startswith('seq'):
                    sequence = l.split()[-1]    
            f.close()
            results[resdir][ID].append((sequence, structure, f'{OUTDIR}/{resdir}/{ID}_{i}.out'))

def read_info_rna(results):
    resdir = 'info-rna'
    results[resdir] = {}
    for fn in os.listdir(f'{OUTDIR}/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'{OUTDIR}/{resdir}/{fn}', 'r')
        res_start = False
        for l in f:
            l = l.strip()
            if l.startswith('Local Search Results'):
                res_start = True
            if res_start:
                if l.startswith('MFE:'):    
                    sequence = l.split()[1]
                    results[resdir][ID].append((sequence, '', f'{OUTDIR}/{resdir}/{fn}'))     
        f.close()    

def check_missing(results, algo):
    f_mis = open(f'/rna_design/results2/missing_{algo}.txt', 'w')
    for k1 in results:
        for k2 in results[k1]:
            if len(results[k1][k2]) != 10:
                f_mis.write(f'Missing res for {k1} {k2}, no 10!\n')
            for sequence, structure in results[k1][k2]:
                if sequence == '' or structure == '':
                    f_mis.write(f'Missing res for {k1} {k2}\n')
    f_mis.close()

POSSIBLE_ALGOS = {'desirna': read_desirna, 'rnainverse': read_rnainverse, 'rnaredprint': read_rnaredprint, 'rnasfbinv': read_rnasfbinv, 'dss-opt': read_dss_opt, 'info-rna': read_info_rna}
def main():
    if len(sys.argv) != 2:
        print('Give algo name')
        exit()
    algo = sys.argv[1]
    if algo not in POSSIBLE_ALGOS:
        print('Wrong algo')
        print('Possible algos:', list(POSSIBLE_ALGOS.keys()))
        exit()

    try:
        os.mkdir('/rna_design/results2')
    except:
        pass
    
    results = {}
    POSSIBLE_ALGOS[algo](results)
    check_missing(results, algo)

    f_o = open(f'/rna_design/results2/results_{algo}.txt', 'w')
    to_write = ['ID', 'algo', 'sequence', 'structure', 'res_sequence', 'res_structure', 'rnapdist', 'seqidentity', 'rnadistance' ,'res_file', 'test_num']
    print(';'.join(to_write), file=f_o)

    for fn in os.listdir('/rna_design/data2'):
        f_list = open(f'/rna_design/data2/{fn}', 'r')
        fn_pref = fn.split('.')[0]
        i = 1
        for l in f_list:
            if l.startswith('Source'): continue
        
            l = l.strip().split(',')
            ID = f'{fn_pref}_{i}'
            if len(l) <= 4:
                print('Error in', fn)
                continue

            og_seq = l[1]
            og_str = remove_pseudoknots(l[3])
            
            i += 1

            for test_num in range(10):
                al_seq, al_str, res_file = results[algo][ID][test_num]
                    
                rnapdist = get_rnapdist_distance(og_seq, al_seq)
                rnadistance = get_rna_distance(og_str, al_str)
                seqidentity = get_sequenceidentity_distance_1(og_seq, al_seq)
                seqidentity2 = get_sequenceidentity_distance_2(og_seq, al_seq)
                
                to_write = [ID, algo, og_seq, og_str, al_seq, al_str, rnapdist, seqidentity, rnadistance, res_file, test_num]
                print(to_write, sep=';', file=f_o)

        f_list.close()
    f_o.close()

main()
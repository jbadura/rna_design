import os
import sys
from minineedle import needle
import subprocess

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
    for resdir in ['desirna', 'desirna_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if fn.endswith('.err'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')
            line = f.readline().strip()
            while not line.startswith('Closest solution:') and not line.startswith('Best solution:'):
                line = f.readline().strip()
                
            sequence = f.readline().strip()
            structure = f.readline().strip()
            
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')

def read_rnainverse(results): 
    for resdir in ['rnainverse', 'rnainverse_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if not fn.endswith('.fold.out'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')
            
            sequence = f.readline().strip()
            structure = f.readline().strip().split()[0]
            
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')

def read_rnaredprint(results):
    for resdir in ['rnaredprint', 'rnaredprint_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if fn.endswith('.err'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')
            
            structure = f.readline().strip()
            sequence = f.readline().strip().split()[0]
            
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')

def read_rnasfbinv(results):
    for resdir in ['rnasfbinv', 'rnasfbinv_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if fn.endswith('.err'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')
            
            f.readline()
            sequence = f.readline().strip()
            structure = f.readline().strip()
             
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')     

def read_dss_opt(results):
    for resdir in ['dss-opt', 'dss-opt_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if fn.endswith('.err'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')

            for l in f:
                l = l.strip()
                if l.startswith('vienna'):
                    structure = l.split()[-1]
                if l.startswith('seq'):
                    sequence = l.split()[-1]    
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')  

def read_info_rna(results):
    for resdir in ['info-rna', 'info-rna_extended']:
        results[resdir] = {}
        for fn in os.listdir(f'/rna_design/outputs/{resdir}'):
            if fn.endswith('.err'): continue
            sequence = ''
            structure = ''
            ID = fn.split('.')[0]
            f = open(f'/rna_design/outputs/{resdir}/{fn}', 'r')
            res_start = False
            for l in f:
                l = l.strip()
                if l.startswith('Local Search Results'):
                    res_start = True
                if res_start:
                    if l.startswith('MFE:'):    
                        sequence = l.split()[1]
                    if l.startswith('NO_MFE:'):
                        structure = l.split()[1]    
            f.close()
            results[resdir][ID] = (sequence, structure, f'/rna_design/outputs/{resdir}/{fn}')  

def check_missing(results, algo):
    f_mis = open(f'/rna_design/results/missing_{algo}.txt', 'w')
    for k1 in results:
        for k2 in results[k1]:
            if results[k1][k2][0] == '' or results[k1][k2][1] == '':
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
        os.mkdir('/rna_design/results')
    except:
        pass
     
    results = {}
    POSSIBLE_ALGOS[algo](results)
    check_missing(results, algo)
    
    f = open('/rna_design/data/loops_id.csv', 'r')
    f_o = open(f'/rna_design/results/results_{algo}.txt', 'w')
    f_o_ext = open(f'/rna_design/results/results_{algo}_ext.txt', 'w')

    to_write = ['ID', 'algo', 'type', 'sequence', 'structure', 'res_sequence', 'res_structure', 'rnapdist', 'seqidentity', 'rnadistance' ,'res_file', 'is_extended']
    print(';'.join(to_write), file=f_o)
    print(';'.join(to_write), file=f_o_ext)

    for l in f:
        l = l.strip().split(',')

        name = l[0]
        typee = l[1]

        if name == 'Source': continue
        ID = l[-1]

        og_seq = l[5]
        og_str = remove_pseudoknots(l[6])

        og_seq_ext = l[8]
        og_str_ext = remove_pseudoknots(l[9])

        if len(og_str_ext) > 100:
            continue

        al_seq, al_str, res_file = results[algo][ID]
        al_seq_ext, al_str_ext, res_file_ext = results[f'{algo}_extended'][ID]
         

        rnapdist = get_rnapdist_distance(og_seq, al_seq)
        rnadistance = get_rna_distance(og_str, al_str)
        seqidentity = get_sequenceidentity_distance_1(og_seq, al_seq)
        seqidentity2 = get_sequenceidentity_distance_2(og_seq, al_seq)
        
        rnapdist_ext = get_rnapdist_distance(og_seq_ext, al_seq_ext)
        rnadistance_ext = get_rna_distance(og_str_ext, al_str_ext)
        seqidentity_ext = get_sequenceidentity_distance_1(og_seq_ext, al_seq_ext)
        seqidentity2_ext = get_sequenceidentity_distance_2(og_seq_ext, al_seq_ext)

        to_write = [ID, algo, typee, og_seq, og_str, al_seq, al_str, rnapdist, seqidentity, rnadistance, res_file, 0]
        print(';'.join(to_write), file=f_o)
        to_write = [ID, algo, typee, og_seq_ext, og_str_ext, al_seq_ext, al_str_ext, rnapdist_ext, seqidentity_ext, rnadistance_ext, res_file_ext, 1]
        print(';'.join(to_write), file=f_o_ext)

    f.close()
    f_o.close()

main()
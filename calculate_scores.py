import sys
from minineedle import needle
import subprocess

def get_needlewunsh_distance(seq1, seq2):
    if seq1 == '' or seq2 == '':
        return 'NA'

    a = needle.NeedlemanWunsch(og_seq, al_seq)
    a.align()
    seq_score = a.get_score()
    return seq_score

def get_rna_distance(str1, str2):
    if str1 == '' or str2 == '':
        return 'NA'

    tmp_f = open('tmp.in', 'w')
    tmp_f.write(f'{og_str}\n{al_str}')
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

#ID;sequence;structure;sequence_extended;structure_extended;desirna;desirna_extended;dss-opt;dss-opt_extended;info-rna;info-rna_extended;rnainverse;rnainverse_extended;rnaredprint;rnaredprint_extended;rnasfbinv;rnasfbinv_extended
f = open('/rna_design/results/results.txt', 'r')
header = f.readline().strip().split(';')

if len(sys.argv) != 2:
    print('No algo name')
    exit()
algo = sys.argv[1]
if 'extended' in algo:
    print("Don't use extended in algo name")
    exit()
algo_i = -1
for i in range(len(header)):
    if algo == header[i].split('_')[0]:
        algo_i = i
        break
if algo_i == -1:
    print('No such algo')
    exit()
    
f_out = open(f'/rna_design/results/{algo}_res.txt', 'w')
    
for l in f:
    l = l.strip().split(';')
    
    ID = l[0]
    
    og_seq = l[1]
    og_str = l[2]
    al_seq = l[algo_i]
    al_str = l[algo_i+1]
    
    og_seq_ext = l[3]
    og_str_ext = l[4]
    al_seq_ext = l[algo_i+2]
    al_str_ext = l[algo_i+3]
    
    score_seq = get_needlewunsh_distance(og_seq, al_seq)
    score_str = get_rna_distance(og_str, al_str)
    
    score_seq_ext = get_needlewunsh_distance(og_seq_ext, al_seq_ext)
    score_str_ext = get_rna_distance(og_str_ext, al_str_ext)
    
    f_out.write(f'{ID};{og_seq};{og_str};{al_seq};{score_seq};{al_str};{score_str};{al_seq_ext};{score_seq_ext};{al_str_ext};{score_str_ext}\n')
    
f.close()
f_out.close()
    
    
    
    
    
    
    
    
    
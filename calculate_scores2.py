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

def main():
    f = open('/rna_design/results2/results.txt', 'r')
    header = f.readline().strip().split(';')        
    f_outs = {}
    for i in range(3, len(header)):
        algo = header[i].split('_')[0]
        if algo not in f_outs:
            f_outs[algo] = open(f'/rna_design/results2/{algo}_res.txt', 'w')
            to_write = ['ID', 'sequence', 'structure']
            for test in range(10):
                to_write.extend([f'{algo}_seqence', f'score_{algo}_seqence', f'{algo}_structure', f'score_{algo}_structure'])
            print(*to_write, file=f_outs[algo])
                
            
    
    for l in f:
        l = l.strip().split(';')
        
        ID = l[0]
        og_seq = l[1]
        og_str = l[2]
        
        i = 3
        for alg_num in range(6):
            algo = header[i].split('_')[0]
            to_write = [ID, og_seq, og_str]
            for test_num in range(10):
                al_seq = l[i]
                al_str = l[i+1]
                score_seq = get_rnapdist_distance(og_seq, al_seq)
                score_str = get_rna_distance(og_str, al_str)
                to_write.append(al_seq)
                to_write.append(score_seq)
                to_write.append(al_str)
                to_write.append(score_str)
            print(*to_write, file=f_outs[algo])
            i += 2
        
    f.close()
    for fo in f_outs.values():
        fo.close()
    
main()    

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

def main():
    for algo in ['desirna', 'rnainverse', 'rnaredprint', 'rnasfbinv', 'dss-opt', 'info-rna']:
        f = open('/rna_design/results/results.txt', 'r')
        header = f.readline().strip().split(';')

        algo_i = -1
        for i in range(len(header)):
            if algo == header[i].split('_')[0]:
                algo_i = i
                break
        if algo_i == -1:
            print('No such algo')
            exit()

        f_out = open(f'/rna_design/results/{algo}_res.txt', 'w')
        f_out.write(f'ID;sequence;structure;sequence_extended;structure_extended;')
        f_out.write(f'{algo}_seqence;rnapdist_{algo}_sequence;seqidentity_{algo}_sequence;seqidentity2_{algo}_sequence;{algo}_structure;rnadistance_{algo}_structure;')
        f_out.write(f'{algo}_seqence_extended;rnapdist_{algo}_sequence_extended;seqidentity_{algo}_sequence_extended;seqidentity2_{algo}_sequence_extended;{algo}_structure_extended;rnadistance_{algo}_structure_extended\n')

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

            print(algo, ID)

            rnapdist_seq = get_rnapdist_distance(og_seq, al_seq)
            rnadist_str = get_rna_distance(og_str, al_str)
            seqidentity = get_sequenceidentity_distance_1(og_seq, al_seq)
            seqidentity2 = get_sequenceidentity_distance_2(og_seq, al_seq)

            rnapdist_seq_ext = get_rnapdist_distance(og_seq_ext, al_seq_ext)
            rnadist_str_ext = get_rna_distance(og_str_ext, al_str_ext)
            seqidentity_ext = get_sequenceidentity_distance_1(og_seq_ext, al_seq_ext)
            seqidentity2_ext = get_sequenceidentity_distance_2(og_seq_ext, al_seq_ext)

            f_out.write(f'{ID};{og_seq};{og_str};{og_seq_ext};{og_str_ext};{al_seq};{rnapdist_seq};{seqidentity};{seqidentity2};{al_str};{rnadist_str};{al_seq_ext};{rnapdist_seq_ext};{seqidentity_ext};{seqidentity2_ext};{al_str_ext};{rnadist_str_ext}\n')

        f.close()
        f_out.close()

main()    

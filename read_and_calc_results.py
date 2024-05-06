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
    if str1 == 'no_structure' or str2 == 'no_structure':
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
    try:
        return line[-1]
    except:
        print(str1)
        print(str2)
        print(line)
        print('-----')
        exit()

def remove_pseudoknots(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)

#outdir is in docker, i.e /rna_design/outputs_suffix
#algodir is relative, i.e 'desirna'
def read_dir(results, outdir, algodir):
    results[algodir] = {}
    for fn in os.listdir(f'{outdir}/{algodir}'):
        ID = fn.split('.')[0]
        if fn.endswith('.timeouted'):
            results[algodir][ID] = ('TIMEOUTED', 'TIMEOUTED', 'TIMEOUTED', 'TIMEOUTED', f'{outdir}/{algodir}/{fn}')
        elif fn.endswith('.rte'):
            results[algodir][ID] = ('RTE', 'RTE', 'RTE', 'RTE', f'{outdir}/{algodir}/{fn}')
        elif fn.endswith('.parsed.out'):
            f = open(f'{outdir}/{algodir}/{fn}', 'r')
            sequence = f.readline().strip().split('=')[1]
            structure = f.readline().strip().split('=')[1]
            rnafold = f.readline().strip().split('=')[1]
            f.close()
            if sequence == 'no_sequence':
                results[algodir][ID] = ('TIMEOUTED2', 'TIMEOUTED2', 'TIMEOUTED2', 'TIMEOUTED2', f'{outdir}/{algodir}/{fn}')
            else:
                f = open(f'{outdir}/{algodir}/{ID}.err', 'r')
                time = -1
                try:
                    for timeline in f:
                        if 'user' in timeline and 'system' in timeline and 'elapsed' in timeline:
                            time = float(timeline.strip().split()[0][:-4])
                except:
                    print('WRONG TIME')
                    print(f'{outdir}/{algodir}/{ID}.err')
                    exit()
                f.close()
                results[algodir][ID] = (sequence, structure, rnafold, time, f'{outdir}/{algodir}/{fn}')


POSSIBLE_ALGOS = {'desirna', 'rnainverse', 'rnaredprint', 'rnasfbinv', 'dss-opt', 'info-rna'}
def main():
    if len(sys.argv) != 3:
        print('Usage: python3 read_and_calc_results.py algo_name dataset')
        exit()
    algo = sys.argv[1]
    if algo not in POSSIBLE_ALGOS:
        print('Wrong algo')
        print('Possible algos:', list(POSSIBLE_ALGOS))
        exit()
    dataset = sys.argv[2]
    if dataset.endswith('/'):
        dataset = dataset[:-1]
    if dataset.startswith('inputs_'):
        dataset = dataset[7:]
    if dataset.startswith('outputs_'):
        dataset = dataset[8:]

    if 'rfam' in dataset:
        shift = 1
    else:
        shift = 0

    # outdir - dir with algo outputs
    # resdir - dir to save parsed data to
    outdir = f'/rna_design/outputs_{dataset}'
    resdir = f'/rna_design/results_{dataset}'
    try:
        os.mkdir(resdir)
    except:
        pass

    results = {}    
    read_dir(results, outdir, algo)
    read_dir(results, outdir, f'{algo}_extended')

    csv_file = open(f'/rna_design/data/{dataset}.csv', 'r')
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    f_o = open(f'{resdir}/results_{algo}.txt', 'w')
    f_o_ext = open(f'{resdir}/results_{algo}_extended.txt', 'w')

    to_write = ['ID', 'algo', 'type', 'sequence', 'structure', 'res_sequence', 'res_structure', 'res_rnafold', 'rnapdist', 'seqidentity', 'rnadistance', 'rnadistance2rnafold' ,'res_file', 'is_extended', 'time']
    print(';'.join(to_write), file=f_o)
    print(';'.join(to_write), file=f_o_ext)

    for l in csv_reader:

        name = l[0]
        typee = l[1+shift]

        if name == 'Source' or name == 'Family':
            if l[-1] != 'id':
                print('Last column of provided file must be "id"')
                exit(0)
            continue
        ID = l[-1]

        og_seq = l[5+shift]
        og_str = remove_pseudoknots(l[6+shift])

        og_seq_ext = l[8+shift]
        og_str_ext = remove_pseudoknots(l[9+shift])

        #if len(og_str_ext) > 100:
        #    continue

        al_seq, al_str, rnafold_str, time, res_file = results[algo][ID]
        al_seq_ext, al_str_ext, rnafold_str_ext, time_ext, res_file_ext = results[f'{algo}_extended'][ID]

    
        if al_seq not in ['TIMEOUTED', 'TIMEOUTED2', 'RTE']:
            rnapdist = get_rnapdist_distance(og_seq, al_seq)
            seqidentity = get_sequenceidentity_distance_1(og_seq, al_seq)
            rnadistance = get_rna_distance(og_str, al_str)
            rnadistance2rnafold = get_rna_distance(og_str, rnafold_str)
        else:
            rnapdist = 0
            seqidentity = 0
            rnadistance = 0
            rnadistance2rnafold = 0
        
        if al_seq not in ['TIMEOUTED', 'TIMEOUTED2', 'RTE']:
            rnapdist_ext = get_rnapdist_distance(og_seq_ext, al_seq_ext)
            seqidentity_ext = get_sequenceidentity_distance_1(og_seq_ext, al_seq_ext)
            rnadistance_ext = get_rna_distance(og_str_ext, al_str_ext)
            rnadistance2rnafold_ext = get_rna_distance(og_str_ext, rnafold_str_ext)
        else:
            rnapdist_ext = 0
            seqidentity_ext = 0
            rnadistance_ext = 0
            rnadistance2rnafold_ext = 0

        to_write = [ID, algo, typee, og_seq, og_str, al_seq, al_str, rnafold_str, rnapdist, seqidentity, rnadistance, rnadistance2rnafold, res_file, 0, time]
        print(';'.join([str(x) for x in to_write]), file=f_o)
        to_write = [ID, algo, typee, og_seq_ext, og_str_ext, al_seq_ext, al_str_ext, rnafold_str_ext, rnapdist_ext, seqidentity_ext, rnadistance_ext, rnadistance2rnafold_ext, res_file_ext, 1, time_ext]
        print(';'.join([str(x) for x in to_write]), file=f_o_ext)

    f.close()
    f_o.close()

main()
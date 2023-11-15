from matplotlib import pyplot as plt
import seaborn as sns
import os

def try_append(l, f):
    try:
        l.append(float(f))
    except:
        pass


#ID;sequence;structure;sequence_extended;structure_extended;desirna_seqence;rnapdist_desirna_sequence;seqidentity_desirna_sequence;seqidentity2_desirna_sequence;desirna_structure;rnadistance_desirna_structure;desirna_seqence_extended;rnapdist_desirna_sequence_extended;seqidentity_desirna_sequence_extended;seqidentity2_desirna_sequence_extended;desirna_structure_extended;rnadistance_desirna_structure_extended
#0  1        2         3                 4                  5               6                         7                            8                              9                10                            11                       12                                 13                                    14                                     15                         16
def main():
    f_out = open(f'results/plot_data.csv', 'w')
    f_out_ext = open(f'results/plot_data_ext.csv', 'w')
    for fn in os.listdir('results'):
        if '_res.' not in fn: continue        
        algo = fn.split('_')[0]
        f = open(f'results/{fn}', 'r')
        header = f.readline().strip().split(';')

        for l in f:
            l = l.strip().split(';')
            rnapdist = 
            try_append(res['rnapdist'], l[6])
            try_append(res['seqidentity'], l[7])
            try_append(res['rnadistance'], l[10])

            try_append(res['rnapdist_extended'], l[12])
            try_append(res['seqidentity_extended'], l[13])
            try_append(res['rnadistance_extended'],l[16])
            
            print(f'{ID};{algo};{rnapdist};{seqidentity};{rnadistance}', stdout=g_out)
            print(f'{ID};{algo};{rnapdist};{seqidentity};{rnadistance', stdout=f_out_ext)

main()
 
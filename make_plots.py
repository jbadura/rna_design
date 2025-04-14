from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import os
import csv
import sys

####### PLOT PARAMS #######
plt.rcParams['figure.figsize'] = [8, 8]

ALGO_NAMES = {'rnainverse': 'RNAinverse', 'info-rna': 'INFO-RNA', 'dss-opt': 'DSS-Opt',
              'rnasfbinv': 'RNAfbinv', 'rnaredprint': 'RNARedPrint', 'desirna': 'DesiRNA',
              'algo': 'Algorithm', 'learna': 'LRNA', 'metalearna': 'MLRNA',
              'metalearnaadapt': 'MLRNAA', 'rnaredprint_calcprobs': 'calcprobs_psum',
              'rnaredprint_designmultistate': 'multistate', 'rnaredprint_calcprobs_mfe_only': 'calcprobs_mfe'}

ALGOS = ['RNAinverse', 'RNAfbinv', 'INFO-RNA', 'RNARedPrint', 'DSS-Opt', 'DesiRNA', 'LRNA', 'MLRNA', 'MLRNAA', 'calcprobs_psum', 'multistate', 'calcprobs_mfe']
ALGO_ORDER = ['DesiRNA', 'RNAinverse', 'DSS-Opt', 'INFO-RNA', 'RNAfbinv', 'RNARedPrint', 'LRNA', 'MLRNA', 'MLRNAA', 'calcprobs_psum', 'multistate', 'calcprobs_mfe']


MY_PAL = {'RNAinverse': 'g', 'RNAfbinv': 'b', 'INFO-RNA': 'm',
          'RNARedPrint': 'r', 'DSS-Opt': 'y', 'DesiRNA': 'c', 
          'LRNA': 'g', 'MLRNA': 'g', 'MLRNAA': 'g',
          'calcprobs': 'g', 'multistate': 'g', 'calcprobs_mfe': 'g'}
##### END PLOT PARAMS #####

def rename(main_dataset):
    f_in = open(f"results_{main_dataset}/plots_data.csv", 'r')
    f_out = open(f"results_{main_dataset}/plots_data_renamed.csv", 'w')
    first_line = True
    for l in f_in:
        l = l.strip().split(';')
        l.append(ALGO_NAMES[l[1]])
        if first_line:
            l[9] = 'Sequence Identity'
            l[8] = 'RNApdist'
            l[11] = 'RNAdistance'
            l.append('len')
            first_line = False
        else:
            l.append(len(l[3]))
        print(*l, sep=';', file=f_out)
    f_in.close()
    f_out.close()


def is_nopk(s):
    for c in s:
        if c not in '.()-':
            return False
    return True


def get_nopk(main_dataset):
    if 'rfam' in main_dataset:
        shift = 1
    else:
        shift = 0
    
    nopk = set()
    csv_file = open(f'data/{main_dataset}.csv', 'r')
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for l in csv_reader:
        if l[-1] == 'id': continue
        s_pattern = l[3+shift]
        if is_nopk(s_pattern):
            nopk.add(int(l[-1]))
    csv_file.close()
    return nopk

# dataset in {all, all_nopk, intersection, intersection_nopk}
# part in {all, interloops, others}
def draw_plots(df, dataset, part, is_extended, main_dataset):
    suffix = '_extended' if is_extended else ''

    if not os.path.exists(f'plots_{main_dataset}/{dataset}'):
        os.mkdir(f'plots_{main_dataset}/{dataset}')
    # if not os.path.exists(f'plots_{main_dataset}/{dataset}/separated'):
    #     os.mkdir(f'plots_{main_dataset}/{dataset}/separated')

    for yax in ['Sequence Identity', 'RNApdist', 'RNAdistance', 'Normalized RNAdistance', 'f1score2rnafold']:
        fig, ax = plt.subplots()
        sns.violinplot(data=df, y=yax, x="Algorithm", ax=ax, palette=MY_PAL, hue="Algorithm", legend=False, order=ALGO_ORDER)
        if yax != 'Sequence Identity':
            ax.set_ylabel(f'{yax} (less is better)')
        fig.savefig(f'plots_{main_dataset}/{dataset}/{part}_{yax}{suffix}.pdf', dpi=600)
        plt.close(fig)

    # for yax in ['Sequence Identity', 'RNApdist', 'RNAdistance']:
    #     for algo in algos:
    #         fig, ax = plt.subplots()
    #         tmp_df = df[df['Algorithm'] == algo]
    #         sns.violinplot(data=tmp_df, y=yax, x="Algorithm", ax=ax)
    #         fig.savefig(f'plots/{dataset}/separated/{part}_{yax}_{algo}{suffix}.pdf', dpi=600)
    #         plt.close(fig)

    stats = open(f'plots_{main_dataset}/{dataset}/{part}{suffix}.stats', 'w')

    line = ['Algorithm', '#solved', 'Tot. time', 'Avg. time']
    for stat in ['Sequence Identity', 'RNApdist', 'RNAdistance', 'Normalized RNAdistance', 'f1score2rnafold']:
        for tmp_name in ['Min', 'Max', 'Avg.', 'Median']:
            line.append(f'{stat} - {tmp_name}')
    print(*line, sep='\t', file=stats)

    line = []
    for algo in ALGOS:
        tmp_data = df[df['Algorithm'] == algo]
        size = len(tmp_data)
        tot_time = pd.to_numeric(tmp_data['time']).sum()
        if size == 0:
            avg_time = 0
        else:
            avg_time = tot_time / size
        line = [algo, size, f'{tot_time:.2f}', f'{avg_time:.2f}']

        for stat in ['Sequence Identity', 'RNApdist', 'RNAdistance', 'Normalized RNAdistance', 'f1score2rnafold']:
            line.append(f'{pd.to_numeric(tmp_data[stat]).min():.2f}')
            line.append(f'{pd.to_numeric(tmp_data[stat]).max():.2f}')
            line.append(f'{pd.to_numeric(tmp_data[stat]).mean():.2f}')
            line.append(f'{pd.to_numeric(tmp_data[stat]).median():.2f}')

        print(*line, sep='\t', file=stats)
    stats.close()

def main():
    main_dataset = sys.argv[1]
    if not os.path.exists(f'plots_{main_dataset}'):
        os.mkdir(f'plots_{main_dataset}')
    rename(main_dataset)
    data = pd.read_csv(f"results_{main_dataset}/plots_data_renamed.csv", sep=';')
    nopk = get_nopk(main_dataset)

    # data = data[data['Algorithm'] != 'RNAfbinv']
    # ALGOS.remove('RNAfbinv')
    # ALGO_ORDER.remove('RNAfbinv')

    for is_extended in [0, 1]:
        filtered = data[data['is_extended'] == is_extended]
        filtered = filtered[filtered['res_sequence'] != 'TIMEOUTED']
        filtered = filtered[filtered['res_sequence'] != 'TIMEOUTED2']
        _all = filtered[filtered['res_sequence'] != 'RTE']

        _all['Normalized RNAdistance'] = _all['RNAdistance'] / _all['len']
        print(_all)

        draw_plots(_all, 'all', 'all', is_extended, main_dataset)
        internalloop = _all[_all['type'] == 'Internal loop']
        draw_plots(internalloop, 'all', 'interloops', is_extended, main_dataset)
        other = _all[_all['type'] != 'Internal loop']
        draw_plots(other, 'all', 'others', is_extended, main_dataset)
        junk3 = _all[_all['type'] == '3-way junction']
        draw_plots(junk3, 'all', '3wayjunk', is_extended, main_dataset)
        junk4 = _all[_all['type'] == '4-way junction']
        draw_plots(junk4, 'all', '4wayjunk', is_extended, main_dataset)

        _all_nopk = _all[_all['ID'].isin(nopk)]
        draw_plots(_all_nopk, 'all_nopk', 'all', is_extended, main_dataset)
        internalloop = _all_nopk[_all_nopk['type'] == 'Internal loop']
        draw_plots(internalloop, 'all_nopk', 'interloops', is_extended, main_dataset)
        other = _all_nopk[_all_nopk['type'] != 'Internal loop']
        draw_plots(other, 'all_nopk', 'others', is_extended, main_dataset)
        junk3 = _all_nopk[_all_nopk['type'] == '3-way junction']
        draw_plots(junk3, 'all_nopk', '3wayjunk', is_extended, main_dataset)
        junk4 = _all_nopk[_all_nopk['type'] == '4-way junction']
        draw_plots(junk4, 'all_nopk', '4wayjunk', is_extended, main_dataset)

        common_ids = set()
        for algo in ALGOS:
            tmp_data = _all[_all['Algorithm'] == algo]
            if len(common_ids) == 0:
                common_ids = set(tmp_data['ID'])
            else:
                common_ids = common_ids & set(tmp_data['ID'])

        intersection = _all[_all['ID'].isin(common_ids)]
        draw_plots(intersection, 'intersection', 'all', is_extended, main_dataset)
        internalloop = intersection[intersection['type'] == 'Internal loop']
        draw_plots(internalloop, 'intersection', 'interloops', is_extended, main_dataset)
        other = intersection[intersection['type'] != 'Internal loop']
        draw_plots(other, 'intersection', 'others', is_extended, main_dataset)
        junk3 = intersection[intersection['type'] == '3-way junction']
        draw_plots(junk3, 'intersection', '3wayjunk', is_extended, main_dataset)
        junk4 = intersection[intersection['type'] == '4-way junction']
        draw_plots(junk4, 'intersection', '4wayjunk', is_extended, main_dataset)

        intersection_nopk = intersection[intersection['ID'].isin(nopk)]
        draw_plots(intersection_nopk, 'intersection_nopk', 'all', is_extended, main_dataset)
        internalloop = intersection_nopk[intersection_nopk['type'] == 'Internal loop']
        draw_plots(internalloop, 'intersection_nopk', 'interloops', is_extended, main_dataset)
        other = intersection_nopk[intersection_nopk['type'] != 'Internal loop']
        draw_plots(other, 'intersection_nopk', 'others', is_extended, main_dataset)
        junk3 = intersection_nopk[intersection_nopk['type'] == '3-way junction']
        draw_plots(junk3, 'intersection_nopk', '3wayjunk', is_extended, main_dataset)
        junk4 = intersection_nopk[intersection_nopk['type'] == '4-way junction']
        draw_plots(junk4, 'intersection_nopk', '4wayjunk', is_extended, main_dataset)


main()
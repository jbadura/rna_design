from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import os
plt.rcParams['figure.figsize'] = [8, 8]

algo_names = {'rnainverse': 'RNAinverse', 'info-rna': 'INFO-RNA', 'dss-opt': 'DSS-Opt',
              'rnasfbinv': 'RNAfbinv', 'rnaredprint': 'RNARedPrint', 'desirna': 'DesiRNA',
              'algo': 'Algorithm'}

algos = ['RNAinverse', 'RNAfbinv', 'INFO-RNA', 'RNARedPrint', 'DSS-Opt', 'DesiRNA']


def rename():
    f_in = open("results/plots_data.csv", 'r')
    f_out = open("results/plots_data_renamed.csv", 'w')
    first_line = True
    for l in f_in:
        l = l.strip().split(';')
        l.append(algo_names[l[1]])
        if first_line:
            l[9] = 'Sequence Identity'
            l[8] = 'RNApdist'
            l[11] = 'RNAdistance'
            first_line = False
        print(*l, sep=';', file=f_out)
    f_in.close()
    f_out.close()


def get_nopk():
    f = open('data/loops_id_nopk.csv', 'r')
    nopk = set()
    for line in f:
        line = line.strip().split(',')
        if line[-1] == 'id': continue
        ID = int(line[-1])
        nopk.add(ID)
    f.close()
    return nopk


# dataset in {all, all_nopk, intersection, intersection_nopk}
# part in {all, interloops, others}
def draw_plots(df, dataset, part, is_extended):
    suffix = '_extended' if is_extended else ''

    if not os.path.exists(f'plots/{dataset}'):
        os.mkdir(f'plots/{dataset}')

    for yax in ['Sequence Identity', 'RNApdist', 'RNAdistance']:
        fig, ax = plt.subplots()
        sns.violinplot(data=df, y=yax, x="Algorithm", ax=ax)
        fig.savefig(f'plots/{dataset}/{part}_{yax}{suffix}.pdf', dpi=600)
        plt.close(fig)

    for yax in ['Sequence Identity', 'RNApdist', 'RNAdistance']:
        for algo in algos:
            fig, ax = plt.subplots()
            tmp_df = df[df['Algorithm'] == algo]
            sns.violinplot(data=tmp_df, y=yax, x="Algorithm", ax=ax)
            fig.savefig(f'plots/{dataset}/{part}_{yax}_{algo}{suffix}.pdf', dpi=600)
            plt.close(fig)

    stats = open(f'plots/{dataset}/{part}{suffix}.stats', 'w')
    print('Algorithm', '#solved', 'Tot. time', 'Avg. time', sep='\t', file=stats)
    for algo in algos:
        tmp_data = df[df['Algorithm'] == algo]
        size = len(tmp_data)
        tot_time = pd.to_numeric(tmp_data['time']).sum()
        avg_time = tot_time / size
        print(f'{algo}\t{size}\t{tot_time:.2f}\t{avg_time:.2f}', file=stats)
    stats.close()


rename()
data = pd.read_csv("results/plots_data_renamed.csv", sep=';')
nopk = get_nopk()

for is_extended in [0, 1]:
    filtered = data[data['is_extended'] == is_extended]
    filtered = filtered[filtered['res_sequence'] != 'TIMEOUTED']
    filtered = filtered[filtered['res_sequence'] != 'TIMEOUTED2']
    _all = filtered[filtered['res_sequence'] != 'RTE']

    draw_plots(_all, 'all', 'all', is_extended)
    internalloop = _all[_all['type'] == 'Internal loop']
    draw_plots(internalloop, 'all', 'interloops', is_extended)
    other = _all[_all['type'] != 'Internal loop']
    draw_plots(other, 'all', 'others', is_extended)

    _all_nopk = _all[_all['ID'].isin(nopk)]
    draw_plots(_all_nopk, 'all_nopk', 'all', is_extended)
    internalloop = _all_nopk[_all_nopk['type'] == 'Internal loop']
    draw_plots(internalloop, 'all_nopk', 'interloops', is_extended)
    other = _all_nopk[_all_nopk['type'] != 'Internal loop']
    draw_plots(other, 'all_nopk', 'others', is_extended)

    common_ids = set()
    for algo in algos:
        tmp_data = filtered[filtered['Algorithm'] == algo]
        if len(common_ids) == 0:
            common_ids = set(tmp_data['ID'])
        else:
            common_ids = common_ids & set(tmp_data['ID'])

    intersection = _all[_all['ID'].isin(common_ids)]
    draw_plots(intersection, 'intersection', 'all', is_extended)
    internalloop = intersection[intersection['type'] == 'Internal loop']
    draw_plots(internalloop, 'intersection', 'interloops', is_extended)
    other = intersection[intersection['type'] != 'Internal loop']
    draw_plots(other, 'intersection', 'others', is_extended)

    intersection_nopk = intersection[intersection['ID'].isin(nopk)]
    draw_plots(intersection_nopk, 'intersection_nopk', 'all', is_extended)
    internalloop = intersection_nopk[intersection_nopk['type'] == 'Internal loop']
    draw_plots(internalloop, 'intersection_nopk', 'interloops', is_extended)
    other = intersection_nopk[intersection_nopk['type'] != 'Internal loop']
    draw_plots(other, 'intersection_nopk', 'others', is_extended)

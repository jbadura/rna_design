import os
import sys

def mkdir(d):
    try:
        os.mkdir(d)
    except:
        pass


mkdir('outputs2')
mkdir('inputs2')
for s in ['inputs2', 'outputs2']:
    mkdir(f'{s}/desirna/')
    mkdir(f'{s}/rnainverse/')
    mkdir(f'{s}/rnasfbinv/')
mkdir(f'outputs2/rnaredprint/')
mkdir(f'outputs2/info-rna/')
mkdir(f'outputs2/dss-opt/')


def remove_junk(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)


for fn in os.listdir('data2'):
    f_list = open(f'data2/{fn}', 'r')
    fn_pref = fn.split('.')[0]
    i = 1
    for l in f_list:
        if l.startswith('Source'): continue
    
        l = l.strip().split(',')
        ID = f'{fn_pref}_{i}'
        if len(l) <= 4:
            print('Error in', fn)
            continue
        fragment_structure = l[3]
        fragment_structure_mod = remove_junk(fragment_structure)
        NNN = 'N' * len(fragment_structure)
        
        i += 1
    
        ##### RNA inverse (also used for RNARedPrint, dss-opt, and info-rna) #####
        f = open(f'inputs2/rnainverse/{ID}.in', 'w')
        f.write(f'{fragment_structure_mod}\n')
        f.write(f'{NNN}\n')
        f.close()

        ##### RNA sfbinv #####
        f = open(f'inputs2/rnasfbinv/{ID}.in', 'w')
        f.write(f'TARGET_STRUCTURE={fragment_structure_mod}\n')
        f.write(f'TARGET_SEQUENCE={NNN}\n')
        f.close()

        ##### Desi RNA #####
        f = open(f'inputs2/desirna/{ID}.in', 'w')
        f.write('>name\n')
        f.write(f'name_{ID}\n')
        f.write('>seq_restr\n')
        f.write(f'{NNN}\n')
        f.write('>sec_struct\n')
        f.write(f'{fragment_structure_mod}\n')
        f.close()
    f_list.close()

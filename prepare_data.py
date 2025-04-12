import os
import sys
import csv


def mkdir(d):
    try:
        os.mkdir(d)
    except:
        pass


def remove_pseudoknots(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)

if len(sys.argv) == 2:
    file_name = sys.argv[1]
    if file_name.endswith('.csv'):
        file_name = file_name[:-4]
    if '/' in file_name:
        file_name = file_name.split('/')[-1]
    suff = f'_{file_name}'
else:
    print('Provide file name from "data" dir.')

INPUTS = f'inputs{suff}'
OUTPUTS = f'outputs{suff}'

mkdir(OUTPUTS)
mkdir(INPUTS)
for s in [INPUTS, OUTPUTS]:
    mkdir(f'{s}/desirna/')
    mkdir(f'{s}/desirna_extended/')
    mkdir(f'{s}/rnainverse/')
    mkdir(f'{s}/rnainverse_extended/')
    mkdir(f'{s}/rnasfbinv/')
    mkdir(f'{s}/rnasfbinv_extended/')
    mkdir(f'{s}/ribologic/')
    mkdir(f'{s}/ribologic_extended/')
    mkdir(f'{s}/learna/')
    mkdir(f'{s}/learna_extended/')

mkdir(f'{OUTPUTS}/rnaredprint/')
mkdir(f'{OUTPUTS}/rnaredprint_extended/')
mkdir(f'{OUTPUTS}/rnaredprint_designmultistate/')
mkdir(f'{OUTPUTS}/rnaredprint_designmultistate_extended/')
mkdir(f'{OUTPUTS}/rnaredprint_calcprobs/')
mkdir(f'{OUTPUTS}/rnaredprint_calcprobs_extended/')
mkdir(f'{OUTPUTS}/info-rna/')
mkdir(f'{OUTPUTS}/info-rna_extended/')
mkdir(f'{OUTPUTS}/dss-opt/')
mkdir(f'{OUTPUTS}/dss-opt_extended/')
mkdir(f'{OUTPUTS}/metalearna')
mkdir(f'{OUTPUTS}/metalearna_extended')
mkdir(f'{OUTPUTS}/metalearnaadapt')
mkdir(f'{OUTPUTS}/metalearnaadapt_extended')

csv_file = open(f'data/{file_name}.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

if 'rfam' in file_name:
    shift = 1
else:
    shift = 0

for l in csv_reader:

    name = l[0]

    if name == 'Source' or name == 'Family':
        if l[-1] != 'id':
            print('Last column of provided file must be "id"')
            exit(0)
        continue
    ID = int(l[-1])

    fragment_structure = l[6+shift]
    fragment_structure_mod = remove_pseudoknots(fragment_structure)
    NNN = 'N' * len(fragment_structure)
    
    fragment_structure_ext = l[9+shift]
    fragment_structure_ext_mod = remove_pseudoknots(fragment_structure_ext)
    NNN_ext = 'N' * len(fragment_structure_ext)

    ##### RNA inverse (also used for RNARedPrint, dss-opt, and info-rna) #####
    f = open(f'{INPUTS}/rnainverse/{ID}.in', 'w')
    f.write(f'{fragment_structure_mod}\n')
    f.write(f'{NNN}\n')
    f.close()

    f = open(f'{INPUTS}/rnainverse_extended/{ID}.in', 'w')
    f.write(f'{fragment_structure_ext_mod}\n')
    f.write(f'{NNN_ext}\n')
    f.close()

    ##### RNA sfbinv #####
    f = open(f'{INPUTS}/rnasfbinv/{ID}.in', 'w')
    f.write(f'TARGET_STRUCTURE={fragment_structure_mod}\n')
    f.write(f'TARGET_SEQUENCE={NNN}\n')
    f.close()

    f = open(f'{INPUTS}/rnasfbinv_extended/{ID}.in', 'w')
    f.write(f'TARGET_STRUCTURE={fragment_structure_ext_mod}\n')
    f.write(f'TARGET_SEQUENCE={NNN_ext}\n')
    f.close()

    ##### Desi RNA #####
    f = open(f'{INPUTS}/desirna/{ID}.in', 'w')
    f.write('>name\n')
    f.write(f'name_{ID}\n')
    f.write('>seq_restr\n')
    f.write(f'{NNN}\n')
    f.write('>sec_struct\n')
    f.write(f'{fragment_structure_mod}\n')
    f.close()

    f = open(f'{INPUTS}/desirna_extended/{ID}.in', 'w')
    f.write('>name\n')
    f.write(f'name_{ID}\n')
    f.write('>seq_restr\n')
    f.write(f'{NNN_ext}\n')
    f.write('>sec_struct\n')
    f.write(f'{fragment_structure_ext_mod}\n')
    f.close()
    
    ##### RiboLogic #####
    f = open(f'{INPUTS}/ribologic/{ID}.in', 'w')
    f.write(f'-sequence\n')
    f.write(f'{NNN}\n')
    f.write('>single\n')
    f.write(f'{fragment_structure_mod}\n')
    xxx = 'x' * len(NNN)
    f.write(f'{xxx}\n')
    f.close()
    
    f = open(f'{INPUTS}/ribologic_extended/{ID}.in', 'w')
    f.write(f'-sequence\n')
    f.write(f'{NNN_ext}\n')
    f.write('>single\n')
    f.write(f'{fragment_structure_ext_mod}\n')
    xxx = 'x' * len(NNN_ext)
    f.write(f'{xxx}\n')
    f.close()
    
    ##### LeaRNA #####
    f = open(f'{INPUTS}/learna/{ID}.in', 'w')
    f.write(f'{fragment_structure_mod}\n')
    f.close()
    
    f = open(f'{INPUTS}/learna_extended//{ID}.in', 'w')
    f.write(f'{fragment_structure_ext_mod}\n')
    f.close()
    

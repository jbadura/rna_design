import os
import sys

def mkdir(d):
    try:
        os.mkdir(d)
    except:
        pass


mkdir('outputs')
mkdir('inputs')
for s in ['inputs', 'outputs']:
    mkdir(f'{s}/desirna/')
    mkdir(f'{s}/desirna_extended/')
    mkdir(f'{s}/rnainverse/')
    mkdir(f'{s}/rnainverse_extended/')
    mkdir(f'{s}/rnasfbinv/')
    mkdir(f'{s}/rnasfbinv_extended/')


def remove_junk(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)


f = open('data/loops_id.csv', 'r')

for l in f:
    l = l.strip().split(',')
    
    name = l[0]
    
    if name == 'Source': continue
    ID = int(l[-1])
    
    fragment_structure = l[6]
    fragment_structure_mod = remove_junk(fragment_structure)
    NNN = 'N' * len(fragment_structure)
    
    fragment_structure_ext = l[9]
    fragment_structure_ext_mod = remove_junk(fragment_structure_ext)
    NNN_ext = 'N' * len(fragment_structure_ext)
          
    if len(fragment_structure_ext) > 100:
        continue
    
    ##### RNA inverse #####
    f = open(f'inputs/rnainverse/{ID}.in', 'w')
    f.write(f'{fragment_structure_mod}\n')
    f.write(f'{NNN}\n')
    f.close()
    
    f = open(f'inputs/rnainverse_extended/{ID}.in', 'w')
    f.write(f'{fragment_structure_ext_mod}\n')
    f.write(f'{NNN_ext}\n')
    f.close()
    
    ##### RNA sfbinv #####
    f = open(f'inputs/rnasfbinv/{ID}.in', 'w')
    f.write(f'TARGET_STRUCTURE={fragment_structure_mod}\n')
    f.write(f'TARGET_SEQUENCE={NNN}\n')
    f.close()
    

    f = open(f'inputs/rnasfbinv_extended/{ID}.in', 'w')
    f.write(f'TARGET_STRUCTURE={fragment_structure_ext_mod}\n')
    f.write(f'TARGET_SEQUENCE={NNN_ext}\n')
    f.close()
    
    ##### Desi RNA #####
    f = open(f'inputs/desirna/{ID}.in', 'w')
    f.write('>name\n')
    f.write(f'name_{ID}\n')
    f.write('>seq_restr\n')
    f.write(f'{NNN}\n')
    f.write('>sec_struct\n')
    f.write(f'{fragment_structure_mod}\n')
    f.close()
    
    f = open(f'inputs/desirna_extended/{ID}.in', 'w')
    f.write('>name\n')
    f.write(f'name_{ID}\n')
    f.write('>seq_restr\n')
    f.write(f'{NNN_ext}\n')
    f.write('>sec_struct\n')
    f.write(f'{fragment_structure_ext_mod}\n')
    f.close()
    
import os
import sys

def remove_junk(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)

results = {}


for resdir in ['desirna', 'desirna_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        line = f.readline().strip()
        while not line.startswith('Closest solution:') and not line.startswith('Best solution:'):
            line = f.readline().strip()
            
        sequence = f.readline().strip()
        structure = f.readline().strip()
        
        f.close()
        results[resdir][ID] = (sequence, structure)
print('Done desirna')    
        
for resdir in ['rnainverse', 'rnainverse_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if not fn.endswith('.fold.out'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        sequence = f.readline().strip().split()[0]
        
        f.close()
        results[resdir][ID] = (sequence, structure)
print('Done rnainverse')          
 
for resdir in ['rnaredprint', 'rnaredprint_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        sequence = f.readline().strip().split()[0]
        
        f.close()
        results[resdir][ID] = (sequence, structure)
print('Done rnaredprint') 
     
for resdir in ['rnasfbinv', 'rnasfbinv_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        f.readline()
        sequence = f.readline().strip()
        structure = f.readline().strip()
         
        f.close()
        results[resdir][ID] = (sequence, structure)     
print('Done rnasfbinv')        

for resdir in ['dss-opt', 'dss-opt_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')

        for l in f:
            l = l.strip()
            if l.startswith('vienna'):
                sequence = l.split()[-1]
            if l.startswith('seq'):
                structure = l.split()[-1]    
        f.close()
        results[resdir][ID] = (sequence, structure)  
print('Done dss-opt')

for resdir in ['info-rna', 'info-rna_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        res_start = False
        for l in f:
            l = l.strip()
            if l.startswith('Local Search Results'):
                res_start = True
            if res_start:
                if l.startswith('MFE:'):    
                    sequence = l.split()[1]
                if l.startswith('NO_MFE:'):
                    structure = l.split()[1]    
        f.close()
        results[resdir][ID] = (sequence, structure)  
print('Done info-rna')

try:
    os.mkdir('results')
except:
    pass
 
f = open('data/loops_id.csv', 'r')
f_o = open('results/results.txt', 'w')
f_mis = open('results/missing.txt', 'w')

for k1 in results:
    for k2 in results[k1]:
        if results[k1][k2][0] == '' or results[k1][k2][1] == '':
            f_mis.write(f'Missing res for {k1} {k2}\n')
f_mis.close()

algs_order = list(results.keys())
algs_order.sort()

to_write = ['ID', 'sequence', 'structure', 'sequence_extended', 'structure_extended']
for algo in algs_order:
    to_write.append(f'{algo}_sequence')
    to_write.append(f'{algo}_structure')
print(';'.join(to_write), file=f_o)

for l in f:
    l = l.strip().split(',')
    
    name = l[0]
    
    if name == 'Source': continue
    ID = l[-1]
    
    fragment_sequence = l[5]
    fragment_structure = remove_junk(l[6])
    
    fragment_sequence_ext = l[8]
    fragment_structure_ext = remove_junk(l[9])
    
    if len(fragment_structure_ext) > 100:
        continue

    to_write = [ID, fragment_sequence, fragment_structure, fragment_sequence_ext, fragment_structure_ext]
    for algo in algs_order:
        to_write.append(results[algo][ID][0])
        to_write.append(results[algo][ID][1])
    
    print(';'.join(to_write), file=f_o)

f.close()
f_o.close()
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
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        line = f.readline().strip()
        while line != 'Closest solution:' and line != 'Best solution:':
            line = f.readline().strip()
            
        sequence = f.readline().strip()
        structure = f.readline().strip()
        
        f.close()
        results[resdir][ID] = (sequence, structure)
#print('Done desirna')    
        
for resdir in ['rnainverse', 'rnainverse_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        sequence = f.readline().strip().split()[0]
        
        f.close()
        results[resdir][ID] = (sequence, structure)
#print('Done rnainverse')          
 
for resdir in ['rnaredprint', 'rnaredprint_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        sequence = f.readline().strip().split()[0]
        
        f.close()
        results[resdir][ID] = (sequence, structure)
#print('Done rnaredprint') 
     
for resdir in ['rnasfbinv', 'rnasfbinv_extended']:
    results[resdir] = {}
    for fn in os.listdir(f'outputs/{resdir}'):
        if fn.endswith('.err'): continue
        ID = fn.split('.')[0]
        f = open(f'outputs/{resdir}/{fn}', 'r')
        
        f.readline()
        sequence = f.readline().strip()
        structure = f.readline().strip()
         
        f.close()
        results[resdir][ID] = (sequence, structure)     
#print('Done rnasfbinv')        

 
f = open('data/loops_id.csv', 'r')
f_o1 = open('results.txt', 'w')
f_o2 = open('results_extended.txt', 'w')
for l in f:
    l = l.strip().split(',')
    
    name = l[0]
    
    if name == 'Source': continue
    ID = l[-1]
    
    if ID not in results['desirna']: continue
    
    print(ID)
    
    fragment_sequence = l[5]
    fragment_structure = remove_junk(l[6])
    
    fragment_sequence_ext = l[8]
    fragment_structure_ext = remove_junk(l[9])
    
    print(f'Original:\t{fragment_sequence}\t{fragment_structure}', file=f_o1)
    for algo in results:
        if 'extended' in algo: continue
        print(f'{algo}:\t{results[algo][ID][0]}\t{results[algo][ID][1]}', file=f_o1)
    print('------------------------------------------------------------', file=f_o1)
        
    print(f'Original:\t{fragment_sequence_ext}\t{fragment_structure_ext}', file=f_o2)
    for algo in results:
        if 'extended' not in algo: continue
        print(f'{algo[:-9]}:\t{results[algo][ID][0]}\t{results[algo][ID][1]}', file=f_o2)
    print('------------------------------------------------------------', file=f_o2)
    
f.close()
f_o1.close()
f_o2.close()
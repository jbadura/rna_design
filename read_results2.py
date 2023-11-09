import os
import sys

def remove_pseudoknots(s):
    res = []
    for c in s:
        if c in '.()':
            res.append(c)
        else:
            res.append('.')
    return ''.join(res)

def read_desirna(results):
    resdir = 'desirna'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'outputs2/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''

            f = open(f'outputs2/{resdir}/{ID}_{i}.out', 'r')
            line = f.readline().strip()
            while not line.startswith('Closest solution:') and not line.startswith('Best solution:'):
                line = f.readline().strip()
                
            sequence = f.readline().strip()
            structure = f.readline().strip()
            
            f.close()
            results[resdir][ID].append((sequence, structure))
    print('Done desirna')    

def read_rnainverse(results): 
    resdir = 'rnainverse'
    results[resdir] = {}
    for fn in os.listdir(f'outputs2/{resdir}'):
        if not fn.endswith('.fold.out'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'outputs2/{resdir}/{fn}', 'r')
        
        for i in range(10):
            sequence = f.readline().strip()
            structure = f.readline().strip().split()[0]
            results[resdir][ID].append((sequence, structure))
        f.close()
    print('Done rnainverse')          
 
def read_rnaredprint(results):
    resdir = 'rnaredprint'
    results[resdir] = {}
    for fn in os.listdir(f'outputs2/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'outputs2/{resdir}/{fn}', 'r')
        
        structure = f.readline().strip()
        for i in range(10):
            sequence = f.readline().strip().split()[0]
            results[resdir][ID].append((sequence, structure))
        f.close()
    print('Done rnaredprint') 

def read_rnasfbinv(results):
    resdir = 'rnasfbinv'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'outputs2/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''
            f = open(f'outputs2/{resdir}/{ID}_{i}.out', 'r')
            
            f.readline()
            sequence = f.readline().strip()
            structure = f.readline().strip()
             
            f.close()
            results[resdir][ID].append((sequence, structure))
    print('Done rnasfbinv')        

def read_dss_opt(results):
    resdir = 'dss-opt'
    results[resdir] = {}
    done = set()
    for fn in os.listdir(f'outputs2/{resdir}'):
        if fn.endswith('.err'): continue
        ID = '_'.join(fn.split('_')[:-1])
        if ID in done: continue
        done.add(ID)
        results[resdir][ID] = []
        for i in range(10):
            sequence = ''
            structure = ''
            
            f = open(f'outputs2/{resdir}/{ID}_{i}.out', 'r')
            for l in f:
                l = l.strip()
                if l.startswith('vienna'):
                    structure = l.split()[-1]
                if l.startswith('seq'):
                    sequence = l.split()[-1]    
            f.close()
            results[resdir][ID].append((sequence, structure))
    print('Done dss-opt')

def read_info_rna(results):
    resdir = 'info-rna'
    results[resdir] = {}
    for fn in os.listdir(f'outputs2/{resdir}'):
        if fn.endswith('.err'): continue
        sequence = ''
        structure = ''
        ID = fn.split('.')[0]
        results[resdir][ID] = []
        f = open(f'outputs2/{resdir}/{fn}', 'r')
        res_start = False
        for l in f:
            l = l.strip()
            if l.startswith('Local Search Results'):
                res_start = True
            if res_start:
                if l.startswith('MFE:'):    
                    sequence = l.split()[1]
                    results[resdir][ID].append((sequence, ''))     
        f.close()    
    print('Done info-rna')

def check_missing(results):
    f_mis = open('results2/missing.txt', 'w')
    for k1 in results:
        for k2 in results[k1]:
            if len(results[k1][k2]) != 10:
                f_mis.write(f'Missing res for {k1} {k2}, no 10!\n')
            for sequence, structure in results[k1][k2]:
                if sequence == '' or structure == '':
                    f_mis.write(f'Missing res for {k1} {k2}\n')
    f_mis.close()


def main():
    try:
        os.mkdir('results2')
    except:
        pass
    
    results = {}
    read_desirna(results)
    read_rnainverse(results)
    read_rnaredprint(results)
    read_rnasfbinv(results)
    read_dss_opt(results)
    read_info_rna(results)
    check_missing(results)
    
    f_o = open('results2/results.txt', 'w')

    algs_order = list(results.keys())
    algs_order.sort()

    to_write = ['ID', 'sequence', 'structure']
    for algo in algs_order:
        for i in range(10):
            to_write.append(f'{algo}_sequence_{i}')
            to_write.append(f'{algo}_structure_{i}')
    print(';'.join(to_write), file=f_o)

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
            fragment_structure = remove_pseudoknots(l[3])
            fragment_sequence = l[1]
            
            i += 1

            to_write = [ID, fragment_sequence, fragment_structure]
            for algo in algs_order:
                for sequence, structure in results[algo][ID]:
                    to_write.append(sequence)
                    to_write.append(structure)

            print(';'.join(to_write), file=f_o)

        f_list.close()
    f_o.close()

main()
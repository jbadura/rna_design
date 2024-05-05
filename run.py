import os
import sys
import utils

'''
Run multiple time: desirna, dss-opt, rnasfbinv
Run once: info-rna, rnainverse, rnaredprint
'''


def run_desirna(indir, outdir, input_file_name, repeats=1):
    for test_num in range(repeats):
        ID = input_file_name.split('.')[0]
        if repeats > 1:
            output_file_name_prefix = f'{ID}_{test_num}'
        else:
            output_file_name_prefix = f'{ID}'

        command = ['time', 'python3', '/DesiRNA/DesiRNA.py', '-f', f'{indir}/{input_file_name}']
        status = utils.run_command(command, outdir, output_file_name_prefix, timeout=80)
        if status != 'DONE':
            continue

        sequence, structure = utils.read_desirna_output(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)

    
def run_dss_opt(indir, outdir, input_file_name, repeats=1):
    for test_num in range(repeats):
        ID = input_file_name.split('.')[0]
        if repeats > 1:
            output_file_name_prefix = f'{ID}_{test_num}'
        else:
            output_file_name_prefix = f'{ID}'

        infile = open(f'{indir}/{input_file_name}', 'r')
        seq = infile.readline().strip()
        infile.close()

        command = ['time', '/dss-opt/opt-md', seq]
        status = utils.run_command(command, outdir, output_file_name_prefix)
        if status != 'DONE':
            continue

        sequence, structure = utils.read_dss_opt_output(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)


def run_rnasfbinv(indir, outdir, input_file_name, repeats=1):
    for test_num in range(repeats):
        ID = input_file_name.split('.')[0]
        if repeats > 1:
            output_file_name_prefix = f'{ID}_{test_num}'
        else:
            output_file_name_prefix = f'{ID}'

        command = ['time', 'python3', '/RNAsfbinv/RNAfbinvCL.py', '-f', f'{indir}/{input_file_name}']
        status = utils.run_command(command, outdir, output_file_name_prefix)
        if status != 'DONE':
            continue

        sequence, structure = utils.read_rnasfbinv_output(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)


def run_info_rna(indir, outdir, input_file_name, repeats=1):
    output_file_name_prefix = input_file_name.split('.')[0]

    infile = open(f'{indir}/{input_file_name}', 'r')
    seq = infile.readline().strip()
    infile.close()

    if repeats == 1:
        command = ['time', '/INFO-RNA-2.1.2/INFO-RNA-2.1.2', seq]
    else:
        command = ['time', '/INFO-RNA-2.1.2/INFO-RNA-2.1.2', seq, '-R', str(repeats)]
    status = utils.run_command(command, outdir, output_file_name_prefix)
    if status != 'DONE':
        return

    if repeats == 1:
        sequence, structure = utils.read_rna_info_one(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)
    else:
        sequences, structures = utils.read_rna_info_many(outdir, f'{output_file_name_prefix}.out')
        for test_num in range(repeats):
            sequence, structure = sequences[test_num], structures[test_num]
            utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}_{test_num}.fold')
            rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}_{test_num}.fold.out')
            utils.save_parsed_results(outdir, f'{output_file_name_prefix}_{test_num}', sequence, structure, rnafold_structure)


def run_rnainverse(indir, outdir, input_file_name, repeats=1):
    output_file_name_prefix = input_file_name.split('.')[0]

    if repeats == 1:
        command = ['time', 'RNAinverse']
    else:
        command = ['time', 'RNAinverse', f'-R{repeats}']
    status = utils.run_command(command, outdir, output_file_name_prefix, input_file_full_path=f'{indir}/{input_file_name}')
    if status != 'DONE':
        return

    if repeats == 1:
        sequence, structure = utils.read_rnainverse_one(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)
    else:
        sequences, structures = utils.read_rnainverse_many(outdir, f'{output_file_name_prefix}.out')
        for test_num in range(repeats):
            sequence, structure = sequences[test_num], structures[test_num]
            utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}_{test_num}.fold')
            rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}_{test_num}.fold.out')
            utils.save_parsed_results(outdir, f'{output_file_name_prefix}_{test_num}', sequence, structure, rnafold_structure)


def run_rnaredprint(indir, outdir, input_file_name, repeats=1):
    output_file_name_prefix = input_file_name.split('.')[0]

    infile = open(f'{indir}/{input_file_name}', 'r')
    seq = infile.readline().strip()
    infile.close()

    command = ['time', '/RNARedPrint/_inst/bin/RNARedPrint', '--num', str(repeats), seq]
    status = utils.run_command(command, outdir, output_file_name_prefix)
    if status != 'DONE':
        return

    if repeats == 1:
        sequence, structure = utils.read_rnaredprint_one(outdir, f'{output_file_name_prefix}.out')
        utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}.fold')
        rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}.fold.out')
        utils.save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure)
    else:
        sequences, structures = utils.read_rnaredprint_many(outdir, f'{output_file_name_prefix}.out')
        for test_num in range(repeats):
            sequence, structure = sequences[test_num], structures[test_num]
            utils.run_rnafold([sequence], outdir, f'{output_file_name_prefix}_{test_num}.fold')
            rnafold_sequence, rnafold_structure = utils.read_rnafold_one(outdir, f'{output_file_name_prefix}_{test_num}.fold.out')
            utils.save_parsed_results(outdir, f'{output_file_name_prefix}_{test_num}', sequence, structure, rnafold_structure)


ALGO = {'desirna': run_desirna, 'dss-opt': run_dss_opt, 'info-rna': run_info_rna, 'rnainverse': run_rnainverse, 'rnaredprint': run_rnaredprint, 'rnasfbinv': run_rnasfbinv}
DIRS ={ 'desirna': [('desirna', 'desirna'), ('desirna_extended', 'desirna_extended')],
        'dss-opt': [('rnainverse', 'dss-opt'), ('rnainverse_extended', 'dss-opt_extended')],
        'info-rna': [('rnainverse', 'info-rna'), ('rnainverse_extended', 'info-rna_extended')],
        'rnainverse': [('rnainverse', 'rnainverse'), ('rnainverse_extended', 'rnainverse_extended')],
        'rnaredprint': [('rnainverse', 'rnaredprint'), ('rnainverse_extended', 'rnaredprint_extended')],
        'rnasfbinv': [('rnasfbinv', 'rnasfbinv'), ('rnasfbinv_extended', 'rnasfbinv_extended')]
}

def main():
    if len(sys.argv) != 5:
        print('Usage: python3 run.py algoname start end dataset')
        exit()
    range_s = int(sys.argv[2])
    range_e = int(sys.argv[3])
    dataset = sys.argv[4]
    if dataset.endswith('/'):
        dataset = dataset[:-1]
    if dataset.startswith('inputs_'):
        dataset = dataset[7:]
    repeats = 1

    INPUT_PREF = f'/rna_design/inputs_{dataset}/'
    OUTPUT_PREF = f'/rna_design/outputs_{dataset}/'

    if sys.argv[1] == 'ALL':
        algos_to_run = list(ALGO.keys())
    else:
        algos_to_run = [sys.argv[1]]

    try:
        os.mkdir('/rna_design/logs')
    except:
        pass

    log = open(f'/rna_design/logs/{dataset}_{range_s}_{range_e}_{sys.argv[1]}.log.out', 'w')
    err = open(f'/rna_design/logs/{dataset}_{range_s}_{range_e}_{sys.argv[1]}.log.err', 'w')
    sys.stdout = log
    sys.stderr = err

    for algo in algos_to_run:
        run_algo = ALGO[algo]
        dirs = DIRS[algo]
        for indir, outdir in dirs:
            indir = INPUT_PREF + indir
            outdir = OUTPUT_PREF + outdir
            
            to_do = os.listdir(indir)
            to_do.sort()
            to_do = to_do[range_s:range_e]
            for fn in to_do:
                print(f'Starting {indir}, {fn}, {run_algo}', flush=True)
                run_algo(indir, outdir, fn, repeats=repeats)
                print(f'Done {indir}, {fn}, {run_algo}', flush=True)


main()

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
            return

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
            return

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
            return

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
DIRS = {'1':
       {'desirna': [('/rna_design/inputs/desirna', '/rna_design/outputs/desirna'), ('/rna_design/inputs/desirna_extended', '/rna_design/outputs/desirna_extended')],
        'dss-opt': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/dss-opt'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/dss-opt_extended')],
        'info-rna': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/info-rna'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/info-rna_extended')],
        'rnainverse': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/rnainverse'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/rnainverse_extended')],
        'rnaredprint': [('/rna_design/inputs/rnainverse', '/rna_design/outputs/rnaredprint'), ('/rna_design/inputs/rnainverse_extended', '/rna_design/outputs/rnaredprint_extended')],
        'rnasfbinv': [('/rna_design/inputs/rnasfbinv', '/rna_design/outputs/rnasfbinv'), ('/rna_design/inputs/rnasfbinv_extended', '/rna_design/outputs/rnasfbinv_extended')]},
        '2':
        {'desirna': [('/rna_design/inputs2/desirna', '/rna_design/outputs2/desirna')],
        'dss-opt': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/dss-opt')],
        'info-rna': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/info-rna')],
        'rnainverse': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/rnainverse')],
        'rnaredprint': [('/rna_design/inputs2/rnainverse', '/rna_design/outputs2/rnaredprint')],
        'rnasfbinv': [('/rna_design/inputs2/rnasfbinv', '/rna_design/outputs2/rnasfbinv')]}
}


def main():
    if len(sys.argv) != 5:
        print('Usage: python3 run.py algoname start end dataset')
        exit()
    range_s = int(sys.argv[2])
    range_e = int(sys.argv[3])
    repeats = 1 if sys.argv[4] == '1' else 10

    if sys.argv[1] == 'ALL':
        algos_to_run = list(ALGO.keys())
    else:
        algos_to_run = [sys.argv[1]]

    for algo in algos_to_run:
        run_algo = ALGO[algo]
        dirs = DIRS[sys.argv[4]][algo]

        for indir, outdir in dirs:
            to_do = os.listdir(indir)
            to_do.sort()
            to_do = to_do[range_s:range_e]
            for fn in to_do:
                print(f'Starting {indir}, {fn}')
                run_algo(indir, outdir, fn, repeats=repeats)
                print(f'Done {indir}, {fn}')

main()

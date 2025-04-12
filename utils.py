import os
import sys
import subprocess
import signal


def save_parsed_results(outdir, output_file_name_prefix, sequence, structure, rnafold_structure):
    f = open(f'{outdir}/{output_file_name_prefix}.parsed.out', 'w')
    print(f'sequence={sequence}', file=f)
    print(f'structure={structure}', file=f)
    print(f'rnafold={rnafold_structure}', file=f)
    f.close()


def run_rnafold(sequences, outdir, output_file_name_prefix):
    f = open('tmp', 'w')
    for seq in sequences:
        f.write(seq + '\n')
    f.close()

    command = ['time', 'RNAfold']
    run_command(command, outdir, output_file_name_prefix, input_file_full_path='tmp')


def run_command(command, outdir, output_file_name_prefix, input_file_full_path=None, timeout=70, skip_if_outputfile_exists=True):
    """
    This function runs command using subprocess.Popen, waits for timeout seconds and kill the process group if TLE.
    Output and errput file is derived from output_file_name_prefix by adding extensions .out and .err
    If TLE then .timeouted file is created.
    By default input_file is passed as argument stdin= of Popen, but it can be turned off (in case command takes input file as a parameter)

    The function returns "DONE" if command ended normally or "TIMEOUTED" when TLE
    """
    if output_file_name_prefix.endswith('.out'):
        print('Wrong output file name passed to run_command')
        exit()
    output_file_name = output_file_name_prefix + '.out'
    errput_file_name = output_file_name_prefix + '.err'
    timeout_file_name = output_file_name_prefix + '.timeouted'
    rte_file_name = output_file_name_prefix + '.rte'

    if skip_if_outputfile_exists:
        if os.path.isfile(f'{outdir}/{output_file_name_prefix}.parsed.out'):
            return 'DONE'
        if os.path.isfile(f'{outdir}/{timeout_file_name}'):
            return 'TIMEOUTED'
        if os.path.isfile(f'{outdir}/{rte_file_name}'):
            return 'RTE'

    if input_file_full_path is not None:
        input_file = open(input_file_full_path, 'r')
    else:
        input_file = None

    output_file = open(f'{outdir}/{output_file_name}', 'w')
    errput_file = open(f'{outdir}/{errput_file_name}', 'w')

    status = 'DONE'
    try:
        p = subprocess.Popen(command, stdin=input_file, stdout=output_file, stderr=errput_file, start_new_session=True)
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        open(f'{outdir}/{timeout_file_name}', 'w').close()
        status = 'TIMEOUTED'

    if status != 'TIMEOUTED' and p.returncode != 0:
        open(f'{outdir}/{rte_file_name}', 'w').close()
        status = 'RTE'

    if input_file is not None:
        input_file.close()
    output_file.close()
    errput_file.close()

    if status != 'TIMEOUTED' and os.stat(f'{outdir}/{output_file_name}').st_size == 0:
        open(f'{outdir}/{rte_file_name}', 'w').close()
        status = 'RTE'

    return status


def read_desirna_output(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    line = f.readline().strip()
    while not line.startswith('Target structure:') and not line.startswith('Best solution:'):
        line = f.readline().strip()
    sequence = f.readline().strip()
    nop = f.readline().strip()
    structure = f.readline().strip()
    f.close()
    return sequence, structure


def read_dss_opt_output(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    for l in f:
        l = l.strip()
        if l.startswith('vienna'):
            structure = l.split()[-1]
        if l.startswith('seq'):
            sequence = l.split()[-1]
    f.close()
    return sequence, structure


def read_rnasfbinv_output(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    f.readline()
    sequence = f.readline().strip()
    structure = f.readline().strip()
    f.close()
    return sequence, structure


def read_rnafold_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    sequence = f.readline().strip()
    structure = f.readline().strip().split()[0]
    f.close()
    return sequence, structure


def read_rna_info_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    res_start = False
    sequence = 'no_sequence'
    structure = 'no_structure'
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
    return sequence, structure


def read_rna_info_many(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    sequences = []
    structures = []
    order = []
    res_start = False
    for l in f:
        l = l.strip()
        if l.startswith('Local Search Results'):
            res_start = True
        if res_start:
            if l.startswith('MFE:'):
                sequence = l.split()[1]
                sequences.append(sequence)
                order.append('MFE')
            if l.startswith('NO_MFE:'):
                structure = l.split()[1]
                structures.append(structure)
                order.append('NO_MFE')
    f.close()
    real_structs = []
    k, i = 0, 1
    while i < len(order):
        if order[i] == 'NO_MFE' and order[i - 1] == 'MFE':
            real_structs.append(structures[k])
            k += 1
        if order[i] == 'MFE' and order[i - 1] == 'MFE':
            real_structs.append('no_structure')
        i += 1
    return sequences, real_structs


def read_rnainverse_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    sequence = f.readline().strip().split()[0]
    f.close()
    return sequence, 'no_structure'


def read_rnainverse_many(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    sequences = []
    for l in f:
        sequence = l.strip().split()[0]
        sequences.append(sequence)
    f.close()
    return sequences, ['no_structure'] * len(sequences)


def read_rnaredprint_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    structure = f.readline().strip()
    sequence = f.readline().strip().split()[0]
    f.close()
    return sequence, structure


def read_rnaredprint_many(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    structure = f.readline().strip()
    sequences = []
    for l in f:
        sequence = f.readline().strip().split()[0]
        sequences.append(sequence)
    f.close()
    return sequences, [structure] * len(sequences)


#TODO don't know output format, expect all to timeout
def read_ribologic(outdir, file_name):
    sequence = 'no_sequence'
    structure = 'no_structure'
    return sequence, structure


def read_learna(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    for l in f:
        sequence = l.strip().split()[-1]
    f.close()
    structure = 'no_structure'
    return sequence, structure


def read_rnaredprint_designmultistate_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    res_seq = ''
    res_energy = 9999999999999999999999999999999999999999999999999
    for l in f:
        l = l.strip().split()
        if len(l) != 3 or not l[2].startswith('E1'):
            continue
            
        e1 = float(l[2].split('=')[1])
        seq = l[0]
        res_energy, res_seq = min((res_energy, res_seq), (e1, seq))
            
    structure = 'no_structure'
    f.close()
    return res_seq, structure


def read_rnaredprint_calcprobs_one(outdir, file_name):
    f = open(f'{outdir}/{file_name}', 'r')
    res_seq = ''
    res_mfe = 9999999999999999999999999999999999999999999999999
    res_psum = -999999999999999999999999999999999999999999999999
    for l in f:
        l = l.strip().split()
        if len(l) != 7 or not l[6].startswith('Psum') or not l[3].startswith('MFE'):
            continue
        
        psum = float(l[6].split('=')[1])
        mfe = float(l[3].split('=')[1])
        seq = l[0]
        if res_psum < psum:
            res_psum, res_mfe, res_seq = psum, mfe, seq
        elif res_psum == psum and res_mfe > mfe:
            res_psum, res_mfe, res_seq = psum, mfe, seq
            
    structure = 'no_structure'
    f.close()
    return res_seq, structure
import os
import sys
import subprocess
import shutil
import glob
from pathlib import Path
from HSDetector.file_copying import copy_inputs_to_cwd
from HSDetector.run_command_with_retries import run_command_with_retries
from HSDetector.run_inputs_script import run_insane


def parse_lipid_string(lipid_str):
    '''
    This function ensures the membrane components inputs is correct before proceeding. Rearranges the string
    to make CHOL the last membrane component in order to be consistent when making the index for GROMACS
    :param lipid_str:
    :return new membrane string:
    '''
    # Check if input is a non-empty string
    if not isinstance(lipid_str, str) or not lipid_str.strip():
        sys.exit("Membrane component string incorrect format. Should be: 'COMP1:ratio,COMP2:ratio...'")

    # Split and strip whitespace
    pairs = [pair.strip() for pair in lipid_str.split(',')]

    # Check for empty entries (e.g., "POPC:50,,CHOL:50")
    if any(not pair for pair in pairs):
        sys.exit("Membrane component string incorrect format. Should be: 'COMP1:ratio,COMP2:ratio...'")

    # Validate each pair
    for pair in pairs:
        if ':' not in pair:
            sys.exit("Membrane component string incorrect format. Should be: 'COMP1:ratio,COMP2:ratio...'")

        lipid, ratio = pair.split(':', 1)
        lipid = lipid.strip()
        ratio = ratio.strip()

        if not lipid:
            sys.exit("Membrane component string incorrect format. Lipid name cannot be empty.")

        try:
            ratio_float = float(ratio)
            if ratio_float <= 0:
                sys.exit("Ratios must be positive numbers.")
        except ValueError:
            sys.exit("Membrane component string incorrect format. Ratios should be numbers.")

    # Check for CHOL (case-sensitive, but whitespace-insensitive)
    chol_pairs = [p for p in pairs if p.startswith('CHOL:')]
    if not chol_pairs:
        sys.exit("Input membrane contains no cholesterol. Add cholesterol for the hot spots calculation.")
    if len(chol_pairs) > 1:
        sys.exit("Multiple CHOL entries found. Only one CHOL component allowed.")

    # Separate CHOL from other lipids
    other_pairs = [p for p in pairs if not p.startswith('CHOL:')]
    chol_pair = chol_pairs[0]

    # Reconstruct the string with CHOL last
    new_str = ','.join(other_pairs + [chol_pair])

    return new_str

def system_build(output_dir, starting_structure, pdb_id, n_reps, mb_comp_raw, martinize2_path, gmx_path):
    '''
    1) Converts to CG using martinize2
    2) Writes topology
    :param pdb:
    :param n_reps:
    :martinize2_path:
    :return:
    '''

    mb_comp = parse_lipid_string(mb_comp_raw) # CHECK IF MEMB INPUT IS CORRECT BEFORE DOING ANYTHING ELSE

    os.makedirs(output_dir, exist_ok=True)

    os.chdir(output_dir)

    print(f"#####################################\n########## 1. SYSTEM BUILD ##########\n#####################################\n")
    print(f"~~~~ STEP 1: Convert structure to Martini 3 ~~~~\n")

    replica = [] # Empty list for the nº of replicas

    for i in range(0, int(n_reps)):
        replica.append(f"rep_{i + 1}") # Script will create as many replicas as stated in n_reps

    print(f"[INFO] Creating simulations directory...\n")

    os.makedirs('sims', exist_ok=True)

    os.chdir('sims')

    print(f"[INFO] Copying MD input files...\n")

    copy_inputs_to_cwd() # This ensures the mdp files and martini inputs are copied to the target directory

    print(f"[INFO] Nº of replicas chosen: {int(n_reps)}. Creating replicas directories...\n")

    print("Current working dir before creating replica dirs:", os.getcwd())

    for r in replica:
        os.makedirs(r, exist_ok=True) # Create all replicas directories

    print(f"[INFO] Converting structure to Martini 3, running Martinize2...\n")

    martinize2_command = f"{martinize2_path} -f {starting_structure} -o {pdb_id}.top \
    -x {pdb_id}_martinized.pdb -p backbone -ff martini3001 -elastic -resid input -maxwarn 100 -merge all"

    run_command_with_retries(martinize2_command) # Runs martinize2, settings are hard-coded above

    print(f"~~~~ STEP 2: Membrane assembly ~~~\n")

    membrane = mb_comp.split(',') # Membrane components

    mb_string = '' # Tailing for naming
    mb_insane_string = '' # String for the insane.py command

    print(f"[INFO] Membrane composition chosen: {membrane}. Running insane.py...\n")

    for component in membrane: # Uses mb_insane_string to assemble the string to run the command
        mb_string += component.split(":")[0] + '_' + component.split(":")[1]
        mb_insane_string += component.split(":")[0] + ':' + component.split(":")[1] + ' '
        if component != membrane[-1]:
            mb_string += '_'
            mb_insane_string += ' -l '

    system_filename = pdb_id + '_' + mb_string
    system_file = system_filename + '.gro'
    system_bad_top = system_filename + '_bad.top'
    martinized_input = '../' + pdb_id + '_martinized.pdb'

    insane_command = (f"-f {martinized_input} -o {system_file} -p {system_bad_top} -pbc orthorhombic -box 14.5,14.5,"
                      f"10.5 -center -sol W -salt 0 -l {mb_insane_string}")

    for rep in replica:
        os.chdir(rep)

        # Get all .itp files in the parent directory (molecule_0.itp)
        itp_files = glob.glob('../*.itp')

        # Copy each .itp file from the parent directory to the current directory
        for itp_file in itp_files:
            shutil.copy(itp_file, os.getcwd())

        # Run the script
        run_insane(insane_command)

        os.chdir('..')

    print(f"[INFO] insane.py succeeded, both replicas built\n")
    print(f"~~~~ STEP 3: Fixing topology and making index ~~~~\n")


    includes_string = '#include "../toppar/martini_v3.0.0.itp"\n' \
                      '#include "../toppar/martini_v3.0.0_phospholipids_v1.itp"\n' \
                      '#include "../toppar/martini_v3.0.0_solvents_v1.itp"\n' \
                      '#include "../toppar/martini_v3.0_sterols_v1.0.itp"\n' \
                      '#include "../toppar/martini_v3.0.0_ions_v1.itp"\n' \
                      '#include "molecule_0.itp"\n'

    corrected_top_file = f"{system_filename}.top"

    print(f"Fixing topology files in both replicas...\n")

    # The following chunk of code writes a proper topology file for the system, correcting the insane.py output
    # by including the .itp file of the protein with its correct name and all martini .itp files
    for rep in replica:

        os.chdir(rep)

        with open(system_bad_top, 'r') as bad_top:
            bad_top_lines = bad_top.readlines()

        with open(corrected_top_file, 'w') as top:
            # Write the complete includes_string (including the molecule_0.itp file)
            top.write(includes_string)

            for line in bad_top_lines[1:]:
                if line.startswith('Protein        1'):
                    # Write the first molecule_0 line
                    top.write('molecule_0        1\n')
                else:
                    # Write other lines as they are (e.g., for POPC, CHOL, etc.)
                    top.write(line)

        os.chdir('..')

    print(f"Topologies fixed, making indices...\n")

    for rep in replica:
        os.chdir(rep)

        membrane_components = []
        for component in membrane:
            membrane_components.append(component.split(":")[0])

        index_prot_memb = '1 | r '
        gmx_index_memb = ''
        rename_components = ''
        component_group_index = 4

        for component in membrane_components:
            index_prot_memb += f"{component} "
            gmx_index_memb += f"r {component}\n"
            rename_components += f"name {component_group_index} {component}\n"
            component_group_index += 1

        run_command = [gmx_path, 'make_ndx', '-f', system_filename + '.gro', '-o', system_filename + '.ndx']
        index_inputs = [
            'del 2-25',
            index_prot_memb,
            'r W CL- NA+',
            gmx_index_memb,
            'name 2 PROT_MEMB',
            'name 3 W_ION',
            rename_components,
            'q'
        ]

        input_str = '\n'.join(index_inputs) + '\n'

        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate(input=input_str)

        print("Standard Output:\n", stdout)
        print("Standard Error:\n", stderr)

        os.chdir('..') # Return to sims/ where the rep_x/ directories are
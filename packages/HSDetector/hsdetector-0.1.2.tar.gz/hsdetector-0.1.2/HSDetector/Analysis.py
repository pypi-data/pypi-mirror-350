import os
import sys
import subprocess
import MDAnalysis as mda
import numpy as np
from tqdm import tqdm
from pathlib import Path

def run_analysis(system_name, n_reps, gmx_path):
    print(f"#####################################\n########## 3. ANALYSIS ##############\n#####################################\n")

    if not os.path.exists('sims'):
        print(f"simulation directory \'sims/\' not found in the current path ({Path.cwd()}). Cannot perform analysis.")
        sys.exit(1)
    else:
        os.chdir('sims')

    for i in range(1, int(n_reps) + 1):

        os.chdir(f"rep_{i}")

        os.makedirs('analysis', exist_ok=True)

        os.chdir('analysis')

        contacts_analysis(f"../{system_name}_prod.xtc", f"../{system_name}_npt_noconst_20fs.gro", system_name)
        density_analysis(system_name, gmx_path)

        os.chdir('../..')

    os.chdir('..')

def contacts_analysis(trajectory, structure, prefix):
    """
    Performs residue-cholesterol contact analysis and identifies outlier residues
    with relevant long contact durations.

    Parameters:
        trajectory (str): Path to trajectory file.
        structure (str): Path to structure file (topology).
        prefix (str): Prefix for output files.
    """

    # File names
    res_total_contacts_filename = prefix + '_res_total_contacts.txt'
    res_max_contacts_filename = prefix + '_res_max_contacts.csv'
    res_outliers_filename = prefix + '_res_outliers.csv'

    # Selection for residue contacts with cholesterol
    res_contact_selection = '(protein) and (around 6 (resname CHOL))'

    # Initialize dictionaries
    res_contacts_dict = {}
    res_timeframe_dict = {}

    print('Loading system...')
    system = mda.Universe(structure, trajectory)
    print('Done\n')

    all_res_ids = list(set(atom.resid for atom in system.select_atoms('protein')))
    for res in all_res_ids:
        res_contacts_dict[res] = [0]
        res_timeframe_dict[res] = [[]]  # Store frame lists as [start, end]

    frames = system.trajectory
    print('Iterating over frames...')
    for frame in tqdm(frames):
        contacting_res_obj = system.select_atoms(res_contact_selection)
        contacting_res_ids = list(set(atom.resid for atom in contacting_res_obj))

        for res in all_res_ids:
            if res in contacting_res_ids:
                if res_contacts_dict[res][-1] == 0:
                    res_timeframe_dict[res][-1] = [frame.frame]
                res_contacts_dict[res][-1] += 1
            else:
                if res_contacts_dict[res][-1] != 0:
                    res_timeframe_dict[res][-1].append(frame.frame)
                    res_timeframe_dict[res].append([])
                    res_contacts_dict[res].append(0)

    print('Writing contact outputs...')
    with open(res_total_contacts_filename, 'w') as res_tot_cnt_file, \
         open(res_max_contacts_filename, 'w') as res_max_cnt_file:

        res_max_cnt_file.write(
            'ResID,Resname,Longest contact (frames),Longest contact (ps),Contact first frame,Contact last frame\n')

        for res in res_contacts_dict:
            if res_contacts_dict[res][-1] == 0:
                res_contacts_dict[res].pop()
                res_timeframe_dict[res].pop()

            residue_selection_obj = system.select_atoms(f'resid {res}')
            resname = list(set(atom.resname for atom in residue_selection_obj))[0]

            res_contact_time_pairs = [
                f"[{frames},{','.join(map(str, timeframe))}]" for frames, timeframe in zip(res_contacts_dict[res], res_timeframe_dict[res])
            ]
            res_tot_cnt_file.write(f"{res},{resname},{res_contact_time_pairs}\n")

            if res_contacts_dict[res]:
                longest_contact_idx = max(range(len(res_contacts_dict[res])), key=res_contacts_dict[res].__getitem__)
                longest_contact_frames = res_contacts_dict[res][longest_contact_idx]
                if longest_contact_frames > 0:
                    longest_contact_ps = longest_contact_frames * 20
                    timeframe = res_timeframe_dict[res][longest_contact_idx]
                    if len(timeframe) == 2:
                        start_frame, end_frame = timeframe
                        res_max_cnt_file.write(
                            f"{res},{resname},{longest_contact_frames},{longest_contact_ps},{start_frame},{end_frame}\n")

    print('Contact analysis completed.\nFinding outliers...')

    all_res_data = {}
    all_calculated_res_longest_contacts = []

    with open(res_max_contacts_filename, 'r') as max_contacts:
        data = max_contacts.readlines()[1:]
        for line in data:
            new_line = line.strip().split(',')
            if len(new_line) >= 6:
                all_res_data[int(new_line[3])] = new_line
                all_calculated_res_longest_contacts.append(int(new_line[3]))

    all_calculated_res_longest_contacts_int = np.array(all_calculated_res_longest_contacts)
    q1, q3 = np.percentile(sorted(all_calculated_res_longest_contacts_int), [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = [x for x in all_calculated_res_longest_contacts_int if x <= lower_bound or x >= upper_bound]

    with open(res_outliers_filename, 'w') as outlier_file:
        header = 'ResID,Resname,Longest contact (frames),Longest contact (ps),Contact first frame,Contact last frame,Beginning of contact (ps),End of contact (ps)\n'
        outlier_file.write(header)

        for t in outliers:
            res_data = all_res_data[t]
            try:
                b_cnt = int(res_data[4]) * 20
                e_cnt = int(res_data[5]) * 20
                outlier_file.write(','.join(res_data) + f",{b_cnt},{e_cnt}\n")
            except (ValueError, IndexError):
                continue

    print(f"Outliers written to {res_outliers_filename}")


def cube_to_coords(cube_file, prefix, sdf_type):

    ''' This function reads a Gaussian Cube file formatted by the GROMACS tool 'gmx spatial' and converts its
    volumetric data at a specific isovalue into an .xyz file with coordinates corresponding to the density points
    above the threshold (the isovalue). Arguments used are the path to the file and 'prefix' and 'sdf_type', with
    the latter two used for the naming of the output file, standardized in the automatic pipeline. '''

    threshold_value = 99.99  # 0.01% of the data will be kept when calculating threshold. Modify to adjust.
    cube_data = {}  # Placeholder for the cube data
    bohr_to_angstrom_conv = 0.529177249  # Conversion from Bohr radius to Angstrom (1 BR = 0.529177249 A)

    # Check for valid sdf_type
    valid_sdf_types = ['hg', 'tl', 'all']
    if sdf_type not in valid_sdf_types:
        print("Error: SDF type not valid. Please enter either hg (head groups), tl (cholesterol tails) or all.")
        sys.exit(1)  # Exit the script with an error code

    with open(cube_file, 'r') as gcube:  # Read the cube and store metadata and data
        lines = gcube.readlines()
        cube_data['title'] = str(lines[0].strip())
        cube_data['description'] = str(lines[1].strip())
        cube_data['n_atoms'] = int(lines[2].split()[0])
        bohr_origin = (float(lines[2].split()[1]), float(lines[2].split()[2]), float(lines[2].split()[3]))
        cube_data['origin'] = tuple(i*bohr_to_angstrom_conv for i in bohr_origin)
        bohr_voxel_size = (float(lines[3].split()[1]), float(lines[4].split()[2]), float(lines[5].split()[3]))
        cube_data['voxel_size'] = tuple(i*bohr_to_angstrom_conv for i in bohr_voxel_size)
        cube_data['dimensions'] = (int(lines[3].split()[0]), int(lines[4].split()[0]), int(lines[5].split()[0]))
        data_start_index = cube_data['n_atoms'] + 6

        voxels = []  # Placeholder for volumetric data

        for line in lines[data_start_index:]:
            stripped_line = line.strip()
            voxel_list = stripped_line.split()
            for i in voxel_list:
                voxels.append(float(i))

        cube_data['data'] = voxels

    voxel_array = np.array(voxels)  # Converted to numpy array for reshaping and further iterations
    threshold = np.percentile(voxel_array, threshold_value)  # Calculated isovalue
    print('Using an isovalue of ' + str(threshold) + ' as the threshold')
    voxel_array = voxel_array.reshape(cube_data['dimensions'])  # Reshape the array using the correct dimensions

    dim_x = len(voxel_array)
    dim_y = len(voxel_array[0])
    dim_z = len(voxel_array[0][0])

    xyz_coords = []  # Placeholder for the voxel coordinates

    with open('coords_tl.txt', 'w') as coords:
        for z in range(dim_z):  # Iterate through the array in a specific way
            for y in range(dim_y):
                for x in range(dim_x):
                    voxel_value = voxel_array[x, y, z]  # Evaluates the value of the voxel in each grid point
                    if voxel_value > threshold:  # If value exceeds threshold coordinates are computed and stored

                        x_center = cube_data['origin'][0] + x * cube_data['voxel_size'][0]
                        y_center = cube_data['origin'][1] + y * cube_data['voxel_size'][1]
                        z_center = cube_data['origin'][2] + z * cube_data['voxel_size'][2]
                        xyz_coords.append([x_center, y_center, z_center])

                        coords.write(str(x_center) + ' ' + str(y_center) + ' ' + str(z_center) + '\n')

    outfile = prefix + '_' + sdf_type + '.xyz'

    if sdf_type == 'tl':  # Loop to check what to write in the xyz file as title
        type = 'cholesterol tails - '
    elif sdf_type == 'hg':
        type = 'cholesterol headgroups - '
    else:  # sdf_type == 'all'
        type = 'all points - '

    with open(outfile, 'w') as sdf:
        n_points = len(xyz_coords)  # Nº points needed by visualization software to understand the file
        sdf.write(str(n_points) + '\n' + 'SDF for ' + type + prefix + '\n')  # Nº points and title
        for point in xyz_coords:
            x = str(round(point[0]))
            y = str(round(point[1]))
            z = str(round(point[2]))
            sdf.write('D ' + x + ' ' + y + ' ' + z + '\n')

    return cube_data

def density_analysis(system_name, gmx_path):
    with open(f"../{system_name}.ndx", "r") as file:
        content = file.read()
        chol_group_index = int(content.count('[')) - 1 # [ CHOL ] will be in the last index group, find the group number to use in gmx spatial

    print(f"~~~~ STEP 1: Recenter and reshape the unit cell (gmx trjconv) ~~~~\n")

    cmd_trjconv_1 = f"echo \"0\" | {gmx_path} trjconv -f ../{system_name}_prod.xtc -s ../{system_name}_prod.tpr -o {system_name}_prod_sdf_1.xtc -n ../{system_name}.ndx -boxcenter tric -ur compact -pbc none"
    subprocess.run(cmd_trjconv_1, shell=True, check=True)  # Ensure it runs successfully

    print(f"~~~~ STEP 2: Align all frames to remove translational and rotational motion (gmx trjconv) ~~~~\n")

    cmd_trjconv_2 = [
            "gmx_mpi", "trjconv",
            "-f", f"{system_name}_prod_sdf_1.xtc",
            "-s", f"../{system_name}_prod.tpr",
            "-o", f"{system_name}_prod_sdf_2.xtc",
            "-n", f"../{system_name}.ndx",
            "-fit", "rot+trans"
        ]

    # We use the Protein as reference and output the whole system
    cmd_trjconv_2_inputs = "1\n0\n"  # Simulate typing '1' (Protein) + Enter, then '0' (System) + Enter

    try:
        process = subprocess.Popen(
            cmd_trjconv_2,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate(input=cmd_trjconv_2_inputs)

    except subprocess.TimeoutExpired:
        process.kill()
        print("Process (cmd_trjconv_2) timed out and was killed.")
    except Exception as e:
        print("An error occurred while executing cmd_trjconv_2:", e)

    print(f"~~~~ STEP 3: Calculate cholesterol SDF with respect to Protein (gmx spatial) ~~~~\n")

    cmd_gmx_spatial =[
        "gmx_mpi", "spatial",
        "-f", f"{system_name}_prod_sdf_2.xtc",
        "-s", f"../{system_name}_prod.tpr",
        "-n", f"../{system_name}.ndx",
        "-nab", "300"
    ]

    # We calculate the density for CHOL with respect to Protein
    cmd_gmx_spatial_inputs = f"{chol_group_index}\n1\n"  # Simulate typing 'N' (CHOL) + Enter, then '1' (Protein) + Enter

    try:
        process = subprocess.Popen(
            cmd_gmx_spatial,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate(input=cmd_gmx_spatial_inputs)
        #print("Standard Output (cmd_gmx_spatial):\n", stdout)
        #print("Standard Error (cmd_gmx_spatial):\n", stderr)
    except subprocess.TimeoutExpired:
        process.kill()
        print("Process (cmd_gmx_spatial) timed out and was killed.")
    except Exception as e:
        print("An error occurred while executing cmd_gmx_spatial:", e)

    print(f"~~~~ STEP 4: Convert volumetric data to cartesian XYZ coordinates ~~~~\n")

    cube_to_coords("grid.cube", system_name, "all")
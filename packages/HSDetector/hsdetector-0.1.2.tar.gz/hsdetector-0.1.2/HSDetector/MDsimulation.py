import os
import sys
import subprocess
from .membrane_quality_check import main as run_membrane_analysis


def run_MD(system_name, n_reps, gmx_path, run_mode, gpu, mb_comp):
    """
    This function checks the run mode assigned and launches the corresponding function
    :param mb_comp:
    :param system_name:
    :param n_reps:
    :param gmx_path:
    :param run_mode:
    :param gpu:
    :return:
    """

    print(f"#####################################\n########## 2. MD SIMULATION #########\n#####################################\n")

    if run_mode == 'sequential':
        sequential_MD(gmx_path, system_name, n_reps, gpu, mb_comp)
    elif run_mode == 'parallel':
        parallel_MD()


def sequential_MD(gmx_path, system_name, n_reps, gpu, mb_comp):
    print('[INFO] Sequential mode was chosen. Each replica will be simulated after the previous is finished\n')

    rep = 1
    os.chdir("sims")

    for i in range(1, int(n_reps) + 1):
        os.chdir(f"rep_{rep}")
        print(f"~~~~ Simulating replica {rep} ~~~~\n")
        run_MD_commands(rep, gmx_path, system_name, gpu, mb_comp)
        os.chdir('..')
        rep += 1

    os.chdir('..')

def parallel_MD():
    print("[FATAL ERROR] This functionality has not been implemented yet and will be available in the future",
          file=sys.stderr)
    sys.exit(1)


def run_MD_commands(n_rep, gmx_path, system_name, gpu, mb_comp):
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = "0,1,2,3"

    commands = [
        # STEP 1
        f"{gmx_path} grompp -f ../mdp_files/em.mdp -o {system_name}_em.tpr -c {system_name}.gro -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_em",

        # STEP 2
        f"{gmx_path} grompp -f ../mdp_files/nvt.mdp -o {system_name}_nvt.tpr -c {system_name}_em.gro -r {system_name}_em.gro -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_nvt -nb gpu -bonded gpu -gpu_id {gpu} -ntomp 24",

        # STEP 3
        f"{gmx_path} grompp -f ../mdp_files/npt_const.mdp -o {system_name}_npt_const.tpr -c {system_name}_nvt.gro -r {system_name}_nvt.gro -t {system_name}_nvt.cpt -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_npt_const -nb gpu -bonded gpu -gpu_id {gpu} -ntomp 24",

        # STEP 4
        f"{gmx_path} grompp -f ../mdp_files/npt_noconst_1fs.mdp -o {system_name}_npt_noconst_1fs.tpr -c {system_name}_npt_const.gro -t {system_name}_npt_const.cpt -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_npt_noconst_1fs -nb gpu -bonded gpu -gpu_id {gpu} -ntomp 24",

        # STEP 5
        f"{gmx_path} grompp -f ../mdp_files/npt_noconst_20fs.mdp -o {system_name}_npt_noconst_20fs.tpr -c {system_name}_npt_noconst_1fs.gro -t {system_name}_npt_noconst_1fs.cpt -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_npt_noconst_20fs -nb gpu -bonded gpu -gpu_id {gpu} -ntomp 24",

        # STEP 5.5 — analysis
        "MEMBRANE_ANALYSIS",

        # STEP 6
        f"{gmx_path} grompp -f ../mdp_files/npt_prod.mdp -o {system_name}_prod.tpr -c {system_name}_npt_noconst_20fs.gro -t {system_name}_npt_noconst_20fs.cpt -p {system_name}.top -n {system_name}.ndx -maxwarn 1",
        f"{gmx_path} mdrun -deffnm {system_name}_prod -nb gpu -bonded gpu -gpu_id {gpu}"
    ]

    # One message per command
    step_cmd = [
        "~~~~ STEP 1: Energy Minimization (GROMPP) ~~~~",
        "~~~~ STEP 1: Energy Minimization (MDRUN) ~~~~",
        "~~~~ STEP 2: Equilibration - NVT (GROMPP) ~~~~",
        "~~~~ STEP 2: Equilibration - NVT (MDRUN) ~~~~",
        "~~~~ STEP 3: Equilibration - NPT (Constrained, GROMPP) ~~~~",
        "~~~~ STEP 3: Equilibration - NPT (Constrained, MDRUN) ~~~~",
        "~~~~ STEP 4: Equilibration - NPT (Unconstrained 1fs, GROMPP) ~~~~",
        "~~~~ STEP 4: Equilibration - NPT (Unconstrained 1fs, MDRUN) ~~~~",
        "~~~~ STEP 5: Equilibration - NPT (Unconstrained 20fs, GROMPP) ~~~~",
        "~~~~ STEP 5: Equilibration - NPT (Unconstrained 20fs, MDRUN) ~~~~",
        "~~~~ STEP 5.5: Membrane analysis ~~~~",
        "~~~~ STEP 6: Production run (GROMPP) ~~~~",
        "~~~~ STEP 6: Production run (MDRUN) ~~~~"
    ]

    for idx, cmd in enumerate(commands):
        print(step_cmd[idx])
        if cmd == "MEMBRANE_ANALYSIS":
            mb_analysis_string = ",".join([item.split(":")[0] for item in mb_comp.split(",")])
            run_membrane_analysis(f"{system_name}_npt_noconst_20fs.tpr", f"{system_name}_npt_noconst_20fs.xtc", mb_analysis_string)
        else:
            try:
                subprocess.run(cmd, shell=True, check=True, env=env)
            except subprocess.CalledProcessError as e:
                print(f"Error in replica {n_rep}: {e}")
                raise

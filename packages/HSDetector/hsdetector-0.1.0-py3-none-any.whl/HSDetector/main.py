import sys
import os
from HSDetector.system_build import system_build
from HSDetector.MDsimulation import run_MD
from HSDetector.Analysis import run_analysis
from HSDetector.merge_data import run_replica_merge_pipeline
from HSDetector.rank_pockets import rank_pockets
from HSDetector import __version__ as VERSION

# Default values for optional parameters
DEFAULTS = {
    'n_reps': 2,
    'martinize2_path': 'martinize2',
    'gmx_path': 'gmx',
    'output_dir': './HSDetector_results',
    'MD_mode': 'sequential',
    'bw_notation': 'False',
    'rank_pockets': 'False'
}

# Mandatory parameters based on run_mode
MANDATORY_FIELDS = {
    'base': ['run_mode', 'pdb_id', 'starting_structure', 'mb_comp'],
    'intermediate': ['step'],
    'standalone': ['step']
}

ALLOWED_MD_MODES = ['sequential', 'parallel']
ALLOWED_BW_NOTATION = ['True', 'False']


def get_system_prefix(pdb_id, lipid_str):
    if not isinstance(lipid_str, str) or not lipid_str.strip():
        sys.exit("Membrane component string incorrect format. Should be: 'COMP1:ratio,COMP2:ratio...'")

    pairs = [pair.strip() for pair in lipid_str.split(',')]
    if any(not pair for pair in pairs):
        sys.exit("Membrane component string incorrect format. Should be: 'COMP1:ratio,COMP2:ratio...'")

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

    chol_pairs = [p for p in pairs if p.startswith('CHOL:')]
    if not chol_pairs:
        sys.exit("Input membrane contains no cholesterol. Add cholesterol for the hot spots calculation.")
    if len(chol_pairs) > 1:
        sys.exit("Multiple CHOL entries found. Only one CHOL component allowed.")

    other_pairs = [p for p in pairs if not p.startswith('CHOL:')]
    chol_pair = chol_pairs[0]
    new_mb_str = ','.join(other_pairs + [chol_pair])
    membrane = new_mb_str.split(',')

    mb_string = ''
    for component in membrane:
        mb_string += component.split(":")[0] + '_' + component.split(":")[1]
        if component != membrane[-1]:
            mb_string += '_'

    system_filename = pdb_id + '_' + mb_string
    return system_filename, new_mb_str


def validate_gpu(params):
    if 'gpu' not in params:
        raise ValueError("Parameter 'gpu' is required to run MD simulations.")

    gpu_raw = params['gpu']
    gpu_split = [g.strip() for g in gpu_raw.split(',')]

    try:
        if len(gpu_split) == 1:
            return int(gpu_split[0])
        elif len(gpu_split) == 2:
            return [int(g) for g in gpu_split]
        else:
            raise ValueError
    except ValueError:
        raise ValueError("Parameter 'gpu' must be a single integer or two integers separated by a comma (e.g., '0' or '0,1').")


def run_full_pipeline(params, system_filename_prefix, mb_comp_formatted):
    print("[INFO] Running full pipeline with parameters:", params)
    working_dir = os.path.abspath(params['output_dir'])

    system_build(
        starting_structure=params['starting_structure'],
        pdb_id=params['pdb_id'],
        n_reps=int(params['n_reps']),
        mb_comp_raw=params['mb_comp'],
        martinize2_path=params['martinize2_path'],
        gmx_path=params['gmx_path'],
        output_dir=params['output_dir']
    )

    os.chdir(working_dir)

    gpu_val = validate_gpu(params)

    run_MD(
        system_name=system_filename_prefix,
        n_reps=params['n_reps'],
        gmx_path=params['gmx_path'],
        run_mode=params['MD_mode'],
        gpu=gpu_val,
        mb_comp=mb_comp_formatted
    )

    run_analysis(
        system_name=system_filename_prefix,
        n_reps=params['n_reps'],
        gmx_path=params['gmx_path']
    )

    os.chdir("sims")
    run_replica_merge_pipeline(
        system_name=system_filename_prefix,
        working_dir="./",
        n_reps=params["n_reps"],
        gpcrdb_file_path=params["gpcrdb_file_path"],
        atomistic_pdb=params["starting_structure"],
        bw=params["bw_notation"]
    )

    if params.get("rank_pockets") == "True":
        rank_pockets(
            system_name=system_filename_prefix,
            pocket_file=params["pockets_file"],
            merged_outliers_csv=f"{system_filename_prefix}_outliers_MERGE.csv",
            merged_density_xyz=f"{system_filename_prefix}_density_MERGE.xyz",
        )


def run_intermediate_pipeline(params, system_filename_prefix, mb_comp_formatted):
    print(f"[INFO] Running pipeline starting from step '{params['step']}' with parameters:", params)
    working_dir = os.path.abspath(params['output_dir'])
    # You can implement intermediate functionality as needed.


def run_standalone_step(params, system_filename_prefix, mb_comp_formatted):
    print(f"[INFO] Running standalone function, only step '{params['step']}' with parameters:", params)
    step = params['step']

    if step == 'system_build':
        system_build(
            starting_structure=params['starting_structure'],
            pdb_id=params['pdb_id'],
            n_reps=int(params['n_reps']),
            mb_comp_raw=params['mb_comp'],
            martinize2_path=params['martinize2_path'],
            gmx_path=params['gmx_path'],
            output_dir=params['output_dir']
        )

    elif step == 'MD_simulation':
        os.chdir(params['output_dir'])
        gpu_val = validate_gpu(params)
        run_MD(
            system_name=system_filename_prefix,
            n_reps=params['n_reps'],
            gmx_path=params['gmx_path'],
            run_mode=params['MD_mode'],
            gpu=gpu_val,
            mb_comp=mb_comp_formatted
        )

    elif step == 'analysis':
        os.chdir(params['output_dir'])
        run_analysis(
            system_name=system_filename_prefix,
            n_reps=params['n_reps'],
            gmx_path=params['gmx_path']
        )

    elif step == 'merge_data':
        os.chdir(f"{params['output_dir']}/sims")
        run_replica_merge_pipeline(
            system_name=system_filename_prefix,
            working_dir="./",
            n_reps=params["n_reps"],
            gpcrdb_file_path=params["gpcrdb_file_path"],
            atomistic_pdb=params["starting_structure"],
            bw=params["bw_notation"]
        )

    elif step == 'rank_pockets':
        os.chdir(f"{params['output_dir']}/sims")
        rank_pockets(
            system_name=system_filename_prefix,
            pocket_file=params["pockets_file"],
            merged_outliers_csv=f"{system_filename_prefix}_outliers_MERGE.csv",
            merged_density_xyz=f"{system_filename_prefix}_density_MERGE.xyz",
        )

    else:
        raise ValueError(f"Unknown standalone step '{step}'")


def parse_prm_file(filepath):
    params = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                params[key] = value
    return params


def validate_parameters(params):
    for key, default in DEFAULTS.items():
        params.setdefault(key, default)

    for field in MANDATORY_FIELDS['base']:
        if field not in params:
            raise ValueError(f"Parameter file is missing the mandatory field '{field}'.")

    run_mode = params['run_mode']
    if run_mode not in ('full', 'intermediate', 'standalone'):
        raise ValueError(f"Unsupported run_mode '{run_mode}'. Must be one of: full, intermediate, standalone.")

    if run_mode in ('intermediate', 'standalone'):
        for field in MANDATORY_FIELDS[run_mode]:
            if field not in params:
                raise ValueError(f"Parameter file is missing the mandatory field '{field}'.")

    md_mode = params.get('MD_mode', DEFAULTS['MD_mode'])
    if md_mode not in ALLOWED_MD_MODES:
        raise ValueError(f"Invalid MD_mode '{md_mode}'. Must be 'sequential' or 'parallel'.")

    bw_notation = params.get('bw_notation', DEFAULTS['bw_notation'])
    if bw_notation == 'True' and 'gpcrdb_file_path' not in params:
        raise ValueError("Parameter 'gpcrdb_file_path' is required when bw_notation is 'True'.")

    if params.get('rank_pockets') == 'True' and 'pockets_file' not in params:
        raise ValueError("Parameter 'pockets_file' is required when rank_pockets is set to 'True'.")


def print_help():
    help_text = f"""
HSDetector - Cholesterol Hot Spot Detection Pipeline (v{VERSION})

Usage:
    HSDetector <parameter_file.prm>
    HSDetector -h | --help
    HSDetector -v | --version

Description:
    This tool performs a full or partial analysis of GPCRs in membrane environments.

Required parameters in the .prm file:
    run_mode            : 'full', 'intermediate', or 'standalone'
    pdb_id              : PDB code for the protein
    starting_structure  : Path to the input PDB file
    mb_comp             : Membrane composition string (e.g., POPC:50,CHOL:50)

Optional parameters:
    n_reps              : Number of replicas (default: 2)
    martinize2_path     : Path to martinize2 (default: "martinize2")
    gmx_path            : Path to gmx binary (default: "gmx")
    output_dir          : Directory for output (default: "./HSDetector_results")
    MD_mode             : 'sequential' or 'parallel' (default: "sequential")
    gpu                 : GPU index (e.g., 0 or 0,1) — required if MD simulations will be performed
    bw_notation         : True/False (default: False) — requires gpcrdb_file_path if True
    gpcrdb_file_path    : Required if bw_notation=True
    rank_pockets        : True/False — if True, pockets_file is required
    pockets_file        : Required for rank_pockets step
    step                : Required if run_mode is 'intermediate' or 'standalone'

Example .prm file:
    run_mode = full
    pdb_id = 1ABC
    starting_structure = /path/to/structure
    n_reps = 2
    mb_comp = POPC:75,CHOL:25
    martinize2_path = martinize2
    gmx_path = gmx
    gpu = 0
    gpcrdb_file_path = /path/to/annotated/structure
    rank_pockets = True
    pockets_file = /path/to/pockets/file
    step = system_build/MD_simulation/analysis/merge_data/rank_pockets
    bw_notation = True
    MD_Mode = sequential
    output_dir = /output/path (Default ./HSDetector_results)

For detailed documentation, visit: https://github.com/orgs/Urbino-CAMD-Lab/HSDetector

"""
    print(help_text)
    sys.exit(0)


def main():
    if len(sys.argv) != 2:
        print("Usage: HSDetector <parameter_file.prm> (or -h for help)")
        sys.exit(1)

    if sys.argv[1] in ['-h', '--help']:
        print_help()

    if sys.argv[1] in ['-v', '--version']:
        print(f"HSDetector version {VERSION}")
        sys.exit(0)

    prm_file = sys.argv[1]

    if not os.path.exists(prm_file):
        print(f"Parameter file '{prm_file}' not found.")
        sys.exit(1)

    try:
        params = parse_prm_file(prm_file)
        validate_parameters(params)
        system_filename_prefix, mb_comp_formatted = get_system_prefix(params['pdb_id'], params['mb_comp'])

        run_mode = params['run_mode']
        if run_mode == 'full':
            run_full_pipeline(params, system_filename_prefix, mb_comp_formatted)
        elif run_mode == 'intermediate':
            run_intermediate_pipeline(params, system_filename_prefix, mb_comp_formatted)
        elif run_mode == 'standalone':
            run_standalone_step(params, system_filename_prefix, mb_comp_formatted)
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()

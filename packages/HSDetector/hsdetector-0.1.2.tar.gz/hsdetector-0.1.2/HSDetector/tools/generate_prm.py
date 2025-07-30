# HSDetector/tools/generate_prm.py

import sys

def generate_prm_file(output_filename="HSDetector_template.prm"):
    template = """run_mode = full
pdb_id = 1ABC
starting_structure = /path/to/structure
n_reps = 2
mb_comp = POPC:75,CHOL:25
martinize2_path = martinize2
gmx_path = gmx
gpu = 0
gpcrdb_file_path = /path/to/annotated/structure
rank_pockets = True/False
pockets_file = /path/to/pockets/file
step = system_build/MD_simulation/analysis/merge_data/rank_pockets
bw_notation = True/False
MD_Mode = sequential
output_dir = /output/path (Default ./HSDetector_results)
"""
    with open(output_filename, "w") as f:
        f.write(template)

    print(f"[INFO] Parameter template written to: {output_filename}")


def main():
    output_filename = "HSDetector_template.prm"  # Default
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    generate_prm_file(output_filename)

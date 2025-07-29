import os
import sys
import MDAnalysis as mda
from MDAnalysis.analysis import align


def align_aa_to_cg(aa, cg):
    """
    Uses a Coarse-Grain structure as reference to align its atomistic structure.
    NOTE: The CG structure should come from that same AA structure, as the alignment works by
    aligning the CA atoms (AA) to the BB atoms (CG), so the same number of particles is expected
    :param aa:
    :param cg:
    :return:
    """
    # Load atomistic and coarse-grain PDBs
    atomistic = mda.Universe(aa)
    coarse_grain = mda.Universe(cg)

    # Select backbone atoms for alignment
    atomistic_selection = atomistic.select_atoms("protein and name CA")  # Atomistic uses C-alpha
    coarse_selection = coarse_grain.select_atoms("protein and name BB")  # CG uses BB

    print(f"🔍 Atomistic selection: {len(atomistic_selection)} atoms selected")
    print(f"🔍 Coarse-grain selection: {len(coarse_selection)} atoms selected")

    alignment = align.alignto(atomistic.atoms,
                              coarse_grain.atoms,
                              select=("name CA", "name BB"),
                              match_atoms=False)

    output_name = f"{os.path.splitext(os.path.basename(aa))[0]}_cg_aligned.pdb"
    print(output_name)
    atomistic.atoms.write(output_name)
    print("✅ Alignment complete, saved.")

    return output_name


if __name__ == "__main__":

    align_aa_to_cg(sys.argv[1], sys.argv[2])

# rank_pockets.py

import os
import glob
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.lib import distances

def _parse_outliers(filepath: str) -> set[str]:
    """Read merged outliers CSV and return a set of ResID strings."""
    df = pd.read_csv(filepath)
    return set(df['ResID'].astype(str).tolist())

def _parse_xyz(filepath: str) -> np.ndarray:
    """Read merged density XYZ and return an (N,3) numpy array of points."""
    coords = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("D"):
                parts = line.split()
                coords.append([float(p) for p in parts[1:4]])
    return np.array(coords)

def rank_pockets(
    system_name: str,
    pocket_file: str,
    merged_outliers_csv: str,
    merged_density_xyz: str,
    distance_cutoff: float = 6.0,
    outlier_weight: int = 1000
) -> pd.DataFrame:
    """
    Rank binding pockets by density proximity and outlier content.

    Parameters
    ----------
    system_name : str
        Base name for outputs, e.g. "7fee".
        Will write "{system_name}_ranked_pockets.csv" and create
        a directory "{system_name}_dens_per_pocket/".
    pocket_file : str
        Path to the pocket definition file, each line a list of ResIDs.
    merged_outliers_csv : str
        Path to merged outliers CSV (must contain a "ResID" column).
    merged_density_xyz : str
        Path to merged density .xyz (lines beginning with "D x y z").
    distance_cutoff : float, optional
        Å cutoff for counting a density point as contributing (default 6.0).
    outlier_weight : int, optional
        Weight (added to score) per outlier residue (default 1000).

    Returns
    -------
    pandas.DataFrame
        DataFrame of pockets sorted by "Total Score" descending.

    Side-effects
    ------------
    - Writes "{system_name}_ranked_pockets.csv"
    - Writes per-pocket XYZ files in "{system_name}_dens_per_pocket/"
    """
    print(f"#####################################\n########## 5. RANK POCKETS ##########\n#####################################\n")
    # ------------------------------------------------------------------------
    # 1) Find any single aligned PDB ending in "_cg_aligned.pdb"
    print(f"~~~~ STEP 1: Retrieve atomistic aligned structure ~~~~\n")
    pattern = "*_cg_aligned.pdb"
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No aligned PDB found matching '{pattern}'")
    if len(matches) > 1:
        raise FileExistsError(f"Multiple aligned PDBs match '{pattern}': {matches}")
    aligned_pdb = matches[0]

    # ------------------------------------------------------------------------
    # 2) Prepare outputs and sanity-check inputs
    print(f"~~~~ STEP 2: Prepare output files ~~~~\n")
    output_csv     = f"{system_name}_ranked_pockets.csv"
    xyz_output_dir = f"{system_name}_dens_per_pocket"
    print(f"[INFO] ranked pockets CSV will be written as {output_csv}\n")
    print(f"[INFO] density points .xyz files will be written to the directory {xyz_output_dir}\n")

    for fp in (pocket_file, merged_outliers_csv, merged_density_xyz):
        if not os.path.isfile(fp):
            raise FileNotFoundError(f"Required file not found: {fp}")

    # ------------------------------------------------------------------------
    # 3) Parse inputs
    print(f"~~~~ STEP 3: Parse inputs ~~~~\n")
    outlier_resids = _parse_outliers(merged_outliers_csv)
    xyz_coords     = _parse_xyz(merged_density_xyz)
    u              = mda.Universe(aligned_pdb)
    all_atoms      = u.atoms

    # ------------------------------------------------------------------------
    # 4) Iterate over pockets, score, and write per-pocket xyz
    print(f"~~~~ STEP 4: Score pockets and write density .xyz ~~~~\n")
    os.makedirs(xyz_output_dir, exist_ok=True)
    records = []

    with open(pocket_file, 'r') as pf:
        for pocket_id, line in enumerate(pf, start=1):
            resid_list = line.split()
            # collect atom indices
            atom_indices = []
            for resid in resid_list:
                sel = all_atoms.select_atoms(f"resid {resid}")
                if len(sel):
                    atom_indices.extend(sel.indices)

            # outlier-based score
            outlier_score = sum(r in outlier_resids for r in resid_list) * outlier_weight

            # density-based score
            if not atom_indices:
                contrib_pts = 0
                coords_in   = np.empty((0, 3))
            else:
                pocket_atoms = all_atoms[atom_indices]
                dmat = distances.distance_array(xyz_coords, pocket_atoms.positions)
                mask = np.any(dmat < distance_cutoff, axis=1)
                contrib_pts = int(mask.sum())
                coords_in   = xyz_coords[mask]

                # write pocket-specific xyz
                out_path = os.path.join(xyz_output_dir, f"pocket_{pocket_id}.xyz")
                with open(out_path, 'w') as w:
                    w.write(f"{len(coords_in)}\n\n")
                    for x, y, z in coords_in:
                        w.write(f"C {x:.3f} {y:.3f} {z:.3f}\n")

            total_score = contrib_pts + outlier_score
            records.append({
                "Pocket id": pocket_id,
                "ResIDs": " ".join(resid_list),
                "Contributing Points": contrib_pts,
                "Outlier Score": outlier_score,
                "Total Score": total_score
            })

    # ------------------------------------------------------------------------
    # 5) Build DataFrame, sort, save, and return
    print(f"~~~~ STEP 5: Create ranked CSV output ~~~~\n")
    df = pd.DataFrame(records).sort_values("Total Score", ascending=False)
    df.to_csv(output_csv, index=False)
    return df

import os
import subprocess
import glob
import pandas as pd
import csv
import fortranformat as ff
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib import distances
from .align_aa2cg import align_aa_to_cg


def merge_outliers_from_replicas(rep_paths, system_name, output_file, bw=False, gpcrdb_file_path=None):
    """
    Merges unique outliers from multiple replicas and optionally annotates them using BW notation
    from a GPCRdb-annotated PDB file (provided in the B-factor of CA atoms).
    """
    bw = str(bw).lower() == "true"
    combined = []
    for rep_path in rep_paths:
        file_path = os.path.join(rep_path, "analysis", f"{system_name}_res_outliers.csv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Outlier file not found: {file_path}")
        df = pd.read_csv(file_path)
        df["Replica"] = os.path.basename(rep_path)
        combined.append(df)

    merged_df = pd.concat(combined, ignore_index=True)
    merged_df["Longest contact (frames)"] = pd.to_numeric(
        merged_df["Longest contact (frames)"], errors="coerce"
    )
    merged_df["ResID"] = merged_df["ResID"].astype(int)
    merged_df = merged_df.sort_values("Longest contact (frames)", ascending=False)
    merged_df = merged_df.drop_duplicates(subset=["ResID"])  # keep highest contact

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        headers = ["Resname", "ResID"]
        if bw:
            headers.append("BW_Notation")
        writer.writerow(headers)

        bw_data = {}
        if bw:
            if gpcrdb_file_path is None:
                raise ValueError("BW annotation enabled but gpcrdb_file_path not provided.")
            pdb_format = ff.FortranRecordReader(
                "(A6,I5,1X,A4,A1,A3,1X,A1,I4,A1,3X,3F8.3,2F6.2,7X,A4,2A2)"
            )
            with open(gpcrdb_file_path, "r") as pdb:
                for line in pdb:
                    if line.startswith("ATOM"):
                        parsed = pdb_format.read(line)
                        atom_name = parsed[2].strip()
                        res_name = parsed[4].strip()
                        res_id = int(parsed[6])
                        b_factor = parsed[12]
                        if atom_name == "CA":
                            try:
                                bw_value = abs(float(b_factor))
                                bw_str = f"{bw_value:.2f}".replace(".", "x")
                                bw_data[(res_id, res_name)] = bw_str
                            except ValueError:
                                continue

        for _, row in merged_df.iterrows():
            resname, resid = row["Resname"], int(row["ResID"])
            entry = [resname, resid]
            if bw:
                entry.append(bw_data.get((resid, resname), ""))
            writer.writerow(entry)

    print(f"Merged outliers written to: {output_file}")


def merge_density_from_replicas(rep_paths, system_name, output_file):
    """
    Merges .xyz density files from multiple replicas into a single merged .xyz file.
    """
    points = set()
    title = None
    for rep_path in rep_paths:
        file_path = os.path.join(rep_path, "analysis", f"{system_name}_all.xyz")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Density file not found: {file_path}")
        with open(file_path, "r") as f:
            lines = f.readlines()
            if title is None and len(lines) > 1:
                title = lines[1].strip()
            for line in lines[2:]:
                parts = line.strip().split()
                # parse as floats for proper coordinates
                point = (float(parts[1]), float(parts[2]), float(parts[3]))
                points.add(point)

    merged_points = sorted(points)
    with open(output_file, "w") as out:
        out.write(f"{len(merged_points)}\n")
        out.write(f"MERGED {title if title else ''}\n")
        for x, y, z in merged_points:
            out.write(f"D {x:.3f} {y:.3f} {z:.3f}\n")

    print(f"Merged density written to: {output_file}")


def extract_last_frame(tpr_file, xtc_file, output_pdb):
    """
    Extracts the last frame of a trajectory using GROMACS.
    """
    cmd = f"echo 1 | gmx_mpi trjconv -s {tpr_file} -f {xtc_file} -o {output_pdb} -dump -1"
    subprocess.run(cmd, shell=True, check=True)
    print(f"Last frame extracted to: {output_pdb}")


def write_outlier_density_pdb(
    cg_aligned_pdb: str,
    merged_outliers_csv: str,
    merged_density_xyz: str,
    output_pdb: str,
    cutoff: float = 6.0
):
    """
    Step 5:
    - Reads `cg_aligned_pdb`, selects ATOM lines with ResIDs from merged_outliers_csv -> chain O
    - Reads merged_density_xyz, finds points within `cutoff` Å of any outlier atom -> write as H atoms
      in a single residue 'DUM', chain D
    - Writes them all to `output_pdb`.
    """
    # load outlier residues
    df = pd.read_csv(merged_outliers_csv)
    outlier_resids = set(df["ResID"].astype(int).tolist())

    # load density points
    xyz = []
    with open(merged_density_xyz) as f:
        for L in f:
            if L.startswith("D"):
                parts = L.split()
                xyz.append((float(parts[1]), float(parts[2]), float(parts[3])))
    xyz = np.array(xyz)

    # load CG-aligned PDB and select outlier atoms
    u = mda.Universe(cg_aligned_pdb)
    outlier_atoms = u.select_atoms(f"resid {' '.join(map(str, outlier_resids))}")
    if not len(outlier_atoms):
        raise RuntimeError("No atoms found for outlier residues in CG-aligned PDB")

    # find density points within cutoff
    dmat = distances.distance_array(xyz, outlier_atoms.positions)
    mask = np.any(dmat <= cutoff, axis=1)
    sel_xyz = xyz[mask]

    # write combined PDB
    with open(cg_aligned_pdb) as f, open(output_pdb, "w") as out:
        atom_serial = 1
        # write outlier ATOMs as chain O
        for L in f:
            if L.startswith("ATOM"):
                resid = int(L[22:26].strip())
                if resid in outlier_resids:
                    rec = L[:6]
                    # atom serial
                    rec += f"{atom_serial:5d}" + L[11:]
                    # chain to O
                    rec = rec[:21] + 'O' + rec[22:]
                    out.write(rec)
                    atom_serial += 1

        # write density points as H in one DUM residue (chain D)
        dum_resid = max(outlier_resids) + 1
        for x, y, z in sel_xyz:
            rec = (
                f"ATOM  {atom_serial:5d} H   DUM D{dum_resid:4d}"  # ATOM, serial, name, resName, chain, resSeq
                f"   {x:8.3f}{y:8.3f}{z:8.3f}"                    # coords
                f"  1.00  0.00          H  \n"                  # occupancy, tempFactor, element
            )
            out.write(rec)
            atom_serial += 1

    print(f"Outlier+Density PDB written to: {output_pdb}")


def run_replica_merge_pipeline(
    system_name,
    working_dir,
    n_reps,
    atomistic_pdb,
    bw="False",
    gpcrdb_file_path=None,
):
    print(
        f"#####################################\n########## 5. MERGE REPLICAS ########\n#####################################\n")
    print("~~~~ Step 1: Merge Outliers ~~~~")
    rep_paths = [os.path.join(working_dir, f"rep_{i+1}") for i in range(int(n_reps))]
    merged_outliers_file = os.path.join(working_dir, f"{system_name}_outliers_MERGE.csv")
    merge_outliers_from_replicas(rep_paths, system_name, merged_outliers_file, bw, gpcrdb_file_path)

    print("~~~~ Step 2: Merge Density ~~~~")
    merged_density_file = os.path.join(working_dir, f"{system_name}_density_MERGE.xyz")
    merge_density_from_replicas(rep_paths, system_name, merged_density_file)

    print("~~~~ Step 3: Extract Last Frame ~~~~")
    tpr_file = os.path.join(rep_paths[0], f"{system_name}_prod.tpr")
    xtc_file = os.path.join(rep_paths[0], "analysis", f"{system_name}_prod_sdf_2.xtc")
    last_frame_file = os.path.join(working_dir, f"{system_name}_lf.pdb")
    extract_last_frame(tpr_file, xtc_file, last_frame_file)

    print("~~~~ Step 4: Align AA to CG ~~~~")
    align_aa_to_cg(atomistic_pdb, last_frame_file)

    print("~~~~ Step 5: Write Hot Spots PDB ~~~~")
    cg_pattern = os.path.join(working_dir, "*_cg_aligned.pdb")
    cg_files = glob.glob(cg_pattern)
    if not cg_files:
        raise FileNotFoundError(f"No CG-aligned PDB found matching {cg_pattern}")
    if len(cg_files) > 1:
        raise FileExistsError(f"Multiple CG-aligned PDBs found: {cg_files}")
    cg_aligned_pdb = cg_files[0]

    output_pdb = os.path.join(working_dir, f"{system_name}_outlier_density.pdb")
    write_outlier_density_pdb(
        cg_aligned_pdb,
        merged_outliers_file,
        merged_density_file,
        output_pdb,
        cutoff=6.0
    )

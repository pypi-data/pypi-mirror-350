# HSDetector/tools/orient_protein.py

import sys
import numpy as np
import MDAnalysis as mda
from scipy.spatial.transform import Rotation as R


def compute_principal_axes(atom_group):
    coords = atom_group.positions
    centroid = np.mean(coords, axis=0)
    centered = coords - centroid
    cov_matrix = np.cov(centered, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov_matrix)
    return eigvecs[:, np.argsort(eigvals)[::-1]]


def get_n_terminal_center(protein, n_residues=5):
    unique_residues = []
    seen = set()
    for res in protein.residues:
        if res.resid not in seen:
            seen.add(res.resid)
            unique_residues.append(res)
        if len(unique_residues) >= n_residues:
            break

    if not unique_residues:
        print("Warning: Couldn't determine N-terminal residues, using fallback.")
        return protein[:10].center_of_geometry()

    n_term_atoms = unique_residues[0].atoms
    for res in unique_residues[1:]:
        n_term_atoms += res.atoms

    return n_term_atoms.center_of_geometry()


def rotate_vector_to_z(vector, target_z=np.array([0, 0, 1])):
    vector = vector / np.linalg.norm(vector)
    if np.allclose(vector, target_z):
        return R.identity()
    if np.allclose(vector, -target_z):
        return R.from_rotvec(np.pi * np.array([1, 0, 0]))
    rot_axis = np.cross(vector, target_z)
    rot_angle = np.arccos(np.clip(np.dot(vector, target_z), -1.0, 1.0))
    return R.from_rotvec(rot_axis / np.linalg.norm(rot_axis) * rot_angle)


def orient_protein(input_pdb, output_pdb=None):
    u = mda.Universe(input_pdb)
    protein = u.select_atoms("protein")

    protein.atoms.positions -= protein.center_of_geometry()

    principal_axes = compute_principal_axes(protein)
    dominant_axis = principal_axes[:, 0]
    n_term_center = get_n_terminal_center(protein)
    current_n_term_projection = np.dot(n_term_center, dominant_axis)

    if current_n_term_projection < 0:
        dominant_axis = -dominant_axis

    rotation = rotate_vector_to_z(dominant_axis)
    protein.atoms.positions = rotation.apply(protein.atoms.positions)

    n_term_center = get_n_terminal_center(protein)
    if n_term_center[2] < 0:
        print("Warning: N-terminus is still pointing toward -Z after rotation. Flipping.")
        flip_rot = R.from_euler('z', 180, degrees=True)
        protein.atoms.positions = flip_rot.apply(protein.atoms.positions)

    if output_pdb is None:
        output_pdb = input_pdb.replace(".pdb", "_oriented.pdb")

    protein.atoms.write(output_pdb)
    print(f"Reoriented protein saved to: {output_pdb}")


def main():
    if len(sys.argv) != 2:
        print("Usage: HSDetector_tools orient_protein input.pdb")
        sys.exit(1)

    input_pdb = sys.argv[1]
    orient_protein(input_pdb)


if __name__ == "__main__":
    main()

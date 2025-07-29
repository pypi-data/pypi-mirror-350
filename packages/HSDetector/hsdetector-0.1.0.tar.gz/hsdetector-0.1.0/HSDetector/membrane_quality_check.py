import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as mda
from MDAnalysis.analysis.density import DensityAnalysis
from lipyphilic.lib.assign_leaflets import AssignLeaflets
from lipyphilic.lib.memb_thickness import MembThickness
from lipyphilic.lib.area_per_lipid import AreaPerLipid
from lipyphilic.lib.order_parameter import SCC


def calculate_membrane_prms(tpr_file, trajectory_file, membrane_composition):
    """Calculate membrane parameters (thickness, APL, order parameters)"""
    resnames = [r.strip() for r in membrane_composition.split(",")]
    phospholipids = [r for r in resnames if r in ["POPC", "DSPC", "POPE", "DPPC", "DOPC"]]

    if not phospholipids:
        raise ValueError("No valid phospholipids found for thickness calculation")

    u = mda.Universe(tpr_file, trajectory_file)

    leaflets = AssignLeaflets(
        universe=u,
        lipid_sel="name GL1 GL2 ROH"
    )
    leaflets.run()

    memb_thickness = MembThickness(
        universe=u,
        leaflets=leaflets.filter_leaflets(f"resname {' '.join(phospholipids)}"),
        lipid_sel=f"resname {' '.join(phospholipids)} and name PO4"
    )
    memb_thickness.run()

    thickness_values = memb_thickness.memb_thickness[~np.isnan(memb_thickness.memb_thickness)]
    if len(thickness_values) == 0:
        raise ValueError("No valid thickness measurements obtained")

    avg_thickness = np.mean(thickness_values)
    std_error_thick = np.std(thickness_values) / np.sqrt(len(thickness_values))

    areas = AreaPerLipid(
        universe=u,
        lipid_sel="name GL1 GL2 ROH",
        leaflets=leaflets.leaflets
    )
    areas.run()

    apl_values = areas.areas[~np.isnan(areas.areas)]
    if len(apl_values) == 0:
        raise ValueError("No valid APL measurements obtained")

    avg_apl = np.mean(apl_values)
    std_error_apl = np.std(apl_values) / np.sqrt(len(apl_values))

    scc_sn1 = SCC(
        universe=u,
        tail_sel="resname POPC and name ??A"
    )
    scc_sn2 = SCC(
        universe=u,
        tail_sel="resname POPC and name ??B"
    )
    scc_sn1.run()
    scc_sn2.run()

    weighted_avg = SCC.weighted_average(scc_sn1, scc_sn2)
    weighted_data = weighted_avg.SCC
    avg_op = np.mean(weighted_data)
    std_error_op = np.std(weighted_data) / np.sqrt(len(weighted_data))

    return avg_thickness, std_error_thick, avg_apl, std_error_apl, avg_op, std_error_op


def calculate_partial_densities(universe, membrane_composition, lipid_dict):
    """Calculate partial densities for system components along Z-axis"""
    resnames = [r.strip() for r in membrane_composition.split(",")]

    # Create atom selections for each component
    selections = {}

    # Water selection - includes all water atoms
    water_sel = universe.select_atoms("resname W")
    if water_sel.n_atoms > 0:
        selections['Water'] = water_sel

    # Protein selection
    protein_sel = universe.select_atoms("protein")
    if protein_sel.n_atoms > 0:
        selections['Protein'] = protein_sel

    # Membrane headgroups
    headgroup_sel_str = " or ".join(
        f"(resname {res} and name {atom})"
        for res in resnames
        if res in lipid_dict
        for atom in lipid_dict[res]['headgroup']
    )
    if headgroup_sel_str:
        headgroup_sel = universe.select_atoms(headgroup_sel_str)
        if headgroup_sel.n_atoms > 0:
            selections['Membrane Headgroups'] = headgroup_sel

    # Membrane tails
    tail_sel_str = " or ".join(
        f"(resname {res} and name {atom})"
        for res in resnames
        if res in lipid_dict
        for atom in lipid_dict[res]['tails']
    )
    if tail_sel_str:
        tail_sel = universe.select_atoms(tail_sel_str)
        if tail_sel.n_atoms > 0:
            selections['Membrane Tails'] = tail_sel

    # Unified grid setup
    all_coords = universe.atoms.positions
    min_coords = all_coords.min(axis=0) - 5.0
    max_coords = all_coords.max(axis=0) + 5.0
    box_size = max_coords - min_coords
    gridcenter = (min_coords + max_coords) / 2

    # Calculate densities
    z_centers = None
    density_profiles = {}

    for name, sel in selections.items():
        try:
            dens = DensityAnalysis(
                sel,
                gridcenter=gridcenter,
                xdim=box_size[0],
                ydim=box_size[1],
                zdim=box_size[2],
                delta=1.0,
                padding=0
            )
            dens.run()

            # Extract Z profile by averaging over x and y
            z_profile = np.mean(dens.results.density.grid, axis=(0, 1))

            # Set z_centers once based on this shared grid
            if z_centers is None:
                z_centers = dens.results.density.edges[2][:-1] + 0.5 * np.diff(dens.results.density.edges[2])

            density_profiles[name] = z_profile

        except Exception as e:
            print(f"Warning: Could not calculate density for {name}: {str(e)}")
            density_profiles[name] = None

    return z_centers, density_profiles


def plot_density_profiles(z_centers, density_profiles, output_dir):
    """
    Plot partial densities and save the file (.png)
    :param z_centers:
    :param density_profiles:
    :param output_dir:
    :return:
    """
    plt.figure(figsize=(10, 6))
    valid_profiles = 0

    for name, profile in density_profiles.items():
        if profile is not None and z_centers is not None:
            plt.plot(z_centers, profile, label=name)
            valid_profiles += 1

    if valid_profiles == 0:
        raise ValueError("No valid density profiles to plot")

    plt.xlabel('Z position (nm)')
    plt.ylabel('Density (g/cm³)')
    plt.title('Partial Density Profiles')
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(output_dir, 'density_profiles.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    return plot_path


def create_output_directory():
    output_dir = "membrane_check"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def write_results_to_file(output_path, composition, thickness, thickness_err, apl, apl_err, op, op_err, density_plot_path=None):
    with open(output_path, 'w') as f:
        f.write("\n=== Membrane Thickness Results ===\n")
        f.write(f"Composition: {composition}\n")
        f.write(f"Average thickness: {thickness:.2f} ± {thickness_err:.2f} Å\n")
        f.write(f"Average APL: {apl:.2f} ± {apl_err:.2f} Å²\n")
        f.write(f"Average Order parameter: {op:.2f} ± {op_err:.2f}\n")
        if density_plot_path:
            f.write(f"\nDensity profiles saved to: {density_plot_path}\n")
        f.write("===============================\n")


def main(tpr_file, trajectory_file, membrane_composition):
    lipid_dict = {
        "POPC": {
            "headgroup": ["NC3", "PO4", "GL1", "GL2"],
            "tails": ["C1A", "D2A", "C3A", "C4A", "C1B", "C2B", "C3B", "C4B"]
        },
        "CHOL": {
            "headgroup": ["ROH"],
            "tails": ["R1", "R2", "R3", "R4", "R5", "R6", "C1", "C2"]
        },
        "DOPC": {
            "headgroup": ["NC3", "PO4", "GL1", "GL2"],
            "tails": ["C1A", "C2A", "C3A", "C4A", "C1B", "C2B", "C3B", "C4B"]
        },
        "POPE": {
            "headgroup": ["NH3", "PO4", "GL1", "GL2"],
            "tails": ["C1A", "C2A", "C3A", "C4A", "C1B", "C2B", "C3B", "C4B"]
        },
        "DPPC": {
            "headgroup": ["NC3", "PO4", "GL1", "GL2"],
            "tails": ["C1A", "C2A", "C3A", "C4A", "C1B", "C2B", "C3B", "C4B"]
        }
    }

    output_dir = create_output_directory()
    output_file = os.path.join(output_dir, "membrane_parameters.info")

    u = mda.Universe(tpr_file, trajectory_file)

    avg_thickness, std_error_thick, avg_apl, std_error_apl, avg_op, std_error_op = calculate_membrane_prms(
        tpr_file, trajectory_file, membrane_composition
    )

    try:
        z_centers, density_profiles = calculate_partial_densities(u, membrane_composition, lipid_dict)
        density_plot_path = plot_density_profiles(z_centers, density_profiles, output_dir)
    except Exception as e:
        print(f"Warning: Density profile calculation failed: {str(e)}")
        density_plot_path = None

    write_results_to_file(
        output_path=output_file,
        composition=membrane_composition,
        thickness=avg_thickness,
        thickness_err=std_error_thick,
        apl=avg_apl,
        apl_err=std_error_apl,
        op=avg_op,
        op_err=std_error_op,
        density_plot_path=density_plot_path
    )

    print(f"\nResults saved to: {output_file}")
    if density_plot_path:
        print(f"Density profiles saved to: {density_plot_path}")
    print("\n=== Membrane Thickness Results ===")
    print(f"Composition: {membrane_composition}")
    print(f"Average thickness: {avg_thickness:.2f} ± {std_error_thick:.2f} Å")
    print(f"Average APL: {avg_apl:.2f} ± {std_error_apl:.2f} Å²")
    print(f"Average Order parameter: {avg_op:.2f} ± {std_error_op:.2f}")
    print("===============================")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python membrane_analysis.py <tpr_file> <trajectory_file> <membrane_composition>")
        print("Example: python membrane_analysis.py system.tpr traj.xtc POPC,CHOL")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

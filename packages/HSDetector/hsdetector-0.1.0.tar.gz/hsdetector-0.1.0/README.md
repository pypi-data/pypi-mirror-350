# HSDetector - Cholesterol Hot Spot Detection Pipeline (v0.1.0)

## Description
HSDetector is a python module aimed to detect potential cholesterol binding sites around membrane proteins. It is mainly tailored to process class A G Protein-Coupled Receptors, but it can theoretically work with other membrane proteins.
This tool is designed to be executed with minimal user input and it requires a <ins>pre-processed</ins>, <ins>membrane-oriented</ins> **PDB** file of a  protein and a file specifying the parameters of the run.
HSDetector relies on the Coarse-Grained Martini 3 representation to carry Molecular Dynamics simulations of the input protein embedded on membranes with cholesterol presence.
Cholesterol hot spots around the protein are detected by analysing the simulated trajectory using two complementary approaches: statistically relevant cholesterol-contacting residues and cholesterol distribution during the MD simulation:
The consensus regions where there is an overlap between statistical outliers and relevant density are considered to be cholesterol hot spots. These regions are reported as a **PDB** file containing the residues considered statistical outliers, as well as the relevant density points associated with them.

## Installation
This package can be installed using the command
```
pip install HSDetector
```

## Inputs
### **Pre-processed PDB file:**
For this tool to work efficiently and to minimise potential errors that could arise from the PDB formatting or the quality of the starting structure it is required to use a PDB that has been properly curated. This means the input structure should be oriented perpendicular to the membrane plane --_aligned to the Z-axis_--, all residues should be complete with no missing atoms and only atoms corresponding to the protein --_no ligands or other HETATM_-- should be present in the PDB.

· Databases such as **OPM** (https://opm.phar.umich.edu/) have a wide variety of already oriented structures that can be used after removing unnecessary atoms.

### **Parameters input file:**
In order to run the protocol several parameters have to be decided in advance and fed to the tool for proper execution.
Below there is an example **.prm** file with all possible parameters that can be set:
```
run_mode = full
step = system_build/MD_simulation/analysis/merge_data/rank_pockets
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
bw_notation = True/False
MD_Mode = sequential
output_dir = /output/path (Default ./HSDetector_results)
```
### MANDATORY PARAMETERS
· **run mode** - The protocol can be run in full or individual steps can be selected. Possible values are: ```full``` or ```standalone```.

· **step** - <ins>Required only if *run_mode=standalone*</ins>. Possible values are: ```system_build```, ```MD_simulation```, ```analysis```, ```merge_data``` or ```rank_pockets```. 

· **pdb_id** - PDB standard 4 character code of the starting structure, e.g. ```7fee```. This is used for the naming of the output, so the use of upper or lowercase is left to preference.

· **mb_comp** - Desired membrane composition. The tool will use insane.py [1] to create the membrane. The format is very specific and HSDetector will either complain or crash if written incorrectly. Correct format is as shown in the example: ```LIP1:[ratio],LIP2:[ratio]```, etc. As in the example ```POPC:75,CHOL:25```. If cholesterol is not selected in the membrane the protocol will not run. On the current version of this software the following phospholipids are supported: POPC, DOPC, DPPC, POPE.

· **gpu** - <ins>Required only if a MD simulation is going to be performed</ins>. Id of the GPU to be used for MD simulations (available GPUs can be checked via ```nvidia-smi``` as long as the CUDA toolkit and NVIDIA(R) drivers are installed).
NOTE: This protocol relies on the CUDA acceleration implemented in GROMACS. If no GPU is available the source code in MDsimulation.py corresponding to GROMACS runs have to be properly modified.

· **starting_structure** - Path to the input structure. Either the relative path --_relative to where the script will be executed from_-- or the absolute path can be used. We recommend the use of absolute paths to avoid confusions.

### OPTIONAL PARAMETERS

· **n_reps** - Nº of replica to create and process (Default: ```2```).

· **martinize2_path** - Martinize 2, included in the Vermouth package [2] is included in the dependencies of this tool and the executable should already be on the PATH. Therfore, its default value is ```martinize2```.

· **gmx_path** - Path to the executable of GROMACS. Default is ```gmx```, assuming the executable is already in PATH. Note that if GROMACS was compiled with MPI support the executable (unless instructed differently during compilation) is created as ```gmx_mpi```, and therefore this parameter needs to be set as such.

· **bw_notation** - If working with GPCRs there is the possibility of annotating the outliers file with the Ballesteros-Weinstein notation adapted from *GPCRdb* [3]. The annotated structure can be downloaded from their database. Possible values: ```True``` or ```False``` (Default is ```False```).

· **gpcrdb_file_path** -  <ins>Required only if bw_notation=True</ins>. Path to the GPCRdb annotated structure. It is assumed that the annotation is on the B-factor column of the PDB --_as GPCRdb does_-- and passing a structure with a different format will lead to errors or unexpected behaviour.

· **MD_mode** - Decides how the MD simulations will be performed. This version of the protocol only supports the value ```sequential```, in which each replica will be performed after the previous finishes. A future version will include the possibility for advanced systems with multiple GPUs to run replicas in parallel.

· **rank_pockets** - HSDetector offers the possibility of ranking a list of pockets detected by an external software based on their propensity to lodge cholesterol by scoring them using the detected outliers and density points. Possible values: ```True``` or ```False``` (Default: ```False```).

· **pockets_file** - <ins>Required only if rank_pockets=True</ins>. Path to the file containing the pockets. It will read pockets in a specific format, so depending on the software utilised the file might need to be adapted. The correct format is a text file, with one pocket per line. Each line should contain the residue IDs conforming the pocket, separated by a single white space. Find an example below, obtained from the Cannabinoid 1 Receptor (PDB:7FEE):
```
201 202 205 208 209 240 243 244 247 282
165 169 191 192 195 198 199 245 248 249 252
138 141 142 148 154 157 158 161 230 234 237 238
280 284 287 288 291 353 356 357 360 361 364
351 354 355 388
```
· **output_dir** - Path to the directory where the output will be saved. If the target directory does not exist it will be created. Default: ```./HSDetector_results```.

## Protocol Steps
A full run of HSDetector will run all the steps detailed below in sequential order. Standalone runs of selected steps can be performed as well. The same **.prm** file can be used for different standalone steps just by adjusting the parameter **step**, as the parameters not used in that step will simply be ignored. However, note that in order to run individual steps, the same directory structure and file naming as used by HSDetector is assumed. It is therefore recommended that individual steps are run on output directories created by HSDetector or adapt the structure and file naming of your data to match what the software expects. An example of the directory structure and the output of a mock run on ```7FEE``` on a ```POPC:75,CHOL:25``` membrane can be found in the example_run/ directory on this repository.

1. **SYSTEM BUILD**

This step of the protocol creates the main structure of the output directories and processes the starting structure. The starting PDB is converted to Coarse-Grain using martinize2 and embedded in a membrane of the defined composition with insane.py. 
HSDetector takes care of copying the necessary inputs and prepare topology files for the simulation step.

2. **MD SIMULATION**

The prepared system undergoes several steps of equilibration before proceeding to the production run.

a) <ins>Energy minimization</ins>: Using steepest descent the total energy of the system is decreased.

b) <ins>Equilibration 1 - NVT</ins>: Short NVT to temper the system to the target 300K

c) <ins>Equilibration 2 - NPT (constrained)</ins>: NPT step with protein backbone atoms restricted. Lipids will adjust and equilibrate.

d) <ins>Equilibration 3 - NPT  (1fs timestep)</ins>:  NPT step simulated at a short timestep to prevent sudden unexpected atom movement when releasing protein restraints.

e) <ins>Equilibration 3 - NPT  (20fs timestep)</ins>:  NPT step simulated at the target 20fs timestep at which the production run takes place.

After the equilibration is completed HSDetector performs a quality check of the membrane, aimed for the user to identify any potential issues arised from the system building and equilibration. For this quality check the membrane thickness, area per lipid and order parameters are calculated. Additionally, a plot showing the partial densities of the membrane components is produced. By comparing obtained values with equivalent ones in the literature, the user can ensure that the produced system is realistic.
	
The production run lasts for 30 $\mu$s, ensuring proper sampling of protein-cholesterol contacts.

3. **ANALYSIS**

As briefly explained in the project Description section, HSDetector uses two approaches to detect cholesterol hot spots.

a) **Protein-cholesterol contacts**: Relevant and persistent contacts across all trajectory frames are extracted --_maximum occupancy time, or t<sub>max<sub>_-- and the statistical outliers in the distribution are reported.

b) **Spatial Density Function**: The probability density map of cholesterol around the protein is calculated and the top 0.01% of the data --_cartesian XYZ coordinates where cholesterol is most likely to be found_-- is reported.

4. **MERGE REPLICAS**

This step simply iterates over all produced replicas and merges all the results, creating a CSV file for all of the statistical outliers found and an XYZ file with the total cholesterol density distribution.

5. **RANK POCKETS**

By providing a correctly formatted file with pockets detected in the structure simulated, HSDetector uses the outliers found and the density points to score and rank them based on their propensity to hold cholesterol.
\- For each outlier found in the residues conforming the pocket the scoring system assigns the pocket 1000 points.
\- For each density point within 6Å of any atom in the pocket the scoring system assigns the pocket 1 point.

## Example Run
In example_outputs/ the files created on a mock run with short MD simulation times can be found. This example was conducted on the **Cannabinoid 1 Receptor** (PDB: *7fee*) using a POPC:75,CHOL:25 membrane.
Note that in order to not overload the repository with heavy files the final production trajectories have been altered to skip keep only every 2nd frame (half of the original frames are kept).
Additionally, the cube file produced by *gmx spatial* is missing from the example for that very same reason. A file ```grid.cube``` should be located in ```{output_dir}/sims/rep_x/analysis/``` after the **analysis** step.
This cube file is the one used to convert its 0.01% top (highest probability) of volumetric data to cartesian coordinates. This information is stored in ```{output_dir}/sims/rep_x/analysis/{system_name}_all.xyz```

## Usage
The correct usage of this tool is quite straightforward, as once it is installed it only requires to run
```
HSDetector prm_file
```
With ```HSDetector -h``` or ```HSDetector --help``` a help message with example parameters and its usage will be printed to STDOUT. The installed version of the HSDetector can be checked by running ```HSDetector -v``` or ```HSDetector --version```.

## HSDetector tools
Together with the main functionality of the package two additional tools are provided that will help on running the protocol.

· ```HSDetector_tools generate_prm``` will generate a template **.prm** file that can then be adapted to users needs. Default name is *HSDetector_template.prm* and will be created where the script is executed. However, custom output name can be given by running ```HSDetector_tools generate_prm output_name```.

· ```HSDetector_tools orient_protein input_structure.pdb``` accepts a pdb file and orients it along the Z-axis. Note that this script was designed for GPCRs and it assumes that only the receptor part of the protein (mostly transmembrane) is present in the PDB. Having other extra or intracellular parts of the protein present will cause the orientation of the principal axis of the protein pore to be incorrectly calculated and the resulting orientation will most likely to be shifted.

## Citations
[1] Tsjerk. (n.d.). Tsjerk/insane: Insert membrane - a simple, versatile tool for building coarse-grained simulation systems. GitHub. https://github.com/Tsjerk/Insane 

[2] Marrink-Lab. (n.d.). Marrink-Lab/Vermouth-Martinize: Describe and apply transformation on molecular structures and Topologies. GitHub. https://github.com/marrink-lab/vermouth-martinize 

[3] Generic residue numbering - GPCRdb 1 documentation. (n.d.). https://docs.gpcrdb.org/generic_numbering.html#:~:text=GPCRdb%20numbers%20are%20distinguished%20by,a%20bulge%20following%20position%2055. 
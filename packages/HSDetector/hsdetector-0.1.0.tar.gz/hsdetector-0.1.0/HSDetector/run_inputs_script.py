import subprocess
import sys
import shlex

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # Python <3.9


def run_insane(args_str):
    """
    Runs insane.py with a command-line argument string.
    Example:
        run_insane("-f structure.pdb -o system.gro -box 5,5,5")
    """
    script_path = files("HSDetector.inputs").joinpath("insane.py")
    full_cmd = f'"{sys.executable}" "{script_path}" {args_str}'

    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"insane.py failed with exit code {result.returncode}")

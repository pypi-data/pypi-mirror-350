# HotSpotDetector/file_copying.py

import os
import shutil

try:
    from importlib.resources import files  # Python 3.9+
except ImportError:
    from importlib_resources import files  # backport for Python <3.9

def copy_inputs_to_cwd():
    target_base = os.getcwd()
    for subdir in ['mdp_files', 'toppar']:
        src_path = files(__package__ + ".inputs").joinpath(subdir)
        dst_path = os.path.join(target_base, subdir)
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)


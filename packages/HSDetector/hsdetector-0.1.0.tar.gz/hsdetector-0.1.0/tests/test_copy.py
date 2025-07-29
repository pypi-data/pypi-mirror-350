import os
import shutil
import tempfile
import pytest

from HSDetector.file_copying import copy_inputs_to_cwd


def test_copy_inputs_to_cwd():
    # Save the original working directory
    orig_cwd = os.getcwd()

    # Use a temporary directory as the working directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            copy_inputs_to_cwd()

            # Check that subdirectories exist
            assert os.path.isdir("mdp_files"), "mdp_files folder was not copied"
            assert os.path.isdir("toppar"), "toppar folder was not copied"

            # Optional: Check at least one file exists in each (if you know file names)
            mdp_files = os.listdir("mdp_files")
            toppar_files = os.listdir("toppar")
            assert mdp_files, "mdp_files is empty"
            assert toppar_files, "toppar is empty"

        finally:
            os.chdir(orig_cwd)

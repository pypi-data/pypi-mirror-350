# tests/test_main.py
import sys
import pytest
from unittest import mock
from io import StringIO

import HSDetector.main as main  # This assumes your main script is named main.py at the top level

def test_help_output(capsys):
    test_args = ["main.py", "-h"]
    with mock.patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):  # Because main.py calls sys.exit()
            main.main()
        captured = capsys.readouterr()
        assert "HSDetector" in captured.out
        assert "Usage" in captured.out

def test_version_output(capsys):
    test_args = ["main.py", "--version"]
    with mock.patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            main.main()
        captured = capsys.readouterr()
        assert "version" in captured.out

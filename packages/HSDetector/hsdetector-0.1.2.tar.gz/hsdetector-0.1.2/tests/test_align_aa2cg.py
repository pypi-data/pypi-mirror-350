import unittest
from unittest import mock
import os

from HSDetector import align_aa2cg


class TestAlignAA2CG(unittest.TestCase):
    @mock.patch("HSDetector.align_aa2cg.mda.Universe")
    @mock.patch("HSDetector.align_aa2cg.align.alignto")
    def test_align_aa_to_cg(self, mock_alignto, mock_universe):
        # Setup mocks
        mock_atomistic = mock.Mock()
        mock_coarse = mock.Mock()

        mock_atomistic.select_atoms.return_value = [1, 2, 3]
        mock_coarse.select_atoms.return_value = [1, 2, 3]
        mock_atomistic.atoms = mock.Mock()
        mock_atomistic.atoms.write = mock.Mock()

        mock_coarse.atoms = mock.Mock()

        # Configure Universe mock to return our fake Universes
        mock_universe.side_effect = [mock_atomistic, mock_coarse]

        # Inputs
        aa_path = "test_aa.pdb"
        cg_path = "test_cg.pdb"
        expected_output = "test_aa_cg_aligned.pdb"

        # Run the function
        output = align_aa2cg.align_aa_to_cg(aa_path, cg_path)

        # Assertions
        self.assertEqual(output, expected_output)
        mock_universe.assert_any_call(aa_path)
        mock_universe.assert_any_call(cg_path)
        mock_alignto.assert_called_once()
        mock_atomistic.atoms.write.assert_called_once_with(expected_output)


if __name__ == "__main__":
    unittest.main()

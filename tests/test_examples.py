"""Smoke tests for example scripts."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_SCRIPT = REPO_ROOT / "examples" / "example.py"


class TestExamples(unittest.TestCase):
    def test_example_script_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(EXAMPLE_SCRIPT)],
                cwd=tmp,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=result.stderr or result.stdout,
            )
            self.assertTrue((Path(tmp) / "veriloga.va").exists())
            self.assertTrue((Path(tmp) / "eqs.csv").exists())
            self.assertTrue((Path(tmp) / "eqs.ocn").exists())


if __name__ == "__main__":
    unittest.main()

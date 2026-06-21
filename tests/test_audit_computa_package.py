import subprocess
import sys
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "audit_computa_package.py"


class ComputaPackageAuditTests(unittest.TestCase):
    def test_package_audit_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            cwd=str(REPO),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

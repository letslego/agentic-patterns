import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_DIRS = sorted(ROOT.glob("code/*/main.py"))


def test_all_examples_run():
    for main_py in CODE_DIRS:
        result = subprocess.run(
            [sys.executable, str(main_py)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"{main_py} failed:\n{result.stderr}"

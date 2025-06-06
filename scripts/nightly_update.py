import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.pipeline import run_nightly_update

if __name__ == "__main__":
    run_nightly_update()

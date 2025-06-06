import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from src.dashboard import run_dashboard

if __name__ == "__main__":
    run_dashboard()

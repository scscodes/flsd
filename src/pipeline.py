import pandas as pd
from pathlib import Path
from .utils.paths import get_data_path


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file from the given path."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Simple cleanup operations used by nightly pipeline."""
    df = df.drop_duplicates()
    return df.fillna(0)


def save_processed(df: pd.DataFrame, name: str = "latest.csv") -> Path:
    out_dir = get_data_path("processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / name
    df.to_csv(out_file, index=False)
    return out_file


def run_nightly_update() -> None:
    """Process the most recent uploaded CSV and store it as processed data."""
    raw_dir = get_data_path("raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    uploads = list(raw_dir.glob("*.csv"))
    if not uploads:
        print("No CSV uploads found in data/raw")
        return
    latest = max(uploads, key=lambda p: p.stat().st_mtime)
    df = load_csv(latest)
    processed = clean_data(df)
    out_file = save_processed(processed)
    print(f"Processed data saved to {out_file}")

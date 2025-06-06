import pandas as pd
import streamlit as st
from .utils.paths import get_data_path


def run_dashboard() -> None:
    processed_file = get_data_path("processed") / "latest.csv"
    st.title("FLSD Financial Dashboard")
    if processed_file.exists():
        df = pd.read_csv(processed_file)
        st.write("Latest processed data:")
        st.dataframe(df.head())
    else:
        st.warning("No processed data found. Upload a CSV to data/raw and run the nightly update.")


if __name__ == "__main__":
    run_dashboard()

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
from src.utils.paths import get_data_path


def load_latest_data(data_type=None):
    """
    Load the latest processed data.
    
    Args:
        data_type: If provided, load data for specific type
        
    Returns:
        DataFrame with the data or None if not found
    """
    processed_dir = get_data_path("processed")
    
    if data_type:
        # Find the latest file for the specified type
        files = list(processed_dir.glob(f"{data_type}_*.csv"))
        if not files:
            return None
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
    else:
        # Default to latest.csv if no type specified
        latest_file = processed_dir / "latest.csv"
        if not latest_file.exists():
            return None
    
    return pd.read_csv(latest_file)


def display_financial_data(df):
    """Display financial data with appropriate visualizations"""
    st.subheader("Financial Data Overview")
    
    # Check for expected columns
    if 'date' in df.columns and 'amount' in df.columns:
        # Convert date column if needed
        if not pd.api.types.is_datetime64_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Display summary metrics
        total = df['amount'].sum()
        avg = df['amount'].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Amount", f"${total:,.2f}")
        col2.metric("Average Amount", f"${avg:,.2f}")
        
        # Line chart for amounts over time
        fig = px.line(
            df, 
            x='date', 
            y='amount',
            title='Financial Amounts Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Running total if available
        if 'running_total' in df.columns:
            fig = px.line(
                df, 
                x='date', 
                y='running_total',
                title='Running Total Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Financial data missing expected columns (date, amount)")
    
    # Always show the raw data
    st.subheader("Raw Data")
    st.dataframe(df)


def display_market_data(df):
    """Display market data with appropriate visualizations"""
    st.subheader("Market Data Overview")
    
    # Check for expected columns
    if 'date' in df.columns and 'price' in df.columns:
        # Convert date column if needed
        if not pd.api.types.is_datetime64_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Display summary metrics
        latest_price = df['price'].iloc[-1] if not df.empty else 0
        price_change = df['price'].iloc[-1] - df['price'].iloc[0] if len(df) > 1 else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Latest Price", f"${latest_price:,.2f}")
        col2.metric("Price Change", f"${price_change:,.2f}", f"{price_change/df['price'].iloc[0]*100:.2f}%" if len(df) > 1 else "0%")
        
        # Candlestick chart if OHLC data is available
        if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
            fig = go.Figure(data=[go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            )])
            fig.update_layout(title='Price Movement (OHLC)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Simple line chart for price
            fig = px.line(
                df, 
                x='date', 
                y='price',
                title='Price Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Percent change chart if available
        if 'pct_change' in df.columns:
            fig = px.bar(
                df, 
                x='date', 
                y='pct_change',
                title='Daily Percent Change'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Market data missing expected columns (date, price)")
    
    # Always show the raw data
    st.subheader("Raw Data")
    st.dataframe(df)


def display_forecast_data(df):
    """Display forecast data with appropriate visualizations"""
    st.subheader("Forecast Data Overview")
    
    # Check for expected columns
    if 'date' in df.columns and 'prediction' in df.columns:
        # Convert date column if needed
        if not pd.api.types.is_datetime64_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Split into historical and forecast
        today = pd.Timestamp.now().normalize()
        historical = df[df['date'] <= today]
        forecast = df[df['date'] > today]
        
        # Display summary metrics
        latest_value = historical['prediction'].iloc[-1] if not historical.empty else 0
        forecast_value = forecast['prediction'].iloc[-1] if not forecast.empty else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Latest Value", f"{latest_value:,.2f}")
        col2.metric("Forecast End Value", f"{forecast_value:,.2f}")
        
        # Combined historical and forecast chart
        fig = go.Figure()
        
        if not historical.empty:
            fig.add_trace(go.Scatter(
                x=historical['date'], 
                y=historical['prediction'],
                mode='lines',
                name='Historical',
                line=dict(color='blue')
            ))
            
        if not forecast.empty:
            fig.add_trace(go.Scatter(
                x=forecast['date'], 
                y=forecast['prediction'],
                mode='lines',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
        fig.update_layout(title='Historical Data and Forecast')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Forecast data missing expected columns (date, prediction)")
    
    # Always show the raw data
    st.subheader("Raw Data")
    st.dataframe(df)


def run_dashboard() -> None:
    """Run the Streamlit dashboard application"""
    st.set_page_config(
        page_title="FLSD Financial Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("FLSD Financial Dashboard")
    st.sidebar.title("Navigation")
    
    # Data type selection
    data_type = st.sidebar.radio(
        "Select Data Type",
        ["financial", "market", "forecast", "latest"]
    )
    
    if data_type == "latest":
        st.subheader("Latest Processed Data")
        df = load_latest_data()
        
        if df is not None:
            st.write("Latest processed data:")
            st.dataframe(df)
        else:
            st.warning("No processed data found. Upload a CSV to data/raw and run the nightly update.")
    else:
        # Load specific data type
        df = load_latest_data(data_type)
        
        if df is not None:
            # Display based on data type
            if data_type == "financial":
                display_financial_data(df)
            elif data_type == "market":
                display_market_data(df)
            elif data_type == "forecast":
                display_forecast_data(df)
        else:
            st.warning(f"No {data_type} data found. Upload a CSV with the {data_type}_*.csv naming convention.")
    
    # Show upload instructions
    with st.sidebar.expander("Upload Instructions"):
        st.write("""
        To add new data:
        1. Use the API endpoint: POST /upload/
        2. Name your file following the convention: {type}_{description}_{date}.csv
        3. Supported types: financial, market, forecast
        
        Example: financial_quarterly_20231231.csv
        """)
    
    # Add timestamp to show last update
    st.sidebar.markdown("---")
    st.sidebar.text(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    run_dashboard()

import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
from .utils.paths import get_data_path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file from the given path."""
    logger.info(f"Loading CSV from {path}")
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Simple cleanup operations used by all pipelines."""
    logger.info("Performing basic data cleaning")
    df = df.drop_duplicates()
    return df.fillna(0)


def save_processed(df: pd.DataFrame, name: str = "latest.csv", data_type: str = None) -> Path:
    """
    Save processed dataframe to the processed directory.
    
    Args:
        df: The dataframe to save
        name: The filename to save as
        data_type: The type of data (to be used in filename prefix)
        
    Returns:
        Path to the saved file
    """
    out_dir = get_data_path("processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # If data_type is provided, create a type-specific filename
    if data_type:
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{data_type}_{timestamp}_{name}"
    else:
        filename = name
    
    out_file = out_dir / filename
    logger.info(f"Saving processed data to {out_file}")
    df.to_csv(out_file, index=False)
    
    # Also save as latest.csv for the dashboard
    latest_file = out_dir / "latest.csv"
    df.to_csv(latest_file, index=False)
    logger.info(f"Also saved as {latest_file} for dashboard")
    
    return out_file


def process_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process financial data with specific operations.
    
    This pipeline performs:
    1. Basic cleaning
    2. Financial-specific calculations
    """
    logger.info("Processing financial data")
    
    # Basic cleaning
    df = clean_data(df)
    
    # Financial-specific processing
    # Check if expected columns exist
    required_columns = ['date', 'amount']
    
    # If columns don't exist, we'll just log a warning but continue
    if not all(col in df.columns for col in required_columns):
        logger.warning("Financial data missing required columns: date, amount")
    else:
        # Ensure date column is properly formatted
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
                logger.info("Converted date column to datetime")
            except Exception as e:
                logger.warning(f"Could not convert date column: {str(e)}")
        
        # Calculate running totals if amount column exists
        if 'amount' in df.columns:
            df['running_total'] = df['amount'].cumsum()
            logger.info("Added running_total column")
    
    return df


def process_market_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process market data with specific operations.
    
    This pipeline performs:
    1. Basic cleaning
    2. Market-specific calculations (like percent changes)
    """
    logger.info("Processing market data")
    
    # Basic cleaning
    df = clean_data(df)
    
    # Market-specific processing
    # Check for typical market data columns
    if 'price' in df.columns and 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df['pct_change'] = df['price'].pct_change() * 100
            logger.info("Calculated percent change in prices")
        except Exception as e:
            logger.warning(f"Error processing market data: {str(e)}")
    else:
        logger.warning("Market data missing expected columns: date, price")
    
    return df


def process_forecast_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process forecast data with specific operations.
    
    This pipeline performs:
    1. Basic cleaning
    2. Forecast-specific validations
    """
    logger.info("Processing forecast data")
    
    # Basic cleaning
    df = clean_data(df)
    
    # Forecast-specific processing
    if 'prediction' in df.columns and 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            # Ensure predictions are for future dates
            today = pd.Timestamp.now().normalize()
            future_mask = df['date'] > today
            
            if not future_mask.any():
                logger.warning("Forecast data contains no future dates")
            else:
                logger.info(f"Forecast contains {future_mask.sum()} future predictions")
        except Exception as e:
            logger.warning(f"Error processing forecast data: {str(e)}")
    else:
        logger.warning("Forecast data missing expected columns: date, prediction")
    
    return df


def process_file_by_type(file_path: Path, data_type: str) -> Path:
    """
    Process a file based on its data type.
    
    Args:
        file_path: Path to the raw CSV file
        data_type: Type of data to determine processing pipeline
        
    Returns:
        Path to the processed output file
    """
    logger.info(f"Processing file {file_path} as {data_type} data")
    
    # Load the data
    df = load_csv(file_path)
    
    # Process based on type
    if data_type == "financial":
        processed_df = process_financial_data(df)
        output_name = "financial_data.csv"
    elif data_type == "market":
        processed_df = process_market_data(df)
        output_name = "market_data.csv"
    elif data_type == "forecast":
        processed_df = process_forecast_data(df)
        output_name = "forecast_data.csv"
    else:
        # Default processing for unknown types
        logger.warning(f"Unknown data type: {data_type}, applying default processing")
        processed_df = clean_data(df)
        output_name = "custom_data.csv"
    
    # Save the processed data
    output_file = save_processed(processed_df, output_name, data_type)
    return output_file


def run_nightly_update() -> None:
    """Process the most recent uploaded CSV and store it as processed data."""
    logger.info("Running nightly update")
    raw_dir = get_data_path("raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    uploads = list(raw_dir.glob("*.csv"))
    
    if not uploads:
        logger.warning("No CSV uploads found in data/raw")
        return
    
    latest = max(uploads, key=lambda p: p.stat().st_mtime)
    logger.info(f"Processing latest file: {latest}")
    
    # Try to determine data type from filename
    parts = latest.stem.split('_')
    if len(parts) >= 1 and parts[0] in ["financial", "market", "forecast"]:
        data_type = parts[0]
        logger.info(f"Detected data type from filename: {data_type}")
    else:
        data_type = "unknown"
        logger.info("Could not determine data type from filename, using default processing")
    
    # Process the file based on its type
    output_file = process_file_by_type(latest, data_type)
    logger.info(f"Processed data saved to {output_file}")

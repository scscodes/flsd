# FLSD Financial Dashboard

A financial data processing pipeline and dashboard system.

## Features

- **API-Based Data Submission**: Upload CSV files via API endpoint
- **Smart Data Processing**: Automatic processing based on data type
- **Interactive Dashboard**: Visualize and explore processed data
- **Type-Specific Visualizations**: Different visualizations for financial, market, and forecast data

## Getting Started

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```
3. Choose one of these installation methods:

   **Option 1: Install using requirements.txt (Recommended for Development)**
   ```
   pip install -r requirements.txt
   ```

   **Option 2: Install as a package**
   ```
   pip install -e .
   ```
   This will install the project as an editable package with command-line tools:
   - `flsd-run`: Run both API and dashboard
   - `flsd-api`: Run only the API server
   - `flsd-dashboard`: Run only the dashboard
   - `flsd-pipeline`: Run the nightly update pipeline

### Running the Application

Run both the API server and dashboard:

```
python -m src.run_services
```

This will start:
- FastAPI server on http://localhost:8000
- Streamlit dashboard on http://localhost:8501

## Data Pipeline

### File Naming Convention

Files should follow this naming pattern:
```
{type}_{description}_{date}.csv
```

Where:
- `type`: Determines processing pipeline (financial, market, forecast)
- `description`: Brief data description
- `date`: Date in YYYYMMDD format

Examples:
- `financial_quarterly_20231231.csv`
- `market_stocks_20240415.csv`
- `forecast_revenue_20240630.csv`

### API Usage

Upload a file:
```
curl -X POST -F "file=@your_file.csv" http://localhost:8000/upload/
```

Or use the Swagger UI at http://localhost:8000/docs

### Expected Data Formats

#### Financial Data
- Required columns: `date`, `amount`
- Optional columns: any additional financial metrics

#### Market Data
- Required columns: `date`, `price`
- Optional OHLC data: `open`, `high`, `low`, `close`

#### Forecast Data
- Required columns: `date`, `prediction`
- Should include both historical and future dates

## Dashboard

The dashboard automatically visualizes the latest data with type-specific visualizations:

- **Financial**: Line charts for amounts and running totals
- **Market**: Price charts, percent change analysis, and OHLC if available
- **Forecast**: Combined historical and forecast visualizations

For details on downloading nightly processed data and sharing the dashboard publicly, see [docs/streamlit_deploy.md](docs/streamlit_deploy.md).

## Directory Structure

```
flsd/
  ├── data/
  │   ├── raw/        # Raw uploaded CSV files
  │   └── processed/  # Processed data files
  ├── scripts/
  │   └── nightly_update.py  # Script for running nightly updates
  ├── src/
  │   ├── utils/      # Utility functions
  │   ├── api.py      # FastAPI server
  │   ├── dashboard.py # Streamlit dashboard
  │   ├── pipeline.py # Data processing logic
  │   └── run_services.py # Run both API and dashboard
  ├── requirements.txt
  ├── setup.py        # Package installation configuration
  └── README.md
```

### Package Installation

The project can be installed as a package, which provides command-line tools for easier usage. To install it in development mode:

```
pip install -e .
```

This will make the following commands available:
- `flsd-run`: Run both API and dashboard
- `flsd-api`: Run only the API server
- `flsd-dashboard`: Run only the dashboard
- `flsd-pipeline`: Run the nightly update pipeline

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License.

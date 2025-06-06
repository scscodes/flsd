# FLSD Financial Analysis

Financial analysis and forecasting tools for the Fort Lauderdale School District (FLSD). This project provides data visualization and scenario analysis tools to help understand and plan for the district's financial future.

## Features

- Revenue and expenditure forecasting
- Expenditure breakdown analysis
- Purchased services analysis
- Scenario planning and impact analysis
- Interactive visualizations using Plotly

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flsd.git
cd flsd
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The project contains Jupyter notebooks for different analyses:

- `grok.ipynb`: Main financial analysis and forecasting
- `scenario_analysis.ipynb`: Detailed analysis of purchased services and scenario planning

To run the notebooks:
```bash
jupyter notebook
```

## Data

The analysis uses sample financial data for demonstration purposes. In a production environment, this would be replaced with actual district financial data.

## Automated Dashboard & Pipeline

The repository includes a simple nightly pipeline that processes uploaded CSV files and stores the cleaned result in `data/processed/latest.csv`. Upload your raw files to `data/raw/` and the pipeline will pick up the most recent one.

A GitHub Actions workflow (`.github/workflows/nightly.yml`) runs `scripts/nightly_update.py` every night at 2 AM UTC. It installs dependencies and processes the latest upload.

To run the update locally:
```bash
python scripts/nightly_update.py
```

### Streamlit Configuration

A basic Streamlit app (`src/dashboard.py`) can display the processed data. To use it, create the Streamlit configuration directory:
```bash
mkdir -p ~/.streamlit
```
Add a `config.toml` with your preferred settings, for example:
```toml
[server]
headless = true
```
Run the dashboard with:
```bash
streamlit run src/dashboard.py
```

## License

MIT License

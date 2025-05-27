# PowerShell script to set up the data science project environment

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path ".\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Green
pip install -r requirements.txt
pip install -e .

# Create a sample .gitignore file if it doesn't exist
if (-not (Test-Path -Path ".\.gitignore")) {
    Write-Host "Creating .gitignore file..." -ForegroundColor Green
    @"
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
ENV/

# Distribution / packaging
dist/
build/
*.egg-info/

# Jupyter Notebook
.ipynb_checkpoints

# Data files (optional, uncomment if you don't want to version data)
# data/raw/
# data/processed/
# data/external/

# Reports and figures
reports/figures/

# OS specific files
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore"
}

Write-Host "Project setup complete!" -ForegroundColor Green
Write-Host "To start Jupyter Lab, run: jupyter lab" -ForegroundColor Cyan 
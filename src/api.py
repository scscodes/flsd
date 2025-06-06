"""
API service for data pipeline interactions.
"""

import os
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
import uvicorn

from src.utils.paths import get_data_path
from src.pipeline import process_file_by_type

app = FastAPI(title="FLSD Data Pipeline API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file to be processed by the pipeline.
    
    The file should follow naming convention: {type}_{description}_{date}.csv
    Where:
    - type: Determines the processing pipeline (e.g., "financial", "market", "forecast")
    - description: Brief description of the data
    - date: Date in YYYYMMDD format
    
    Example: financial_quarterly_20231231.csv
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    # Parse filename to determine processing type
    try:
        filename = file.filename
        parts = filename.split('_')
        
        if len(parts) < 3:
            raise HTTPException(
                status_code=400, 
                detail="Filename should follow convention: {type}_{description}_{date}.csv"
            )
            
        data_type = parts[0].lower()
        
        # Create unique temp filename for storage
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        temp_filename = f"{data_type}_{timestamp}_{unique_id}.csv"
        
        # Save uploaded file to raw directory
        raw_dir = get_data_path("raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        file_path = raw_dir / temp_filename
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # Process the file based on its type
        result = process_file_by_type(file_path, data_type)
        
        return {
            "filename": filename,
            "saved_as": temp_filename,
            "type": data_type,
            "processed_file": str(result),
            "status": "success"
        }
        
    except Exception as e:
        # Log the error
        print(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")

@app.get("/data/types")
async def get_data_types():
    """Get available data processing types"""
    return {
        "data_types": [
            "financial", 
            "market", 
            "forecast"
        ],
        "naming_convention": "{type}_{description}_{date}.csv"
    }

@app.get("/data/latest/{data_type}")
async def get_latest_data(data_type: str):
    """Get information about the latest processed data for a specific type"""
    processed_dir = get_data_path("processed")
    try:
        files = list(processed_dir.glob(f"{data_type}_*.csv"))
        if not files:
            return {"status": "no_data", "message": f"No processed data found for type: {data_type}"}
            
        latest = max(files, key=lambda p: p.stat().st_mtime)
        return {
            "status": "success",
            "filename": latest.name,
            "last_modified": datetime.fromtimestamp(latest.stat().st_mtime).isoformat(),
            "size_bytes": latest.stat().st_size
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def start_api(host="0.0.0.0", port=8000):
    """Start the API server"""
    uvicorn.run("src.api:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    start_api() 
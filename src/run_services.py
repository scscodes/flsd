"""
Script to run all project services (API and Dashboard).
"""

import os
import subprocess
import threading
import time
import signal
import sys
from pathlib import Path

def run_api_server():
    """Run the FastAPI server"""
    print("Starting API server...")
    return subprocess.Popen(
        [sys.executable, "-m", "src.api"],
        env=dict(os.environ, PYTHONPATH=str(Path.cwd()))
    )

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("Starting Streamlit dashboard...")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/dashboard.py"],
        env=dict(os.environ, PYTHONPATH=str(Path.cwd()))
    )

def main():
    """Start all services and handle graceful shutdown"""
    try:
        # Create necessary directories
        from src.utils.paths import get_data_path
        raw_dir = get_data_path("raw")
        processed_dir = get_data_path("processed")
        raw_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Start the services
        api_process = run_api_server()
        # Give the API a moment to start
        time.sleep(2)
        dashboard_process = run_dashboard()
        
        print("\n" + "="*50)
        print(" Services running! Access them at:")
        print(" - API: http://localhost:8000/docs")
        print(" - Dashboard: http://localhost:8501")
        print("="*50 + "\n")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down services...")
    finally:
        # Ensure all subprocesses are terminated
        for process in [p for p in [api_process, dashboard_process] if p]:
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception as e:
                print(f"Error terminating process: {e}")
                try:
                    process.kill()
                except:
                    pass
        print("All services stopped.")

if __name__ == "__main__":
    main() 
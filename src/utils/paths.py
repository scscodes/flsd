"""
Utility functions for managing file paths in the project.
"""

import os
from pathlib import Path

def get_project_root():
    """Return the absolute path to the project root directory."""
    # This assumes the paths.py file is in src/utils
    return Path(__file__).parent.parent.parent.absolute()

def get_data_path(subfolder=None):
    """
    Return the path to the data directory or a subdirectory.
    
    Args:
        subfolder (str, optional): Subdirectory within the data directory.
            Can be 'raw', 'processed', or 'external'. Defaults to None.
            
    Returns:
        Path: Path object pointing to the requested directory
    """
    root = get_project_root()
    data_path = root / 'data'
    
    if subfolder:
        if subfolder in ['raw', 'processed', 'external']:
            return data_path / subfolder
        else:
            raise ValueError(f"Invalid subfolder: {subfolder}. Use 'raw', 'processed', or 'external'.")
    
    return data_path

def get_notebooks_path():
    """Return the path to the notebooks directory."""
    return get_project_root() / 'notebooks'

def get_reports_path(figures=False):
    """
    Return the path to the reports directory or figures subdirectory.
    
    Args:
        figures (bool, optional): If True, returns path to figures subdirectory.
            Defaults to False.
            
    Returns:
        Path: Path object pointing to the requested directory
    """
    reports_path = get_project_root() / 'reports'
    return reports_path / 'figures' if figures else reports_path 
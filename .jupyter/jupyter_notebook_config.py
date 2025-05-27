"""
Configuration file for Jupyter Notebook.
"""

# Set the default directory where notebooks are opened
c.NotebookApp.notebook_dir = 'notebooks'

# Don't open a browser window by default
c.NotebookApp.open_browser = False

# Allow remote access
c.NotebookApp.ip = '0.0.0.0'

# Use a custom port
c.NotebookApp.port = 8888

# Enable autosave
c.FileContentsManager.autosave_interval = 120  # seconds 
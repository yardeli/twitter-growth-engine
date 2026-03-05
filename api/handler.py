import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import Flask app from the parent api.py
from api import app as application

# Vercel expects the app to be called 'app'
app = application

"""
WSGI entry point for Vercel deployment
"""
import sys
import os

# Ensure we can import from the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import app

if __name__ == "__main__":
    app.run()

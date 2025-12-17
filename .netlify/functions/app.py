import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
import serverless_wsgi

def handler(event, context):
    """Netlify Functions handler using serverless-wsgi"""
    return serverless_wsgi.handle_request(app, event, context)


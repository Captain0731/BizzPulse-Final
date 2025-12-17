import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app with explicit template folder
app = Flask(__name__, template_folder='templates')

# Configuration
app.secret_key = os.environ.get("SESSION_SECRET", "fallback_super_secret_key_123")

# Only use ProxyFix if not on Vercel (Vercel handles this automatically)
if not os.environ.get("VERCEL"):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback for local development only
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# CSRF Protection
csrf = CSRFProtect(app)

# Initialize the app with the extension
db.init_app(app)

from routes import *  # noqa: F401, F403

def init_app():
    """Initialize the application and database"""
    try:
        with app.app_context():
            # Import models after app initialization
            from models import Contact, Newsletter
            
            # Only create tables if DATABASE_URL is set and not SQLite
            database_url = os.environ.get("DATABASE_URL", "")
            if database_url and not database_url.startswith("sqlite"):
                try:
                    db.create_all()
                    app.logger.info("Database tables created successfully")
                except Exception as e:
                    app.logger.warning(f"Database initialization failed: {str(e)}")
            else:
                app.logger.warning("DATABASE_URL not set or using SQLite. Database features may not work.")
    except Exception as e:
        app.logger.error(f"App initialization error: {str(e)}")
        # Don't fail the app startup, just log the error

# Initialize app for Vercel (with error handling)
try:
    init_app()
except Exception as e:
    logging.error(f"Failed to initialize app: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
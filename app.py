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
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# CSRF Protection
csrf = CSRFProtect(app)

# Initialize the app with the extension
db.init_app(app)

from routes import *  # noqa: F401, F403

def init_app():
    with app.app_context():
        # Import models after app initialization
        from models import Contact, Newsletter
        
        # Create all database tables
        db.create_all()
        
        app.logger.info("Database tables created successfully")

# Initialize app for Vercel
init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
csrf = CSRFProtect()

def create_app(config_name='production'):
    """Application factory pattern"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load config
    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    with app.app_context():
        from routes_refactored import main_bp, api_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp, url_prefix='/api')
        
        # Create tables if needed
        try:
            from models import Contact, Newsletter
            db.create_all()
            logger.info("Database tables verified/created")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    return app

# For Railway/Production
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)


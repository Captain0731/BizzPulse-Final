"""
WSGI entry point for Render deployment
"""
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app_refactored import app
    logger.info("✓ App imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import app: {e}")
    raise

# Verify app has routes
if app:
    logger.info(f"✓ App created with {len(app.url_map._rules)} routes")
    for rule in app.url_map.iter_rules():
        logger.info(f"  Route: {rule.rule} -> {rule.endpoint}")

# Export for gunicorn
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


#!/usr/bin/env python3
# ============================================================================
# SBRBIOFORGE - Environmental Intelligence Platform
# Integrated with SBRCORE Foundation
# ============================================================================

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SBRCORE
from sbrcore.config import Config
from sbrcore.database import DatabaseConnection, run_migrations
from sbrcore.logging import get_logger, setup_logging
from sbrcore.api.errors import SBRException

# Setup logging
setup_logging(Config.LOG_LEVEL)
logger = get_logger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='build/web', static_url_path='')
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['ENV'] = Config.ENV
app.config['DEBUG'] = Config.DEBUG

# Initialize Database
try:
    DatabaseConnection.initialize(Config.DATABASE_URL, echo=Config.DEBUG)
    run_migrations()
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {str(e)}")
    raise

# =====================================================================
# GLOBAL ERROR HANDLER
# =====================================================================

@app.errorhandler(SBRException)
def handle_sbr_exception(error):
    """Handle SBRCORE exceptions"""
    response = {
        'success': False,
        'error': {
            'message': error.message,
            'code': error.code
        }
    }
    return jsonify(response), error.status_code

@app.errorhandler(Exception)
def handle_generic_exception(error):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {str(error)}")
    response = {
        'success': False,
        'error': {
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }
    }
    return jsonify(response), 500

# =====================================================================
# HEALTH CHECK ENDPOINT
# =====================================================================

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        'status': 'healthy',
        'service': 'SBRBIOFORGE',
        'version': '1.0.0',
        'environment': Config.ENV
    }), 200

# =====================================================================
# STATIC FILE SERVING (Flutter Web)
# =====================================================================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Serve Flutter web build"""
    from flask import send_from_directory, make_response, safe_join
    
    file_path = safe_join(app.static_folder, path)
    
    if path and os.path.isfile(file_path):
        response = make_response(send_from_directory(app.static_folder, path))
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    else:
        response = make_response(send_from_directory(app.static_folder, 'index.html'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    
    # Security Headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

# =====================================================================
# IMPORT BLUEPRINTS
# =====================================================================

try:
    from routes import auth_bp, ai_bp, environmental_bp, products_bp, orders_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')
    app.register_blueprint(environmental_bp, url_prefix='/api/v1/environmental')
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')
    app.register_blueprint(orders_bp, url_prefix='/api/v1/orders')
    
    logger.info("✅ All API routes registered")
    
except ImportError as e:
    logger.warning(f"Could not load some blueprints: {str(e)}")

# =====================================================================
# STARTUP EVENT
# =====================================================================

@app.before_first_request
def startup():
    """Run on first request"""
    logger.info(f"🚀 SBRBIOFORGE started in {Config.ENV} mode")
    logger.info(f"Available AI engines: {getattr(request, 'available_engines', 'Not initialized')}")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Starting server on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=Config.DEBUG,
        use_reloader=Config.DEBUG
    )

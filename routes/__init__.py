# ============================================================================
# SBRBIOFORGE API Routes
# ============================================================================

# Authentication Routes
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
ai_bp = Blueprint('ai', __name__)
environmental_bp = Blueprint('environmental', __name__)
products_bp = Blueprint('products', __name__)
orders_bp = Blueprint('orders', __name__)

# Routes will be implemented in individual route files
__all__ = ['auth_bp', 'ai_bp', 'environmental_bp', 'products_bp', 'orders_bp']

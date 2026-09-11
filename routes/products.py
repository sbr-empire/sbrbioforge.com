# ============================================================================
# Product Routes (E-Commerce)
# ============================================================================

from flask import Blueprint
from sbrcore.api.decorators import log_request
from sbrcore.api.utils import format_success_response
from sbrcore.logging import get_logger

products_bp = Blueprint('products', __name__)
logger = get_logger(__name__)

@products_bp.route('/', methods=['GET'])
@log_request
def list_products():
    """
    List all products
    """
    return format_success_response(
        {'products': []},
        'Products retrieved'
    )

# ============================================================================
# Order Routes (E-Commerce)
# ============================================================================

from flask import Blueprint
from sbrcore.api.decorators import log_request
from sbrcore.api.utils import format_success_response
from sbrcore.logging import get_logger

orders_bp = Blueprint('orders', __name__)
logger = get_logger(__name__)

@orders_bp.route('/', methods=['GET'])
@log_request
def list_orders():
    """
    List user orders
    """
    return format_success_response(
        {'orders': []},
        'Orders retrieved'
    )

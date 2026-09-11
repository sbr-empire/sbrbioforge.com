# ============================================================================
# Environmental Data Routes
# Fetch and manage environmental metrics
# ============================================================================

from flask import Blueprint, request, jsonify
from sbrcore.api.decorators import require_auth, rate_limit, log_request
from sbrcore.api.utils import format_error_response, format_success_response
from sbrcore.logging import get_logger
from sbrcore.database import DatabaseConnection
from models import Location, EnvironmentalData, Alert

environmental_bp = Blueprint('environmental', __name__)
logger = get_logger(__name__)

@environmental_bp.route('/current', methods=['GET'])
@log_request
@rate_limit(max_requests=50, window_seconds=60)
def get_current_data():
    """
    Get current environmental data for location
    """
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        
        if not latitude or not longitude:
            return format_error_response(
                'Missing latitude or longitude',
                'MISSING_LOCATION',
                422
            )
        
        # In production: fetch from weather API
        mock_data = {
            'location': {
                'latitude': float(latitude),
                'longitude': float(longitude)
            },
            'air_quality': {
                'aqi': 65,
                'pm25': 12.5,
                'status': 'Good'
            },
            'weather': {
                'temperature': 28,
                'humidity': 65,
                'wind_speed': 10
            },
            'water': {
                'level': 'Normal',
                'quality_index': 75
            },
            'health_alerts': []
        }
        
        return format_success_response(
            mock_data,
            'Environmental data retrieved'
        )
    
    except Exception as e:
        logger.error(f"Environmental data error: {str(e)}")
        return format_error_response(
            'Failed to fetch environmental data',
            'DATA_ERROR',
            500
        )

@environmental_bp.route('/forecast', methods=['GET'])
@log_request
def get_forecast():
    """
    Get 30-day environmental forecast
    """
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        days = int(request.args.get('days', 30))
        
        mock_forecast = {
            'location': {'latitude': float(latitude), 'longitude': float(longitude)},
            'forecast_days': days,
            'data': []
        }
        
        return format_success_response(
            mock_forecast,
            'Forecast retrieved'
        )
    
    except Exception as e:
        logger.error(f"Forecast error: {str(e)}")
        return format_error_response('Forecast failed', 'FORECAST_ERROR', 500)

@environmental_bp.route('/alerts', methods=['GET'])
@log_request
@require_auth
def get_alerts(user):
    """
    Get alerts for current user
    """
    try:
        with DatabaseConnection.session_scope() as session:
            alerts = session.query(Alert).filter(
                Alert.user_id == user['user_id']
            ).order_by(Alert.created_at.desc()).limit(50).all()
            
            alerts_data = [
                {
                    'id': alert.id,
                    'type': alert.alert_type,
                    'severity': alert.severity,
                    'title': alert.title,
                    'description': alert.description,
                    'created_at': alert.created_at.isoformat()
                }
                for alert in alerts
            ]
            
            return format_success_response(
                {'alerts': alerts_data},
                'Alerts retrieved'
            )
    
    except Exception as e:
        logger.error(f"Alerts error: {str(e)}")
        return format_error_response('Failed to fetch alerts', 'ALERTS_ERROR', 500)

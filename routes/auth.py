# ============================================================================
# Authentication Routes
# User registration, login, OAuth integration
# ============================================================================

from flask import Blueprint, request, jsonify
from sbrcore.auth import JWTHandler, OAuthManager
from sbrcore.database import DatabaseConnection, User
from sbrcore.api.decorators import require_auth, log_request
from sbrcore.api.utils import hash_password, verify_password, validate_email, format_error_response, format_success_response
from sbrcore.logging import get_logger

auth_bp = Blueprint('auth', __name__)
logger = get_logger(__name__)

@auth_bp.route('/register', methods=['POST'])
@log_request
def register():
    """
    Register new user
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('email') or not data.get('password') or not data.get('username'):
            return format_error_response('Missing required fields', 'VALIDATION_ERROR', 422)
        
        if not validate_email(data['email']):
            return format_error_response('Invalid email format', 'INVALID_EMAIL', 422)
        
        with DatabaseConnection.session_scope() as session:
            # Check if user exists
            existing = session.query(User).filter(
                (User.email == data['email']) | (User.username == data['username'])
            ).first()
            
            if existing:
                return format_error_response('User already exists', 'USER_EXISTS', 409)
            
            # Create user
            user = User(
                email=data['email'],
                username=data['username'],
                password_hash=hash_password(data['password']),
                full_name=data.get('full_name', ''),
                phone=data.get('phone', ''),
                roles='user'
            )
            
            session.add(user)
            session.flush()
            
            logger.info(f"User registered: {user.email}")
            
            return format_success_response(
                {
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username
                },
                'User registered successfully',
                201
            )
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return format_error_response('Registration failed', 'REGISTER_ERROR', 500)

@auth_bp.route('/login', methods=['POST'])
@log_request
def login():
    """
    User login with email/username and password
    """
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return format_error_response('Missing email or password', 'MISSING_CREDENTIALS', 422)
        
        with DatabaseConnection.session_scope() as session:
            # Find user
            user = session.query(User).filter(
                (User.email == data['email']) | (User.username == data['email'])
            ).first()
            
            if not user or not verify_password(data['password'], user.password_hash):
                return format_error_response('Invalid credentials', 'INVALID_CREDENTIALS', 401)
            
            if not user.is_active:
                return format_error_response('Account is inactive', 'ACCOUNT_INACTIVE', 403)
            
            # Generate token
            jwt_handler = JWTHandler()
            token = jwt_handler.generate_token(
                user_id=user.id,
                email=user.email,
                roles=user.roles.split(',')
            )
            
            # Update last login
            from datetime import datetime
            user.last_login = datetime.utcnow()
            
            logger.info(f"User logged in: {user.email}")
            
            return format_success_response(
                {
                    'token': token,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'full_name': user.full_name
                    }
                },
                'Login successful'
            )
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return format_error_response('Login failed', 'LOGIN_ERROR', 500)

@auth_bp.route('/google/callback', methods=['POST'])
@log_request
def google_callback():
    """
    Google OAuth callback handler
    """
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return format_error_response('Missing authorization code', 'MISSING_CODE', 422)
        
        oauth = OAuthManager('google')
        
        # This would be async in production
        # auth_result = await oauth.authenticate(code)
        
        return format_success_response(
            {'message': 'OAuth implementation pending'},
            'Partial implementation',
            200
        )
    
    except Exception as e:
        logger.error(f"OAuth error: {str(e)}")
        return format_error_response('OAuth failed', 'OAUTH_ERROR', 500)

@auth_bp.route('/verify-token', methods=['POST'])
@log_request
@require_auth
def verify_token(user):
    """
    Verify JWT token validity
    """
    return format_success_response(
        {'user': user},
        'Token is valid'
    )

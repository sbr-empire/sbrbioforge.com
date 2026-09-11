# ============================================================================
# SBRBIOFORGE Config Module
# Application-specific configuration
# ============================================================================

from sbrcore.config import Config as CoreConfig

class AppConfig(CoreConfig):
    """
    SBRBIOFORGE specific configuration
    Extends SBRCORE base configuration
    """
    
    # Application Info
    APP_NAME = 'SBRBIOFORGE'
    APP_DESCRIPTION = 'Environmental Intelligence Platform for 300-Year Civilization'
    
    # Environmental Data Sources
    ENVIRONMENTAL_UPDATE_INTERVAL = 300  # 5 minutes
    WEATHER_API = 'openweathermap'  # or 'nasa'
    AQI_API = 'airnow'  # Air Quality Index provider
    
    # Offline Cache
    OFFLINE_CACHE_ENABLED = True
    OFFLINE_CACHE_DAYS = 30
    
    # AI Configuration
    AI_DEFAULT_MODEL = 'groq'  # Fast responses for environmental alerts
    AI_TRANSLATION_ENGINE = 'groq'  # Multi-language support
    
    # Features
    ENABLE_OFFLINE_MODE = True
    ENABLE_PUSH_NOTIFICATIONS = True
    ENABLE_VOICE_ALERTS = True
    ENABLE_VIDEO_TUTORIALS = True
    
    # Location Services
    GPS_ACCURACY_HIGH = True
    GPS_UPDATE_INTERVAL = 60  # seconds
    
    # Data Privacy
    DATA_ENCRYPTION_ENABLED = True
    GDPR_COMPLIANT = True
    
    # Payment (for future e-commerce features)
    STRIPE_API_KEY = CoreConfig.get('STRIPE_API_KEY')
    RAZORPAY_API_KEY = CoreConfig.get('RAZORPAY_API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration on startup"""
        required_keys = [
            'OPENWEATHER_API_KEY',
            'GEMINI_API_KEY',
            'GROQ_API_KEY',
            'JWT_SECRET_KEY'
        ]
        
        missing = [key for key in required_keys if not cls.get(key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

# Configuration instance
config = AppConfig()

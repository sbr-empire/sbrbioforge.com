# ============================================================================
# SBRBIOFORGE Database Models Extension
# Models specific to environmental data
# ============================================================================

from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sbrcore.database.models import BaseModel, User

class Location(BaseModel):
    """
    User location tracking for environmental data
    """
    __tablename__ = 'locations'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    
    # Coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    
    # Location Info
    city = Column(String, nullable=False, index=True)
    state = Column(String)
    country = Column(String, nullable=False)
    timezone = Column(String)
    
    # Tracking
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship('User', backref='locations')

class EnvironmentalData(BaseModel):
    """
    Cached environmental metrics
    """
    __tablename__ = 'environmental_data'
    
    id = Column(String, primary_key=True)
    location_id = Column(String, ForeignKey('locations.id'), nullable=False, index=True)
    
    # Air Quality
    aqi = Column(Float)  # Air Quality Index
    pm25 = Column(Float)  # Particulate Matter 2.5
    pm10 = Column(Float)  # Particulate Matter 10
    no2 = Column(Float)  # Nitrogen Dioxide
    o3 = Column(Float)   # Ozone
    so2 = Column(Float)  # Sulfur Dioxide
    co = Column(Float)   # Carbon Monoxide
    
    # Weather
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    precipitation = Column(Float)
    cloudiness = Column(Float)
    
    # Water
    water_level = Column(Float)  # Groundwater level
    water_quality_index = Column(Float)
    water_temperature = Column(Float)
    
    # Health
    uv_index = Column(Float)
    allergen_level = Column(String)  # Low, Medium, High
    
    # Metadata
    data_source = Column(String)  # nasa, openweather, airnow
    confidence = Column(Float)  # 0-1 confidence score
    collected_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Alert(BaseModel):
    """
    Environmental alerts for users
    """
    __tablename__ = 'alerts'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    location_id = Column(String, ForeignKey('locations.id'), nullable=False)
    
    # Alert Details
    alert_type = Column(String, nullable=False)  # air_quality, water, weather, health
    severity = Column(String)  # low, medium, high, critical
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # AI-Generated Content
    ai_recommendation = Column(Text)  # AI generated advice
    ai_engine_used = Column(String)  # Which AI engine generated this
    
    # Status
    is_read = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Multimedia
    has_audio = Column(Boolean, default=False)  # ElevenLabs TTS
    has_video = Column(Boolean, default=False)  # Luma AI video
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', backref='alerts')

class OfflineData(BaseModel):
    """
    30-day offline cache for emergency situations
    """
    __tablename__ = 'offline_data'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    location = Column(String, nullable=False)
    
    # Cached Data (JSON)
    environmental_data = Column(JSON)
    health_guidelines = Column(JSON)
    survival_tips = Column(JSON)
    emergency_contacts = Column(JSON)
    
    # Metadata
    data_version = Column(Integer, default=1)
    last_synced = Column(DateTime)
    expires_at = Column(DateTime)  # 30 days from sync
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

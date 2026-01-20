"""
Configuration classes for different environments
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Google Sheets
    GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0')
    GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH', './config/secrets/google_sheets_credentials.json')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Development-specific settings
    PC_MLRA_DEMO_MODE = os.environ.get('PC_MLRA_DEMO_MODE', 'false').lower() == 'true'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use test database/Google Sheet
    GOOGLE_SHEET_ID = os.environ.get('TEST_GOOGLE_SHEET_ID', 'test_sheet_id')
    
    # Mock external services
    MOCK_EXTERNAL_SERVICES = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Production security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Production logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"

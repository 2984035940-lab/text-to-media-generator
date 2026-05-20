import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # API Keys
    RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY', '')
    LEONARDO_API_KEY = os.getenv('LEONARDO_API_KEY', '')
    
    # Paths
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../output')
    TEMP_FOLDER = os.path.join(os.path.dirname(__file__), '../temp')
    
    # Runway API
    RUNWAY_API_URL = 'https://api.runwayml.com/v1'
    
    # Leonardo API
    LEONARDO_API_URL = 'https://api.leonardo.ai/rest/v1'
    
    # Settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_VIDEO_FORMATS = ['mp4', 'mov', 'avi']
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'webp']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    RUNWAY_API_KEY = 'test-key'
    LEONARDO_API_KEY = 'test-key'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

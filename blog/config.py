"""Application configuration options"""

import os

# Configuration variables that control app
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful"  # Environment variable for database location
    DEBUG = True  # Use Flask debug mode to track errors
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
    # 'SECRET_KEY' used to cryptographically secure app
    # Rather than keep key inside application, store as environment variable
    # Set enviroment variable in terminal: export BLOGFUL_SECRET_KEY="secret key"
    # Could run as bash script before app run

# Config for testing environment    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful-test"  # Different database
    DEBUG = False      # Turn off debugging
    SECRET_KEY = "Not secret"    # Different secret key not tied to environment variable
"""Application setup and configuration"""

import os
from flask import Flask

# Create app
app = Flask(__name__)

# Load configuration file
# Either from CONFIG_PATH environment variable or default development configuration
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
# Configure app
# Could use different configurations for different environments: development, testing, production
app.config.from_object(config_path)


# Import views and filters after creating app
# Views and filters use 'app' object
import views
import filters

# Import login and access to user ID
import login
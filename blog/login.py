"""Login system"""

from flask.ext.login import LoginManager

from blog import app
from database import session
from models import User

# Use Flask-Login LoginManager object and initialize
login_manager = LoginManager()
login_manager.init_app(app)

# View which unauthorized user is redirected to
login_manager.login_view = "login_get"
# Error message classification used in conjunction with Bootstrap
login_manager.login_message_category = "danger"

# Function that accesses object that represents user ID
@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))
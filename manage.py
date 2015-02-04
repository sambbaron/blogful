"""Application management file (uses Flask-Script)"""

import os
# Use Flask-Script to automate tasks to manage application
from flask.ext.script import Manager

# Use 'app' object from __init__
from blog import app

# Import database connection 'session' and database table 'Post'
from blog.models import Post
from blog.database import session

# Libraries/objects to manage users
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

# Create instance of 'manager' object
manager = Manager(app)

# Use decorator to add command to manager
@manager.command
# Name of function is script name called from "manager"
# python manager.py run
def run():
    """Run development server"""
    # Retrieve port from environment, if none available, use 8080
    # Allows flexibility for servers that don't use fixed outgoing ports
    port = int(os.environ.get('PORT', 8080))
    # Start application development server
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    """Add dummy posts to database"""
    
    # Dummy post content
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    # Create 25 dummy posts
    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()
    
@manager.command
def adduser():
    """Create new user"""
    
    # User input name and email address
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    # Test whether user already exists
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return
    
    # User input password (entered twice for verification)
    password = ""
    password_2 = ""
    # Loop while either password is empty or passwords do not match
    while not (password and password_2) or password != password_2:
        # Use builtin getpass function to input password without echoing string
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    # Create new user instance
    # Password is converted to hash - string of characters based on SHA1 hashing algorithm
    # Hashes only work one-way (password to hash string) to prevent malicious use of stored passwords
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()    

if __name__ == "__main__":
    manager.run()
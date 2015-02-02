"""Application management file (uses Flask-Script)"""

import os
# Use Flask-Script to automate tasks to manage application
from flask.ext.script import Manager

# Use 'app' object from __init__
from blog import app

# Import database connection 'session' and database table 'Post'
from blog.models import Post
from blog.database import session

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

if __name__ == "__main__":
    manager.run()
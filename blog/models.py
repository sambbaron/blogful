"""Database models - SQLAlchemy"""

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base, engine

# Flask-Login to manage user login/logout and session tracking
from flask.ext.login import UserMixin

# Create a table - Posts
class Post(Base):
    # Table name
    __tablename__ = "posts"

    # Column definitions
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    
# User table for Flask-Login
# Inherits from UserMixin, which adds default methods
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))    

# Create database tables 
Base.metadata.create_all(engine)
"""Database models - SQLAlchemy"""

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base, engine

# Create a table - Posts
class Post(Base):
    # Table name
    __tablename__ = "posts"

    # Column definitions
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

# Create database tables 
Base.metadata.create_all(engine)
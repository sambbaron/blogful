"""Database setup"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from blog import app

import multiprocessing

# Engine to communicate with database using URI name from config.py
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
# Base - db model repository
Base = declarative_base()
# Session - object used to execute database transactions
Session = sessionmaker(bind=engine)
session = Session()
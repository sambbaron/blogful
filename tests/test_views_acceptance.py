"""Acceptance Testing"""

import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
        
    def setUp(self):
        """ Test setup """
        
        # Unlike integration test, create browser instance rather than app instance
        # PhantomJS used for browser automation
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
        # Use 'multiprocessing' module to run test server since test is going to actual website
        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)
        
        # Set url path
        self.url_path = "http://127.0.0.1:5000"
        
    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        Base.metadata.drop_all(bind=engine, checkfirst=False)
        self.browser.quit()    
        
    def simulate_login(self):
        """Login using example user"""
        
        self.browser.visit(self.url_path + "/login")  # Go to /login page
        self.browser.fill("email", "alice@example.com")  # Fill in "email" form
        self.browser.fill("password", "test")        # Fill in "password" form
        button = self.browser.find_by_css("button[type=submit]")  # Press "submit" button
        button.click()
        
    def testLoginCorrect(self):
        """Test successful login using example user"""        
        
        self.simulate_login()
        self.assertEqual(self.browser.url, self.url_path + "/") # Test whether redirected to root path

    def testLoginIncorrect(self):
        """Test unsuccessful login"""
        
        self.browser.visit(self.url_path + "/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, self.url_path + "/login")    
        
    def testAddPost(self):
        """Test add post"""
        
        # Login
        self.simulate_login()
        
        # Click on "Add Post" button
        self.browser.find_by_css("button[name='add-post']").click()
        # Test whether on "Add Post" page
        self.assertEqual(self.browser.url, self.url_path + "/post/add")
        # Fill add post form
        self.browser.fill("title", "New Post Title")
        self.browser.fill("content", "New post content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        # Test whether redirected to root path
        self.assertEqual(self.browser.url, self.url_path + "/")    

if __name__ == "__main__":
    unittest.main()
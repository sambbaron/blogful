"""Integration test of add_post_post view"""

import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database from config.py
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        
        # Create a test client that allows inspection of app views/responses
        self.client = app.test_client()

        # Set up the tables in the testing database
        Base.metadata.create_all(engine)

        # Create an example user in the testing database
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the testing database
        Base.metadata.drop_all(engine)
        
    def simulate_login(self):
        """Simulate user login in testing session"""
        # Open testing session transaction using 'session_transaction'
        # Represents HTTP session
        with self.client.session_transaction() as http_session:
            # Add variables to session
            http_session["user_id"] = str(self.user.id)  # User ID from example user created in setUp method
            http_session["_fresh"] = True  # Defines session as active

    def post_get(self):
        # Use 'self.client.get' method to send HTTP GET request to "/post/add"
        pass
    
    def add_post(self):        
        # Use 'self.client.post' method to send HTTP POST request to "/post/add"
        # 'data' parameter simulates form submission
        return self.client.post("/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        })


    def testAddPost(self):
        """Test adding post"""
        
        # Login using login simulation method from above
        self.simulate_login()
        
        # Add post
        response = self.add_post()
        
        # Test app response
        self.assertEqual(response.status_code, 302)  # 302 Found - redirect after POST
        self.assertEqual(urlparse(response.location).path, "/")  # Redirect path is root URI
        # Test post in database with count
        posts = session.query(models.Post).all() 
        self.assertEqual(len(posts), 1)
        # Test post data
        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "<p>Test content</p>\n")
        self.assertEqual(post.author, self.user)        

    def testEditPost(self):
        """Test editing post"""
        
        # Login using login simulation method from above
        self.simulate_login()
        
        # Add post
        self.add_post()
        
        # Edit Post
        response = self.client.post("/post/1/edit", data={
            "title": "Edit Post",
            "content": "Edit content"
        })
        
        # Test app response
        self.assertEqual(response.status_code, 302)  # 302 Found - redirect after POST
        self.assertEqual(urlparse(response.location).path, "/")  # Redirect path is root URI
        # Test post data
        posts = session.query(models.Post).all() 
        post = posts[0]
        self.assertEqual(post.title, "Edit Post")
        self.assertEqual(post.content, "<p>Edit content</p>\n")
        self.assertEqual(post.author, self.user)                

    def testDeletePost(self):
        """Test deleting post"""
        
        # Login using login simulation method from above
        self.simulate_login()
        
        # Add post
        self.add_post()
        
        # Delete Post
        response = self.client.post("/post/1/delete")
        
        # Test app response
        self.assertEqual(response.status_code, 302)  # 302 Found - redirect after POST
        self.assertEqual(urlparse(response.location).path, "/")  # Redirect path is root URI
        # Test post data
        posts = session.query(models.Post).all() 
        self.assertEqual(len(posts), 0)
        
if __name__ == "__main__":
    unittest.main()
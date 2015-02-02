"""Views - Route to Jinja Templates"""

# Import 'render_template' function to return Jinja templates
from flask import render_template

from blog import app
from database import session
from models import Post

# Route to top url
@app.route("/")
def posts():
    # Return query for posts table
    posts = session.query(Post)
    # Order posts by datetime descending
    posts = posts.order_by(Post.datetime.desc())
    # Return all rows in posts table
    posts = posts.all()
    # Pass posts to posts.html template
    return render_template("posts.html",
        posts=posts
    )
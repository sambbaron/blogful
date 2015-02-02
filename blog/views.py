"""Views - Route to Jinja Templates"""

# Import 'render_template' function to return Jinja templates
from flask import render_template

from blog import app
from database import session
from models import Post

# Mistune - markdown parser for submitting formatted blog posts
import mistune
# Flask objects for form post
from flask import request, redirect, url_for

# Route to top url
@app.route("/")
# Route using <page> placeholder
@app.route("/page/<int:page>")
# page - page number; paginate_by - how many posts on a page
def posts(page=1, paginate_by=10):
    # Convert 'page' to zero-indexed 'page_index'
    page_index = page - 1
    
    # Number of posts
    count = session.query(Post).count()
    
    # Start and ending posts calculated based on 'paginate_by' argument
    start = page_index * paginate_by
    end = start + paginate_by
    
    # Calculate total pages and whether current page is at beginning or end
    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    # Return query for posts table
    posts = session.query(Post)
    # Order posts by datetime descending
    posts = posts.order_by(Post.datetime.desc())
    # Return posts for start/end indices
    posts = posts[start:end]
    # Pass posts to posts.html template
    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages                           
    )

# GET request for adding post
@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")

# POST request for adding post
@app.route("/post/add", methods=["POST"])
def add_post_post():
    # New post - use request.form Flask dictionary to access HTML form
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    # Use Flask redirect function to send user back to home page
    return redirect(url_for("posts"))
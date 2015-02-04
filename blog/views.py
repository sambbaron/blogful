"""Views - Route to Jinja Templates"""

# Import 'render_template' function to return Jinja templates
from flask import render_template

from blog import app
from database import session
from models import Post

# Mistune - markdown parser for submitting formatted blog posts
import mistune
# Html2Text - convert html to markdown
import html2text
# Flask objects for form post
from flask import request, redirect, url_for

# Flask objects for login
from flask import flash
from flask.ext.login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from models import User

# Route to top url
@app.route("/")
# Route using <page> placeholder
@app.route("/page/<int:page>")
# page - page number; paginate_by - how many posts on a page
def posts(page=1, paginate_by=10):
    # Convert 'page' to zero-indexed 'page_index'
    page_index = page - 1
    
    # Number of posts
    count = session.query(Post).filter(Post.author==current_user).count()
    
    # Start and ending posts calculated based on 'paginate_by' argument
    start = page_index * paginate_by
    end = start + paginate_by
    
    # Calculate total pages and whether current page is at beginning or end
    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    # Return query for posts table
    posts = session.query(Post)
    # Filter posts by current user
    posts = posts.filter(Post.author==current_user)
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

# GET request for adding new post
@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

# POST request for adding post
@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    # New post - use request.form Flask dictionary to access HTML form
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        # Set author using Flask-Login current_user object
        author=current_user
    )
    session.add(post)
    session.commit()
    # Use Flask redirect function to send user back to home page
    return redirect(url_for("posts"))

# View single post
@app.route("/post/<int:id>")
def single_post(id=1):
    posts = session.query(Post)
    posts = posts.filter(Post.id == id).all()
    return render_template("posts.html",
        posts=posts)

# GET request for editing existing post
@app.route("/post/<int:id>/edit", methods=["GET"])
@login_required
def edit_post_get(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    if post.author == current_user:
        return render_template("edit_post.html", post_title=post.title, post_content=html2text.html2text(post.content))
    else:
        return redirect(url_for("posts"))

# POST request for editing existing post
@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
def edit_post_post(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))

# GET request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["GET"])
@login_required
def delete_post_get(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    return render_template("delete_post.html", post_title=post.title)

# POST request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["POST"])
@login_required
def delete_post_delete(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))

# GET request for login
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

# POST request for login
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    # Test whether user already exists
    user = session.query(User).filter_by(email=email).first()
    # If user does not exist or password does not match hashed password, then redirect with error message
    if not user or not check_password_hash(user.password, password):
        # Flask 'flash' function stores message to display in page
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    
    # If username and password are correct, 
    # Use Flask-Login login_user function to use cookie to identify user in browser
    login_user(user)
    # Either access resource selected at login or go to main /posts page
    return redirect(request.args.get('next') or url_for("posts"))

# Logout
@app.route("/logout")
def logout():
    logout_user()
    return render_template("login.html")
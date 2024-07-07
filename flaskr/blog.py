# blog will list posts, allow logged in users to create posts, and allow the author to edit/delete their posts
# PART 7A: CREATE A BLUEPRINT FOR BLOG FUNCTIONALITIES

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# PART 7B: CREATE THE INDEX (where all the blog posts will be shown)
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        'FROM post p JOIN userr u ON p.author_id = u.id' # JOIN is used so the user/author info from the user table is available
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# PART 8: CREATE THE CREATE VIEW (similar to the register view, but to create new posts instead of accounts)
@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?,?,?)', title(title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
        return render_template('blog/create.html')
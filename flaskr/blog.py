# blog will list posts, allow logged in users to create posts, and allow the author to edit/delete their posts
# PART 7A: CREATE A BLUEPRINT FOR BLOG FUNCTIONALITIES
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import feedparser

bp = Blueprint('blog', __name__)

# PART 7B: CREATE THE INDEX (where all the blog posts will be shown)
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id' # JOIN is used so the user/author info from the user table is available
        ' ORDER BY created DESC' # NOTE: these spaces at the beginning of the queries matter
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

# PART 8B: GET POSTS (fetch a post by its id and check if the author is the logged in user. This function will be called from both update/delete views)
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,),
    ).fetchone()    

    if post is None:
        abort(404, f"Post id {id} does not exist.") # abort() raises a special exception that returns an HTTP status code and taks an optional error message
    if check_author and post['author_id'] != g.user['id']:
        abort(403) # 404 = Not Found and 403 means Forbidden
    return post

# PART 8A: CREATE THE CREATE VIEW (similar to the register view, but to create new posts instead of accounts)
@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    feed = None
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        # feed_url = 'https://feed.desiringgod.org/link/23670/16736952/keep-rejoicing' # change to request.form and take the url as form input?
        # feed = feedparser.parse('https://feed.desiringgod.org/link/23670/16736952/keep-rejoicing')
        # feed = request.form['feed']
        video_url = request.form['video_url']
        error = None

        if not title:
            error = 'A title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, video_url, author_id) VALUES (?, ?, ?, ?)',
                (title, body, video_url, g.user['id']),
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')

# PART 8C: UPDATE VIEW
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id): # this view takes id as an argument
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        video_url = request.form['video_url']
        error = None
    
        if not title:
            error = 'A title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, video_url = ?'
                ' WHERE id = ?',
                (title, body, video_url, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# 8D: DELETE POST
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
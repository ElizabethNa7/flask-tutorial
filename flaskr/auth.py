# terms: endpoint(s), blueprint(s)

# PART 3: CREATE A BLUEPRINT
import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# # url_for() generates the URL to a view based on a name + arguments. The name is called an endpoint, which is the unique identifier for view functions
# example: url_for('hello', who='World')
# # blueprint is a way to organize Flask apps into modular components. The name you give a bp is used to prefix the endpoints of all the bp's view functions

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') # a blueprint called auth is created, and the url_prefix (/auth) will be prepended to all URLs associated with this blueprint


# PART 4: Create the first view (page) for REGISTRATION
# --> when the user visits the /auth/register URL, this register view will return HTML with a form for them to fill out
# --> once submitted, it will validate their input and either show the form + error message or create the new user and go to the login page
@bp.route('/register', methods=('GET', 'POST')) # bp.route associates the URL /register with the register view function
def register():
    if request.method == 'POST': # if the user had submitted the form, the POST method is used and the input starts getting validated
        username = request.form['username'] # request.form is dict mapping of submitted form keys and values
        password = request.form['password'] # Note: 'single quotes' are used for HTML template paths and certain string literals.
        db = get_db()
        error = None

        if not username:
            error = 'Please enter a username.'
        elif not password:
            error = 'Please enter a password.'

        if error is None:
            try:
                db.execute( # Note: "double quotes" are used for SQL queries
                    "INSERT INTO user (username, password) VALUES (?,?)", # ? is an SQL placeholder for user input
                    (username, generate_password_hash(password)), # a tuple () replaces the placeholders
                )
                db.commit() # this is used to save the changes (since password was hashed for security)
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login")) # once user info is stored, the user is redirected to the login page
        flash(error) # if there was an error, show the user the error (flash() stores messages retrieved when rendering the template)
    return render_template('auth/register.html') # renders the template containing this HTML

# PART 5: Create the LOGIN view (page), similar to register
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute( # query (check/look) for the entered user
            'SELECT * FROM user WHERE username = ?', (username)
        ).fetchone() # fetchone() returns one row from teh query

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear() # session is a dict that stores data across requests
            session['user_id'] = user['id'] # If/when validation succeeds, the user's id is stored in a new session. Now that it's stored in the session, it'll be available in subsequent requests
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

# PART 6A: check if user exists
@bp.before_app_request # registers a function that runs before the view function, regardless of the URL requested
def load_logged_in_user(): # check if a user id is stored in the session, get that user's data from the db, and store it in g.user (which lasts for the lenght of the request)
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# PART 6B: log out
bp.route('/logout')
def logout():
    session.clear() # remove the user id from the session so load_logged_in_user won't have/use a user_id to load in subsequent requests
    return redirect(url_for('index'))

# PART 6C: login required of user
# use a decorator to check if the user is logged in for otherr features (creating, editing, deleting posts)
def login_required(view):
    @functools.wraps(view) 
    def wrapped_view(**kwargs): # returns a new view function that wraps the original view it's applied to
        if g.user is None: # if user is not loaded
            return redirect(url_for('auth.login'))
        return view(**kwargs) # kwargs is flexible and used so any view function can be wrapped regardless of its parameters
    return wrapped_view
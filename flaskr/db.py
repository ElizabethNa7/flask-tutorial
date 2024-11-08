# PART 2: CREATE DB
import sqlite3

import click
from flask import current_app, g
# g is a special object unique for every request. It's used to store data that might be accessed by multiple functions during the request.
# The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request

def get_db():
    if 'db' not in g:
        g.db=sqlite3.connect( # used to establish a connection to the file pointed to by 'DATABASE' config key
            current_app.config['DATABASE'], # current_app points to the Flask app handling the request
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row # tells the connection to return rows that behave like dicts - allows columns to be accessed by name
    return g.db

def close_db(e=None):
    db=g.pop('db', None)
    if db is not None: # if a connection was created, close it
        db.close()

# REGISTER with the app
# python function to run the SQL commands in schema.sql
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
@click.command('init-db') # click.command() defines a command line command (init-db) which calls the init_db function to show a success message to the user
def init_db_command():
    """Clear existing data and create new tables"""
    init_db()
    click.echo('Database initialized.')

def init_app(app): # registerrs the close_db and init_db_command functions with the application instance so they can be used by the app
    app.teardown_appcontext(close_db) # tells Flask to call the close_db function after the returning the response, when cleaning up
    app.cli.add_command(init_db_command) # adds the a new command (init_db_command) so it can be used with the flask command
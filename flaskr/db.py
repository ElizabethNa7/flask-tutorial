import sqlite3

import click
from flask import current_app, g
# g is a special object unique for every request. It's used to store data that might be accessed by multiple functions during the request.
# The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request

def get_db():
    if 'db' not in g:
        g.db=sqlite3.connect( # used to establish a connection to the file pointed to by 'DATABASE' config key
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row # tells the connection to return rows that behave like dicts - allows columns to be accessed by name
    return g.db

def close_db(e=None):
    db=g.pop('db', None)
    if db is not None:
        db.close()

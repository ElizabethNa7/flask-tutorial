import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app): # test that get_db returns the same connection whenever it's called
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed in str(e.value)'

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db) # use Pytest's monkeypatch fixture to replace the init_db function with one that records it's been called
    result = runner.invoke(args=['init-db']) # runner fixture (written above) is used to call the init-db command
    assert 'initialized' in result.output
    assert Recorder.called
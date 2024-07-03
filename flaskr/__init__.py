import os
from flask import Flask # every Flask app is an instance of the Flask class

def create_app(test_config=None): 
    app=Flask(__name__, instance_relative_config=True) # create your app by creating a Flask instance
    app.config.from_mapping(
        SECRET_KEY='dev', # SECRET_KEY is to keep data safe. Its default is dev while developing but later should be overridden with a random/hashed value
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # I think you could use other db tools like SQLAlchemy here, but basically DATABASE is the path where your db file will be saved
    )

    if test_config is None:
        # if not testing, load the instance config
        app.config.from_pyfile('config.py', silent=True) # override default configs with values from config.py if it esists (for example, changing the SECRET_KEY)
    else:
        # if the test config is passed in, load it
        app.config.from_mapping(test_config) # to use test configs while testing instead of your standard configs
    
    # make sure the instance folder (for your db?) exists
    try:
        os.makedirs(app.instance_path) # note this does not create it if it doesn't exist, just checks if it does
    except OSError:
        pass # if already exists just pass

    @app.route('/hello') # to create routes (basically used to create a connection between the URL and function (URL /hello and the hello() function in this case)
    def hello():
        return 'Hello, World!'
    
    return app
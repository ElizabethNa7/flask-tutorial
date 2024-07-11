# flask-tutorial (https://flask.palletsprojects.com/en/3.0.x/tutorial/database/)

- activate your virtual environment (within flask-tutorial): . .venv/bin/activate
- start/run the app: flask --app flaskr run --debug
- initialize the db: flask --app flaskr init-db


## Study/Review
- PART 1: CREATE APP (__init__.py)
- PART 2: CREATE DB (db.py)
- PART 3: CREATE authorization BLUEPRINT (auth.py)
- PART 4: CREATE first VIEW (page) for REGISTRATION (auth.py)
- PART 5: Create view (page) for LOGIN (auth.py)
- PART 6: Create CSS stylesheet.css
- PART 7A: CREATE blog BLUEPRINT (blog.py)
- PART 7B: CREATE THE INDEX (wherre all the blog posts will be shown)
- PART 7C: CREATE AN INDEX.HTML 
- PART 8A: CREATE VIEW (similar to the register view, but to create new posts instead of accounts)
- PART 8B: GET VIEW (get post. this function is used for UPDATE and DELETE functions)
- PART 8C: UPDATE VIEW
- PART 8D: DELETE VIEW

Testing with Pytest (terms: fixtures, factory, context)
- note: when running I had to first do 2 things first to fix the directories and let conftest.py find the flaskr module...
- . .venv/bin/activate
- export PYTHONPATH=.
- then run pytest (or pytest -v to get a list of each test function, or coverage report for a simple report)
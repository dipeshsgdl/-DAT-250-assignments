from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import flask_login, sqlite3, os, secrets


# create and configure app
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
Bootstrap(app)
app.config.from_object(Config)

# flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# limiter -> Limited amount of requests from client
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)

# get an instance of the db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

# initialize db for the first time
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# perform generic query, not very secure yet
def query_db(query,arg,one=False):
    db = get_db()
    cursor = db.execute(query, arg)
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    if one:
        return rv[0] if rv else None
    return rv

def user_info(username, one=False):
    db = get_db()
    cursor = db.execute("SELECT * FROM Users WHERE username=?", [username])
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    if one:
        return rv[0] if rv else None
    return rv

def query_friends(users,one=False):
    if len(users) != 2: return 0
    db = get_db()
    cursor = db.execute("SELECT * FROM Friends WHERE u_id=? AND f_id=?", [users[0],users[1]])
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    if one:
        return rv[0] if rv else None
    return rv

# TODO: Add more specific queries to simplify code

# automatically called when application is closed, and closes db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# initialize db if it does not exist
if not os.path.exists(app.config['DATABASE']):
    init_db()

if not os.path.exists(app.config['UPLOAD_PATH']):
    os.mkdir(app.config['UPLOAD_PATH'])

from app import routes
import os,secrets

# contains application-wide configuration, and is loaded in __init__.py

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_bytes(32) # secrets.token_urlsafe(20)
    DATABASE = 'database.db'
    UPLOAD_PATH = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','webp'}
from pydoc import plain
import bcrypt,base64,hashlib
from urllib.parse import unquote,quote
from app import query_db
from app.forms  import IndexForm

# Hash
def hash_password(plain_text_password):
    plain_text_password = base64.b64encode(hashlib.sha256(safe_convert(plain_text_password).encode('utf-8')).digest()) #safe_convert(plain_text_password).encode('utf-8')
    return bcrypt.hashpw(plain_text_password, salt = bcrypt.gensalt()).decode('utf-8')

def check_password(plain_text_password, hashed_password):
    plain_text_password = base64.b64encode(hashlib.sha256(safe_convert(plain_text_password).encode('utf-8')).digest())
    return bcrypt.checkpw(plain_text_password, hashed_password.encode('utf-8')) #base64.b64encode( hashlib.sha256( plain_text_password ).digest() )

# Escape special symbols.
def safe_convert(input):
    try:
      number = int(input)
      return number
    except:
      return quote(input)

def convert_back(input):
    return unquote(input)

def check_if_username_exist(username_entered):
    existing_user = query_db('SELECT * FROM Users WHERE username="{}" limit 1;'.format(username_entered), one=True)
    if existing_user is None: return False
    return False if existing_user['username'] is None else True

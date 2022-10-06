import bcrypt,base64,hashlib
from urllib.parse import unquote,quote
from app import app,query_friends, user_info

# Hash
def hash_password(plain_text_password):
    plain_text_password = base64.b64encode(hashlib.sha256(safe_convert(plain_text_password).encode('utf-8')).digest())
    return bcrypt.hashpw(plain_text_password, salt = bcrypt.gensalt()).decode('utf-8')

def check_password(plain_text_password, hashed_password):
    plain_text_password = base64.b64encode(hashlib.sha256(safe_convert(plain_text_password).encode('utf-8')).digest())
    return bcrypt.checkpw(plain_text_password, hashed_password.encode('utf-8'))

# Escape special symbols.
def safe_convert(input):
    if input is None: return input
    try:
      return int(input)
    except ValueError:
      return quote(input)

def convert_back(input):
    if input is None: return input
    return unquote(input)

def check_if_username_exist(username_entered):
    existing_user = user_info(safe_convert(username_entered),one=True)
    if existing_user is None: return False
    return False if existing_user['username'] is None else True

def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def are_friends(main, friend):
    try:
      main = int(main)
      friend = int(friend)
    except ValueError:
      return "Exception: one of the inputs that were given were not an int"
    friends = query_friends([main,friend],one=True)
    if friends is None: return False
    return friends

# Checks if both of them agreed to be friends.
def both_friends(userA, userB):
    try:
      userA = int(userA)
      userB = int(userB)
    except ValueError:
      return "Exception: one of the inputs that were given were not an int"
    friends_0 = query_friends([userA,userB],one=True)
    friends_1 = query_friends([userB,userA],one=True)
    if friends_0 is None or friends_1 is None: return False
    return True

def get_user_id(username):
    if username is None: return
    user = user_info(safe_convert(username),one=True)
    try:
      return int(user['id'])
    except ValueError:
      print('Expected number')
    return False
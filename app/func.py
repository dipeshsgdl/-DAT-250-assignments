import bcrypt
from urllib.parse import unquote,quote
from app import query_db
from app import IndexForm

#### HASH ####
def hash_password(plain_text_password):
    return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password.encode('utf-8')).digest()), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password.encode('utf-8')).digest()), hashed_password)

def check_if_username_exist(username_entered):
    existing_user = query_db('SELECT * FROM Users WHERE username="{}" limit 1;'.format(IndexForm().login.username.data), one=True)
    for i in existing_user:
        print(i)
    if username_entered == existing_user:
        return True
    else:
        return False
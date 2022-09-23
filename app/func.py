import bcrypt
from urllib.parse import unquote,quote

#### HASH ####
def hash_password(plain_text_password):
    return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password.encode('utf-8')).digest()), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password.encode('utf-8')).digest()), hashed_password)
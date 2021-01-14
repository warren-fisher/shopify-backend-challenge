from sqlalchemy import create_engine
from sqlalchemy.sql import select, text

from cred_mysql import credentials

engine = create_engine(
    f"mysql+pymysql://{credentials['username']}:{credentials['password']}@localhost/imagerepository",
     echo=True)

def get_files():
    return

def create_file_record():
    return

def get_albums():
    return

def create_album_record():
    return

def create_user(username, password):
    s = text("""INSERT INTO users (U_NAME, U_PSWD) VALUES (:x, :y)""")

    result = engine.connect().execute(s, x=username, y=password)
    return

def check_user_name(username):
    s = text("""SELECT * FROM users where U_NAME like :x""")

    result = engine.connect().execute(s, x=username)

    is_available = "true"

    for res in result:
        # If there is a result then this name is taken
        is_available = "false"
        break

    return {'available': is_available}
from sqlalchemy import create_engine
from sqlalchemy.sql import select, text

from cred_mysql import credentials

engine = create_engine(
    f"mysql+pymysql://{credentials['username']}:{credentials['password']}@localhost/imagerepository",
     echo=True)

def get_files():
    user_code = get_user_code(username)

    s = text("""SELECT P_NAME FROM photos WHERE P_PRIVATE = 0 OR U_CODE is :x""")
    result = engine.connect().execute(s, x=user_code, y=private, z=filename)

    return

def create_file_record(username, private, filename):
    user_code = get_user_code(username)

    s = text("""INSERT INTO photos (U_CODE, P_PRIVATE, P_NAME) VALUES (:x, :y, :z)""")
    result = engine.connect().execute(s, x=user_code, y=private, z=filename)

    return


def get_albums(username):
    user_code = get_user_code(username)

    s = text("""SELECT A_NAME, P_NAME FROM albums INNER JOIN photos ON albums.A_ID = photos.A_ID
             WHERE P_PRIVATE = 0 OR photos.U_CODE IS :x""")
    result = engine.connect().execute(s, x=user_code)

    return

def get_user_code(username):
    s = text("""SELECT U_CODE FROM users where U_NAME like :x""")
    result = engine.connect().execute(s, x=username)

    for row in results:
        return row[0]
    return None


def create_album_record(username, private, album_name):
    user_code = get_user_code(username)

    s = text("""INSERT INTO albums (U_CODE, A_PRIVATE, A_NAME) VALUES (:x, :y, :z)""")
    result = engine.connect().execute(s, x=user_code, y=private, z=album_name)
    return

def login_user(username, password):
    s = text("""SELECT * FROM users WHERE U_NAME LIKE :x AND U_PSWD LIKE :y""")
    result = engine.connect().execute(s, x=username, y=password)

    res = result.first()

    if res is None:
        return 'failure'
    return 'success'

def create_user(username, password):
    s = text("""INSERT INTO users (U_NAME, U_PSWD) VALUES (:x, :y)""")

    result = engine.connect().execute(s, x=username, y=password)
    return

def is_available_check(result):
    is_available = "true"

    for res in result:
        # If there is a result then this name is taken
        is_available = "false"
        break

    return {'available': is_available}

def check_user_name(username):
    s = text("""SELECT * FROM users where U_NAME like :x""")

    result = engine.connect().execute(s, x=username)
    return is_available_check(result)

def check_album_name(album_name):
    s = text("""SELECT * FROM albums where A_NAME like :x""")

    result = engine.connect().execute(s, x=album_name)
    return is_available_check(result)

def check_photo_name(photo_name):
    s = text("""SELECT * FROM photos where P_NAME like :x""")

    result = engine.connect().execute(s, x=photo_name)
    return is_available_check(result)
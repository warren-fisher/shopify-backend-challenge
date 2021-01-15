from sqlalchemy import create_engine
from sqlalchemy.sql import select, text

from cred_mysql import credentials

engine = create_engine(
    f"mysql+pymysql://{credentials['username']}:{credentials['password']}@localhost/imagerepository",
     echo=True)

def get_files():
    """Get all files that a user can view"""
    user_code = get_user_code(username)

    s = text("""SELECT P_NAME FROM photos WHERE P_PRIVATE = 0 OR U_CODE is :x""")
    result = engine.connect().execute(s, x=user_code, y=private, z=filename)

    return

def create_file_record(username, filename, private):
    """
    Add the specified file to the MySQL database, for access control reasons

    Arguments:
        username {string} -- The user creating the file
        filename {string} -- The file's name
        private {bool} -- Whether or not the file is private (only the user can see)
    """
    user_code = get_user_code(username)

    bool_code = 1 if private else 0

    s = text("""INSERT INTO photos (U_CODE, P_PRIVATE, P_NAME) VALUES (:x, :y, :z)""")
    result = engine.connect().execute(s, x=user_code, y=bool_code, z=filename)

    return

def get_albums(username):
    """
    Get all albums that a user can view

    Arguments:
        username {string} -- The user accessing the albums
    """
    user_code = get_user_code(username)

    s = text("""SELECT A_NAME, P_NAME FROM albums INNER JOIN photos ON albums.A_ID = photos.A_ID
             WHERE P_PRIVATE = 0 OR photos.U_CODE IS :x""")
    result = engine.connect().execute(s, x=user_code)

    return

def get_user_code(username):
    """
    Get a user's ID code

    Arguments:
        username {string} -- The user
    """
    s = text("""SELECT U_CODE FROM users where U_NAME like :x""")
    result = engine.connect().execute(s, x=username)

    for row in results:
        return row[0]
    return None


def create_album_record(username, album_name, private):
    """
    Add the specified album to the MySQL database, for access control reasons

    Arguments:
        username {string} -- The user creating the album
        album_name {string} -- The album's name
        private {bool} -- Whether or not the album is private (only the user can see)
    """
    user_code = get_user_code(username)

    s = text("""INSERT INTO albums (U_CODE, A_PRIVATE, A_NAME) VALUES (:x, :y, :z)""")
    result = engine.connect().execute(s, x=user_code, y=private, z=album_name)
    return

def login_user(username, password):
    """
    Attempt to login with a username and password combination

    Arguments:
        username {string} -- The user
        password {string} -- The password
    """
    s = text("""SELECT * FROM users WHERE U_NAME LIKE :x AND U_PSWD LIKE :y""")
    result = engine.connect().execute(s, x=username, y=password)

    res = result.first()

    if res is None:
        return 'failure'
    return 'success'

# TODO: verify username, password that they do not contain invalid characters
def create_user(username, password):
    """
    Create a new user account based on the credentials

    Arguments:
        username {string} -- The user
        password {string} -- The password
    """
    s = text("""INSERT INTO users (U_NAME, U_PSWD) VALUES (:x, :y)""")

    result = engine.connect().execute(s, x=username, y=password)
    return

def is_available_check(result):
    """
    Helper method for checking the availability of username, album name, or photo name

    Arguments
        results -- The result from a query to the database engine
    """
    is_available = "true"

    for res in result:
        # If there is a result then this name is taken
        is_available = "false"
        break

    return {'available': is_available}

def check_user_name(username):
    """
    Check if a username is available for use

    Arguments:
        username {string} -- The user
    """
    s = text("""SELECT * FROM users where U_NAME like :x""")

    result = engine.connect().execute(s, x=username)
    return is_available_check(result)

def check_album_name(album_name):
    """
    Check if a username is available for use

    Arguments:
        album_name {string} -- The album name
    """
    s = text("""SELECT * FROM albums where A_NAME like :x""")

    result = engine.connect().execute(s, x=album_name)
    return is_available_check(result)

def check_photo_name(photo_name):
    """
    Check if a username is available for use

    Arguments:
        photo_name {string} -- The photo name
    """
    s = text("""SELECT * FROM photos where P_NAME like :x""")

    result = engine.connect().execute(s, x=photo_name)
    return is_available_check(result)
from sqlalchemy import create_engine
from sqlalchemy.sql import select, text

from cred_mysql import credentials

engine = create_engine(
    f"mysql+pymysql://{credentials['username']}:{credentials['password']}@localhost/imagerepository",
     echo=True)

def get_files(user_code=None):
    """Get all files that a user can view"""

    if user_code is None:
        s = text("""SELECT P_NAME FROM photos WHERE P_PRIVATE = 0 AND A_ID IS NULL""")
        result = engine.connect().execute(s)

    s = text("""SELECT P_NAME FROM photos WHERE (P_PRIVATE = 0 OR U_CODE = :x) AND A_ID IS NULL""")
    result = engine.connect().execute(s, x=user_code)

    files = []

    for row in result:
        files.append(row[0])

    return files

def get_albums(user_code=None):
    """
    Get all albums that a user can view

    Arguments:
        username {string} -- The user accessing the albums
    """

    print(user_code)

    if user_code is None:
        s = text("""SELECT A_NAME, P_NAME FROM albums INNER JOIN photos ON albums.A_ID = photos.A_ID
             WHERE P_PRIVATE = 0""")
        result = engine.connect().execute(s)
    else:
        s = text("""SELECT A_NAME, P_NAME FROM albums INNER JOIN photos ON albums.A_ID = photos.A_ID
                WHERE P_PRIVATE = 0 OR photos.U_CODE = :x""")
        result = engine.connect().execute(s, x=user_code)

    albums = {}

    for row in result:
        try:
            albums[row[0]]
        except KeyError:
            albums[row[0]] = []

        albums[row[0]].append(row[1])
    return albums

def get_user_code(username):
    """
    Get a user's ID code

    Arguments:
        username {string} -- The user
    """
    s = text("""SELECT U_CODE FROM users where U_NAME like :x""")
    result = engine.connect().execute(s, x=username)

    for row in result:
        return row[0]
    return None

def get_album_code(album_name):
    """
    Get an album's ID code

    Arguments:
        album_name {string} -- The album name
    """
    s = text("""SELECT A_ID FROM albums where A_NAME like :x""")
    result = engine.connect().execute(s, x=album_name)

    for row in result:
        return row[0]
    return None

def create_file_record(filename, private, user_code=None, album_code=None):
    """
    Add the specified file to the MySQL database, for access control reasons

    Arguments:
        username {string} -- The user creating the file
        filename {string} -- The file's name
        private {bool} -- Whether or not the file is private (only the user can see)
    """
    bool_code = 1 if private else 0

    if user_code is None and album_code is None:
        s = text("""INSERT INTO photos (P_PRIVATE, P_NAME) VALUES (:y, :z)""")
        result = engine.connect().execute(s, y=bool_code, z=filename)
    elif album_code is None:
        s = text("""INSERT INTO photos (U_CODE, P_PRIVATE, P_NAME) VALUES (:x, :y, :z)""")
        result = engine.connect().execute(s, x=user_code, y=bool_code, z=filename)
    else:
        if user_code is None:
            s = text("""INSERT INTO photos (A_ID, P_PRIVATE, P_NAME) VALUES (:a, :y, :z)""")
            result = engine.connect().execute(s, a=album_code, y=bool_code, z=filename)
        else:
            s = text("""INSERT INTO photos (A_ID, U_CODE, P_PRIVATE, P_NAME) VALUES (:a, :x, :y, :z)""")
            result = engine.connect().execute(s, a=album_code, x=user_code, y=bool_code, z=filename)

    return

def create_album_record(album_name, private, user_code=None):
    """
    Add the specified album to the MySQL database, for access control reasons

    Arguments:
        username {string} -- The user creating the album
        album_name {string} -- The album's name
        private {bool} -- Whether or not the album is private (only the user can see)
    Returns:
        album_code {integer} -- The album's code
    """
    bool_code = 1 if private else 0

    if user_code is None:
        s = text("""INSERT INTO albums (A_PRIVATE, A_NAME) VALUES (:y, :z)""")
        result = engine.connect().execute(s, y=bool_code, z=album_name)
    else:
        s = text("""INSERT INTO albums (U_CODE, A_PRIVATE, A_NAME) VALUES (:x, :y, :z)""")
        result = engine.connect().execute(s, x=user_code, y=bool_code, z=album_name)

    return get_album_code(album_name)

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

def is_available_check(result):
    """
    Helper method for checking the availability of username, album name, or photo name

    Arguments
        results -- The result from a query to the database engine
    """
    is_available = True

    for res in result:
        # If there is a result then this name is taken
        is_available = False
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
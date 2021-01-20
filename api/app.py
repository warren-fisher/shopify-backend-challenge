import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin
from flask import jsonify

from cred_secret import key

import jwt

import sql

from string import ascii_letters, digits

UPLOAD_FOLDER = '../uploads'
ALBUM_FOLDER = './albums'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

ALLOWED_CHARS = ascii_letters + digits + '_'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://images.warrenfisher.net"]}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALBUM_FOLDER'] = ALBUM_FOLDER
app.config['SECRET_KEY'] = key

def get_token(username):
    user_code = sql.get_user_code(username)
    payload = {"username": username, "user_code": user_code}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return token

def decode_token(request):
    try:
        token = request.headers['token']
        if token == '':
            print("no token??")
            return {"username": None, "user_code": None}
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return data
    except Exception as e:
        return {"username": None, "user_code": None}

# TODO: verify this?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_folder(foldername):
    for char in foldername:
        if char not in ALLOWED_CHARS:
            return False
    return True

@app.route('/get/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/get/albums/<album>/<filename>')
def uploaded_file_in_album(album, filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['ALBUM_FOLDER'], album)
    return send_from_directory(path, filename)

def save_file(file, path):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        available = check_photo_name(filename)

        file.save(os.path.join(path, filename))

# TODO: filename conflicts, order of saving file and sql record
@app.route('/post/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'File' not in request.files:
            return redirect(request.url)
        file = request.files['File']
        # if user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        token = decode_token(request)
        isPrivate = True if request.form['private'] == 'on' else False

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            sql.create_file_record(filename, isPrivate, token['user_code'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify([])

# TODO: filename conflicts, order of saving file and sql record
@app.route('/post/upload/album', methods=['POST'])
def upload_album():
    if request.method == 'POST':

        if 'album[]' not in request.files:
            return ''

        files = request.files.getlist("album[]")

        token = decode_token(request)
        isPrivate = True if request.form['private'] == 'on' else False

        albumName = request.form['album_name']
        if not allowed_folder(albumName) or albumName == '':
            return jsonify(['invalid_album_name']),400

        available = sql.check_album_name(albumName)

        while not available:
            albumName += "1"
            available = sql.check_album_name(albumName)

        album_code = sql.create_album_record(albumName, isPrivate, token['user_code'])

        path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['ALBUM_FOLDER'], albumName)
        os.mkdir(path)

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                # TODO what if a file is a duplicate name (within this album)
                sql.create_file_record(filename, isPrivate, token['user_code'], album_code)
                f.save(os.path.join(path, filename))

    return jsonify([])

@app.route('/get/files', methods=['GET'])
def get_files():
    token = decode_token(request)

    filenames = sql.get_files(token['user_code'])

    return jsonify(filenames)

@app.route('/get/albums', methods=['GET'])
def get_albums():

    token = decode_token(request)

    albums = sql.get_albums(token['user_code'])

    return jsonify(albums)

@app.route('/post/login', methods=['POST'])
def login():
    data = request.form

    username = data['user']
    hash_ = data['hash']
    res = sql.login_user(username, hash_)

    if res == 'failure':
        # invalid
        print('fail')
        return jsonify([])
    else:
        # success
        token = get_token(username)
        print(token)
        return jsonify(token)

@app.route('/post/register', methods=['POST'])
def register():
    data = request.form

    username = data['user']
    hash_ = data['hash']
    res = sql.create_user(username, hash_)

    if res == 'failure':
        # invalid
        return jsonify([])
    else:
        # success
        token = get_token(username)
        print(token)
        return jsonify(token)

@app.route('/get/username/<name>')
def check_if_name_available(name):
    return jsonify(sql.check_user_name(name))

@app.route('/post/create/user/<name>/<hash>')
def create_user(name, hash):
    return jsonify(sql.create_user(name, hash))

if __name__ == '__main__':
    app.run(debug=True)
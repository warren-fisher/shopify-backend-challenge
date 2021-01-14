import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin
from flask import jsonify

import sql

UPLOAD_FOLDER = '../uploads'
ALBUM_FOLDER = './albums'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://test.warrenfisher.net"]}}, methods=["POST"])
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALBUM_FOLDER'] = ALBUM_FOLDER

# TODO: verify this?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/get/albums/<album>/<filename>')
def uploaded_file_in_album(album, filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['ALBUM_FOLDER'], album)
    return send_from_directory(path, filename)


# TODO: filename conflicts
@app.route('/post/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'File' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['File']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

@app.route('/get/files', methods=['GET'])
def get_files():

    _, _, filenames = next(os.walk(app.config['UPLOAD_FOLDER']))

    return jsonify(filenames)


@app.route('/post/upload/album', methods=['POST'])
def upload_album():
    if request.method == 'POST':

        if 'album[]' not in request.files:
            return ''

        files = request.files.getlist("album[]")

        # TODO: variable album name
        path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['ALBUM_FOLDER'], 'album1')
        os.mkdir(path)

        for f in files:

            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(path, filename))

    return jsonify([])

@app.route('/get/albums', methods=['GET'])
def get_albums():

    albums = {}

    # TODO: can treat paths better
    path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['ALBUM_FOLDER'])

    _, directories, _ = next(os.walk(path))

    for d in directories:
        album_path = os.path.join(path, d)

        _, _, files = next(os.walk(album_path))

        albums[d] = files

    return jsonify(albums)

@app.route('/get/username/<name>')
def check_if_name_available(name):
    return jsonify(sql.check_user_name(name))

@app.route('/post/create/user/<name>/<hash>')
def create_user(name, hash):
    return jsonify(sql.create_user(name, hash))

if __name__ == '__main__':
    app.run(debug=True)
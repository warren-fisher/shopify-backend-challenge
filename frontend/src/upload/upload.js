import React, {useState} from 'react';

/**
 *
 * @param {*} props.token, the user token
 */
export default function Upload(props) {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [albumName, setAlbumName] = useState();
    const [isPrivate, setPrivate] = useState(false);

    const handleSubmission = e => {
        e.preventDefault();
        const formData = new FormData();

        if (selectedFiles.length == 0) {
            // what to do if no files?

        }
        else if (selectedFiles.length == 1) {
            formData.append("File", selectedFiles[0]);
            formData.append("private", isPrivate);

            fetch('http://localhost:5000/post/upload', {
                method: 'POST',
                body: formData,
                headers: { 'token': props.token }
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));

        } else {
            for (var i = 0; i < selectedFiles.length; i++) {
                formData.append("album[]", selectedFiles[i]);
            }

            formData.append("album_name", albumName);
            formData.append("private", isPrivate);

            fetch('http://localhost:5000/post/upload/album', {
                method: 'POST',
                body: formData,
                headers: {'token': props.token}
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
        }
    }


    return (
        <div id="upload">
            <h1> Upload new image(s)</h1>
            <form method="post" enctype="multipart/form-data">
                <label>
                    <p>Select file(s) to upload</p>
                    <input type="file" name="file" multiple="true" onChange={e => setSelectedFiles(e.target.files)} />
                </label>

                <label>
                    <p>If you are submitting more than one file please include an album name (alphanumeric characters only)</p>
                    <input type="text" name="albumname" onChange={e => setAlbumName(e.target.value)} />
                </label>

                <label>
                    <p>Would you like your file(s) to be private?</p>
                    <input type="checkbox" name="private" onChange={e => setPrivate(e.target.value)} />
                </label>

                <label>
                    <p>Upload your file(s) when you are ready</p>
                    <input type="submit" value="Upload" onClick={handleSubmission} />
                </label>
            </form>
        </div>
    )
}
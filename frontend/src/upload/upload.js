import React, {useState} from 'react';

export default function Upload(props) {
    const [selectedFiles, setSelectedFiles] = useState();
    const [albumName, setAlbumName] = useState();

    const handleChange = (event) => {
        setSelectedFiles(event.target.files);
    }

    const handleSubmission = () => {
        const formData = new FormData();

        if (selectedFiles.length == 0) {
            // what to do if no files?

        }
        else if (selectedFiles.length == 1) {
            formData.append("File", selectedFiles[0]);

            fetch('http://localhost:5000/post/upload', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));

        } else {
            for (var i = 0; i < selectedFiles.length; i++) {
                formData.append(`album[]`, selectedFiles[i]);
            }

            fetch('http://localhost:5000/post/upload/album', {
                method: 'POST',
                body: formData,
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
                    <input type="file" name="file" multiple="true" onChange={handleChange} />
                    <input type="text" name="albumname" onChange={e=>setAlbumName(e)} />
            </form>
            <input type="submit" value="Upload" onClick={handleSubmission} />
        </div>
    )
}
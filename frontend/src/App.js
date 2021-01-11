import logo from './logo.svg';
import './App.css';

import Image from './image.js';

import React, {useState} from 'react';

function App() {
    const [selectedFiles, setSelectedFiles] = useState();

    const [uploadedFiles, setUploadedFiles] = useState([]);



    const getState = () => {
        fetch('http://localhost:5000/get/files')
            .then(response => response.json())
            .then(data => setUploadedFiles(data))
            .catch(error => console.error(error));
    }

    const handleChange = (event) => {
        setSelectedFiles(event.target.files[0]);
    }

    const handleSubmission = () => {
        const formData = new FormData();

        formData.append("File", selectedFiles);

        fetch('http://localhost:5000/post/upload', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));
    }

    return (
        <div className = "App">
            <h1> Upload new File</h1>
            <form method="post" enctype="multipart/form-data">
            <input type ="file" name="file" multiple="true" onChange={handleChange}/>
            </form>
            <input type="submit" value="Upload" onClick={handleSubmission} />
            <input type="submit" value="Get images" onClick={getState}/>

            {/* Display variable # of images based on GET request returning all images */}
            {/* set KEY!!!! for Image comp.*/}

            <div id="imgs">
            {
                uploadedFiles.map((object, i) => <Image image_name={object} key={i}/>)
            }
            </div>

        </div>
    );
}

export default App;
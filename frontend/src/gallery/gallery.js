import React, { useEffect , useState} from 'react';
import Image from '../image.js';

export default function Gallery() {

    const [uploadedFiles, setUploadedFiles] = useState([]);


    const getState = () => {
        return fetch('http://localhost:5000/get/files');
    }

    useEffect(() => {
        getState()
            .then(response => response.json())
            .then(data => setUploadedFiles(data))
            .catch(error => console.error(error));
    }, [])


    return (
        <div id="imgs">
            { uploadedFiles.map((object, i) => <Image image_name={object} key={i} />) }
        </div>
    );
}
import React, { useEffect , useState} from 'react';
import Image from '../image.js';

/**
 *
 * @param {str} props.token, the user token
 */
export default function Gallery(props) {

    const [uploadedFiles, setUploadedFiles] = useState([]);


    const getState = () => {
        return fetch('https://apis.warrenfisher.net/get/files', {
            headers: {
                'token': props.token
            }
        });
    }

    useEffect(() => {
        getState()
            .then(response => response.json())
            .then(data => setUploadedFiles(data))
            .catch(error => console.error(error));
    }, [])


    return (
        <div id="imgs">
            { uploadedFiles.map((object, i) => <Image image_name={object} key={i}/>) }
        </div>
    );
}
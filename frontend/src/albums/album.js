import React, { useEffect, useState } from 'react';
import Image from '../image.js';

export default function Album() {

    const [uploadedAlbums, setUploadedAlbums] = useState([]);


    const getState = () => {
        return fetch('http://localhost:5000/get/albums');
    }

    useEffect(() => {
        getState()
            .then(response => response.json())
            .then(data => setUploadedAlbums(data))
            .catch(error => console.error(error));
    }, [])

    let albumKeys = Object.keys(uploadedAlbums);

    return (

        <div id="albums">

            { albumKeys.map((album, i) => {

                return (
                    <div className="album" key={i}>
                    {uploadedAlbums[album].map((image_name, j) => <Image image_name={image_name} key={j} album_name={album}/>)}
                    </div>
                );

            }
            )}

        </div>
    );
}
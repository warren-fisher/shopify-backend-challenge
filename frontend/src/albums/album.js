import React, { useEffect, useState } from 'react';
import Image from '../image.js';

/**
 * 
 * @param {str} props.token, the user token
 */
export default function Album(props) {

    const [uploadedAlbums, setUploadedAlbums] = useState([]);


    const getState = () => {
        return fetch('https://apis.warrenfisher.net/get/albums', {
            headers: {
                'token': props.token
            }
        });
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
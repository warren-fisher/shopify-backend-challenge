
/**
 * Function component for displaying an image
 *
 * @param {str} props.image_name, name of the file
 * @param {str} props.album_name, name of the album (if the image is from an album)
 */
function Image(props) {

    let url;
    // If this image is from an album the API endpoint for retrieving it is slightly different
    if (props.album_name) {
        url = `https://apis.warrenfisher.net/get/albums/${props.album_name}`;
    } else {
        url = "https://apis.warrenfisher.net/get/files";
    }

    return (
        <div class="image-container">
        <img src={`${url}/${props.image_name}`} />
        </div>
    )
}

export default Image;
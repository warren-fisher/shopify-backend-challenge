function Image(props) {

    return (
        <div class="image-container">
        <img src={`http://localhost:5000/uploads/${props.image_name}`} />
        </div>
    )
}

export default Image;
function Image(props) {

    return (
        <img src={`http://localhost:5000/uploads/${props.image_name}`} />
    )
}

export default Image;
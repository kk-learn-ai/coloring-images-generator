from PIL import Image

def load_image(file_path: str) -> Image.Image:
    """
    Loads an image from a file path using PIL (Python Imaging Library).

    This function opens an image file and returns it as a PIL Image object.
    It can be used to load various image formats supported by PIL.

    Args:
        file_path (str): The path to the image file to be loaded.

    Returns:
        Image.Image: A PIL Image object representing the loaded image.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        PIL.UnidentifiedImageError: If the file is not a valid image or the format is not recognized.

    Example:
        >>> image = load_image("path/to/image.png")
        >>> image.show()  # Display the loaded image
    """
    
    return Image.open(file_path)

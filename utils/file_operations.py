import os
import requests
import zipfile
import io
from typing import List

def save_image(url: str, folder_name: str, image_number: int) -> str | None:
    
    """
    Downloads an image from a URL and saves it to a local file.

    This function creates a folder within the 'download_creation' directory,
    downloads an image from the provided URL, and saves it with a unique filename
    based on the image number.

    Args:
        url (str): The URL of the image to download.
        folder_name (str): The name of the folder to create within 'download_creation'.
        image_number (int): A unique number to append to the image filename.

    Returns:
        str | None: The full path of the saved image file if successful, None otherwise.

    Raises:
        requests.RequestException: If there's an error downloading the image.
        IOError: If there's an error saving the image to the local file system.

    Note:
        This function uses Streamlit's st.error() to display error messages in the UI.
    """
    full_folder_path = os.path.join("download_creation", folder_name)
    os.makedirs(full_folder_path, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error downloading image: {e}")
        return None
    
    file_path = os.path.join(full_folder_path, f"generated_image_{image_number}.png")
    try:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    except IOError as e:
        st.error(f"Error saving image: {e}")
        return None
    
    return file_path

def create_zip_file(folder_name: str) -> io.BytesIO:
    """
    Creates a ZIP file containing all files from a specified folder.

    This function walks through the specified folder within the 'download_creation' 
    directory, adds all files to a ZIP archive, and returns the archive as a bytes buffer.

    Args:
        folder_name (str): The name of the folder within 'download_creation' to zip.

    Returns:
        io.BytesIO: A bytes buffer containing the ZIP file data.

    Raises:
        OSError: If there's an error accessing the folder or its files.
        zipfile.BadZipFile: If there's an error creating the ZIP file.

    Note:
        - The function uses DEFLATE compression for the ZIP file.
        - The original folder structure is preserved in the ZIP file.
        - The returned buffer's position is reset to the beginning for immediate reading.

    Example:
        >>> zip_buffer = create_zip_file("my_images")
        >>> with open("my_images.zip", "wb") as f:
        ...     f.write(zip_buffer.getvalue())
    """
    
    zip_buffer = io.BytesIO()
    full_folder_path = os.path.join("download_creation", folder_name)
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(full_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, full_folder_path)
                zip_file.write(file_path, relative_path)
    zip_buffer.seek(0)
    return zip_buffer

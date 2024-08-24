from openai import OpenAI

def create_openai_client(api_key: str) -> OpenAI:
    """
    Creates and returns an OpenAI client instance.

    This function initializes an OpenAI client using the provided API key.
    The client can be used to interact with various OpenAI services,
    such as generating text or images.

    Args:
        api_key (str): The API key for authenticating with OpenAI services.

    Returns:
        OpenAI: An initialized OpenAI client instance.

    Raises:
        ValueError: If the api_key is None or an empty string.
    """
    if not api_key:
        raise ValueError("API key cannot be None or empty")
    return OpenAI(api_key=api_key)

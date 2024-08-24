from openai import OpenAI
from typing import List

def generate_themes(client: OpenAI) -> List[str]:
    """
    Generate a list of themes for children's coloring book pages using OpenAI's GPT model.

    This function sends a prompt to the OpenAI API requesting 10 suitable themes
    for children's coloring book pages. It then processes the response to return
    a clean list of themes.

    Args:
        client (OpenAI): An initialized OpenAI client instance.

    Returns:
        List[str]: A list of 10 generated themes, each as a separate string.

    Raises:
        openai.OpenAIError: For any API-related errors (e.g., rate limiting, authentication issues).

    Example:
        >>> client = OpenAI(api_key="your-api-key")
        >>> themes = generate_themes(client)
        >>> print(themes)
        ['Underwater Adventure', 'Space Exploration', 'Fairy Tale Forest', ...]
    """
    prompt = "Generate a list of 10 suitable themes for children's coloring book pages."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return [theme.strip('- ') for theme in response.choices[0].message.content.strip().split('\n')]

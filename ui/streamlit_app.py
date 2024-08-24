import os
import streamlit as st
import datetime
from api.openai_client import create_openai_client
from openai import OpenAI, AuthenticationError
from generators.theme_generator import generate_themes
from generators.image_generator import image_prompt, generate_image
from utils.file_operations import save_image, create_zip_file
from utils.image_processing import load_image
from PIL import Image

def get_api_key() -> str:
    """
    Prompts the user to enter their OpenAI API key using a Streamlit password input field.

    This function creates a text input field in the Streamlit app that masks the input,
    suitable for entering sensitive information like API keys. The input is not stored
    or logged by the application for security reasons.

    Returns:
        str: The user-provided OpenAI API key.

    Note:
        The API key is entered as a password field, so it will be masked in the UI.

    Example:
        >>> api_key = get_api_key()
        >>> if api_key:
        ...     # Use the API key to initialize the OpenAI client
        ...     client = OpenAI(api_key=api_key)
    """
    return st.text_input(
        "Enter your OpenAI API key (don't worry, we won't peek)",
        type='password',
        key="api_key_input"
    )

def show_openai_instructions():
    """
    Display instructions for obtaining an OpenAI API key using Streamlit components.

    This function creates an expandable section in the Streamlit app that provides
    step-by-step instructions on how to obtain an OpenAI API key. It includes both
    a brief overview and detailed instructions that can be revealed with a button click.

    The function uses Streamlit's expander and markdown components to structure
    and display the information in a user-friendly format.

    Note:
        This function does not return any value. It directly renders content
        to the Streamlit app interface.

    Example:
        >>> show_openai_instructions()
        # This will display an expander in the Streamlit app with API key instructions
    """
    
    with st.expander("How to Get Your OpenAI API Key", expanded=False):
        st.markdown("""
        ## 🔑 Getting Your OpenAI API Key

        Follow these steps to obtain your OpenAI API key:

        1. Visit [OpenAI's website](https://platform.openai.com/)
        2. Sign up or log in to your account
        3. Navigate to API keys in your account settings
        4. Create a new API key
        5. Copy and securely store your API key
        6. Set up billing in your account
        7. Set usage limits (optional)

        For detailed instructions, click the button below.
        """)
        
        if st.button("View Detailed Instructions"):
            st.markdown("""
            ### Detailed Instructions:

            1. **Visit OpenAI's website**: Go to [https://platform.openai.com/](https://platform.openai.com/)
            2. **Sign up or log in**: 
               - New users: Click "Sign up" and create an account
               - Existing users: Click "Log in"
            3. **Navigate to API keys**: 
               - Look for your account name/icon in the top-right corner
               - Click to open the dropdown menu
               - Select "View API keys"
            4. **Create a new API key**: 
               - Look for "Create new secret key" or "+ New secret key"
               - Optionally, give your key a name
            5. **Copy and save your API key**: 
               - The key will be displayed only once
               - Copy it immediately and store it securely
            6. **Set up billing**: 
               - Find the "Billing" or "Payment" section in account settings
               - Add a payment method
            7. **Set usage limits (optional)**: 
               - In the billing section, you may be able to set spending limits

            Remember to keep your API key confidential and never share it publicly.
            """)

def main():
    st.title("🪄 AI Coloring Images Generator 🖍️")

    st.markdown("""
    Welcome to the cutest corner of the internet! This Streamlit app is your magical gateway to creating adorable coloring pages that will make children (and let's be honest, adults too) squeal with delight.

    ## 🌟 What's This All About?""")
    
    # Load and display the image
    image = Image.open('./images/magic_garden.png')
    st.image(image, caption='Its magical')

    # Load and display the image
    image = Image.open('./images/super.png')
    st.image(image, caption='Its super')
    
    st.markdown("""
    Ever wished you could summon an army of cute, colorable images with just a few clicks? Well, now you can! Our app uses the power of AI to generate custom coloring book pages faster than you can say "pass the crayons!"

    ## 🚀 Features

    🎨 Generate unique coloring pages with various themes
    🔢 Choose how many masterpieces you want (up to 10!)
    📥 Download your creations as a zip file
    🌈 Perfect for rainy days, birthday parties, or when you just need a dose of cuteness
    """)

    show_openai_instructions()  # give an option for pop-up for obtaining OpenAI API key instruction
    
    st.markdown("---")  # This adds a horizontal line for separation

    # Initialize session state for theme if it doesn't exist
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = None

    api_key = get_api_key()
    if api_key:
        try:
            client = create_openai_client(api_key)

            # Test the API key with a simple request
            client.models.list()
            
            if 'themes' not in st.session_state:
                st.session_state.themes = generate_themes(client)
            
            # Use session state to maintain the selected theme
            selected_theme = st.selectbox("Select a theme", st.session_state.themes, key="theme_selector", index=st.session_state.themes.index(
                st.session_state.selected_theme) if st.session_state.selected_theme in st.session_state.themes else 0)

            # Update session state when a new theme is selected
            if selected_theme != st.session_state.selected_theme:
                st.session_state.selected_theme = selected_theme

            num_images = st.slider("Number of images to generate",
                                min_value=1, max_value=10, value=3, key="num_images_slider")

            st.warning(
                f"You've chosen to generate {num_images} images. Please note that generating more images will increase your API usage and costs.")

            if st.button("Generate Images", key="generate_button"):
                st.write(
                    f"Creating images based on '{st.session_state.selected_theme}'")

                folder_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{st.session_state.selected_theme.replace(' ', '_')}"
                generated_file_paths = []

                progress_bar = st.progress(0)
                for i in range(num_images):
                    generate_image_prompt = image_prompt(st.session_state.selected_theme)
                    try:
                        image_url = generate_image(client, generate_image_prompt)
                        file_path = save_image(image_url, folder_name, i + 1)
                        if file_path:
                            generated_file_paths.append(file_path)
                        else:
                            st.warning(f"Failed to save image {i+1}")
                    except Exception as e:
                        st.error(f"Error generating image {i+1}: {str(e)}")
                    progress_bar.progress((i + 1) / num_images)

                st.write(f"Generated {len(generated_file_paths)} images for theme: {st.session_state.selected_theme}")

                if generated_file_paths:
                    for file_path in generated_file_paths:
                        if file_path and os.path.exists(file_path):
                            st.image(file_path)
                        else:
                            st.error(f"Failed to load image: {file_path}")

                    zip_buffer = create_zip_file(folder_name)
                    st.download_button(
                        label="Download Images",
                        data=zip_buffer.getvalue(),
                        file_name=f"{folder_name}.zip",
                        mime="application/zip",
                        key="download_button"
                    )
                else:
                    st.error("No images were generated. Please try again.")

                st.info("Note: These images are generated at 1024x1024 pixels. For best print quality on A4 paper, you may need to scale them up slightly using an image editing software.")

        except AuthenticationError:
            st.error("Invalid API key. Please check your API key and try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter your OpenAI API key to use this app.")

if __name__ == "__main__":
    main()

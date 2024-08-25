import os
from ui.streamlit_app import main

# Set the port to 8501
os.environ['STREAMLIT_SERVER_PORT'] = '8501'

if __name__ == "__main__":
    main()
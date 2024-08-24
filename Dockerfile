FROM python:3.12

# Set the working directory to the location where the Dockerfile is located
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the download_creation directory
RUN mkdir -p download_creation

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8503", "--server.address=0.0.0.0"]

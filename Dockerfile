# Use official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt update && apt install -y portaudio19-dev

# Copy the project files into the container
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command
CMD ["python", "app.py"]

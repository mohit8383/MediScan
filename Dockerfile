FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port (if needed for a web app)
EXPOSE 8000

# Command to run your app
CMD ["python", "gradio_app.py"]

# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /bot

# Copy the project files into the container
COPY . .

# Install required dependencies
RUN apt update && apt install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

# Expose port (not needed for Telegram bots but good for debugging)
EXPOSE 8080

# Command to run the bot
CMD ["python", "main.py"]

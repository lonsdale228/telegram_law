FROM python:3.10.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt from the host to the container's /app directory
COPY requirements.txt .

# Install the requirements inside the container
RUN pip3 install -r requirements.txt

# Set the entry point of the container to execute the main.py file
CMD ["python3", "main.py"]
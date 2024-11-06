#This Docker file is another image to avoid python conflict with Anaconds
# Use the official Python image from Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /web

# Copy the requirements file into the container
COPY require.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r require.txt

# Copy the rest of your application code
COPY . .

# Command to run your application
CMD [".\.venv\Scripts\activate"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]


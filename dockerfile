# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /web

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install Node.js dependencies for Tailwind
COPY home/static/src/package.json /web/home/static/src/
RUN npm install --prefix /web/home/static/src

# Set up tailwind build process
RUN npx tailwindcss -i /web/home/static/src/styles/styles.css -o /app/theme/static/css/main.css --minify

# Expose the port the app runs on
EXPOSE 8000

# Copy the rest of the application code into the container
COPY . /web/

# Run Django development server (or gunicorn for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

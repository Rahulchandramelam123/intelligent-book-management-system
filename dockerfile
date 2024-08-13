# Use the official Python image from the Docker Hub
FROM ubuntu:22.04


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install PostgreSQL development package
RUN apt-get update && \
    apt-get install -y \
    gunicorn \
    python3 \
    python3-pip \
    python3-venv \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt --verbose

# Copy the rest of the application code into the container
COPY . /app/

# Set the default command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]



# Expose the port the app runs on
EXPOSE 8000

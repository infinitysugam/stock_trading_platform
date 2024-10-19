# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev

# Step 4: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 5: Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add MySQL client installation
# RUN apt-get update && apt-get install -y mysql-client
RUN apt-get update && apt-get install -y default-mysql-client



# Step 6: Copy the rest of the application code
COPY . /app

# Step 7: Make port 8000 available to the world outside this container
EXPOSE 8000

# Step 8: Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

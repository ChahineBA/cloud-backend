# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Install python-dotenv to load .env files
RUN pip install python-dotenv

# Use build arguments for secrets
ARG MONGO_URI
ARG MONGO_DB
ARG MONGO_COLLECTION

# Set environment variables using build arguments
ENV MONGO_URI=${MONGO_URI}
ENV MONGO_DB=${MONGO_DB}
ENV MONGO_COLLECTION=${MONGO_COLLECTION}

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
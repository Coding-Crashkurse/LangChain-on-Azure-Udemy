# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn redis requests openai tiktoken langchain typing_extensions python-dotenv python-multipart psycopg2-binary azure-storage-blob pgvector

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy wait-for-postgres.sh into the container and make it executable
COPY ./wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the script to run on container start
ENTRYPOINT ["/wait-for-postgres.sh"]

# Define the command to run the app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

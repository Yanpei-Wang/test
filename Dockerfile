# Use Python 3.11-slim as the base image
FROM python:3.11-slim
# Set the working directory

WORKDIR /code

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
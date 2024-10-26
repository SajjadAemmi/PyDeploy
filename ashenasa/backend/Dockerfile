FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the FastAPI server by default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

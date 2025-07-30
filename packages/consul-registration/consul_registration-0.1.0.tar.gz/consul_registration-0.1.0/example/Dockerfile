FROM python:3.11-slim

WORKDIR /app

# Install the library (in development, use local version)
COPY .. /app
RUN pip install -e .[dev]

# Copy example application
COPY . /app/example

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "example.main:app", "--host", "0.0.0.0", "--port", "8000"]
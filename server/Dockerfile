# Building project with Python 3.12 
FROM python:3.12
# Install dependencies
RUN pip install Flask gunicorn matplotlib
# Copy sources to the app folder in container
COPY src/ /app
WORKDIR /app
# Expose port 8080
ENV PORT 8080
# Init http server gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

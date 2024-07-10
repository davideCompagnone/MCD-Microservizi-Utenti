# Base image

FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy all files (except for those specified in the .dockerignore)
COPY ./requirements.txt ./requirements.txt

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy routers
COPY ./v1 ./v1

# Copy main.py
COPY ./main.py ./main.py

# When running the image, run the command to deploy the web interface
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]

EXPOSE 8080
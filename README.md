# About

A transcription service application that converts speech to text using the whisper-tiny model.

## Features

- Speech-to-text transcription using Whisper (tiny model)
- RESTful API endpoints for transcription management
- File upload support with automatic file name handling
- SQLite database for storing transcriptions
- Search functionality for transcriptions

## Tech Stack

- Backend: Python FastAPI
- Speech Recognition: Whisper (tiny model)
- Database: SQLite

## Setup

Pre-requisites:

- This repo uses Docker and docker-compose. Please make sure those are installed.

Note the build might take over 5 minutes due to the pytorch library having large file size.

### Backend

The backend FastAPI Python server runs within the docker container. By default, the server will run on port 8000. If you'd like to change the port, please create an `.env` file in the backend folder, and populate it as such:

```plaintext
PORT=8080   # The port number
```

If using VSC for development, its recommended to create a virtual environment and install the dependencies in `backend/requirements.txt` to prevent import warnings.

Libraries will be automatically installed within the docker instance.
To start/stop the server docker container, run the following commands:

```bash
docker-compose up --build -d    # To start the server.
docker-compose down             # To stop the server.
```

### Testing

Use the following command to run the backend tests.

```bash
# Ensure you are in the backend folder.
cd /backend
ENVIRONMENT=test pytest
```

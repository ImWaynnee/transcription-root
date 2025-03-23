# Transcription Service

A transcription service application that converts English speech to text using the Whisper-tiny model.

## Features

- Speech-to-text transcription using Whisper (tiny model)
- RESTful API endpoints for transcription management
- File upload support with automatic file name handling
- SQLite database for storing transcriptions
- Search functionality for transcriptions

## Tech Stack

- **Frontend**: React, Vite, Ant Design
- **Backend**: Python, FastAPI
- **Speech Recognition**: Whisper (tiny model)
- **Database**: SQLite

## Setup

### Assumptions

- **Docker and Docker Compose**: Ensure both are installed on your system.
- **Internet Connectivity**: Required to download necessary files for building containers.
- **Ports**:
  - Backend runs on port 8000.
  - Frontend runs on port 4550.

### Application Setup

1. **Start the Container**:

   - Navigate to the root directory of the project (/transcription-root).
   - Run the following command to build and start the backend and frontend server:
     ```bash
     docker-compose up --build -d
     ```
   - It might take a few minutes to start due to large Python dependencies (PyTorch).

2. **Ensure services are running**:

   - You will see `INFO:     Application startup complete.` in the backend container terminal.
   - You will see `VITE v6.1.0  ready in XXX ms` in the frontend container terminal.

### Testing

#### Backend Unit Testing

- Navigate to the `backend` directory.
- Run the tests using:
  ```bash
  ENVIRONMENT=test pytest
  ```

#### Frontend Unit Testing

- Navigate to the `frontend` directory.
- Run the tests using:
  ```bash
  npm run test
  ```

#### Accessing the UI for Manual Testing

- Navigate to 'http://localhost:4550/' in your browser. (Tested on Chrome 134.0.6998.117)

## Notes

- The build process for the backend might take over 5 minutes due to the large file size of the PyTorch library.
- Ensure your Docker and Docker Compose are up to date to avoid compatibility issues.

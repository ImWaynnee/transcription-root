import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, engine, SessionLocal
from app.db.base import Base
import json

# Define client as a global variable
client = TestClient(app)

# Create a fixture for setting up the database once per session
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Override the get_db dependency
    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)

    yield  # This is where the testing happens

    # Drop all tables after the test session
    Base.metadata.drop_all(bind=engine)

def test_transcribe_audio(snapshot):
    # Debugging: Print the current working directory
    print("Current working directory:", os.getcwd())

    # Debugging: List the contents of the current directory
    print("Contents of current directory:", os.listdir(os.getcwd()))

    # Use the test-sample-1.mp3 and test-sample-2.txt files
    with open("src/tests/assets/test-sample-1.mp3", "rb") as audio_file, \
         open("src/tests/assets/test-sample-2.txt", "rb") as text_file:
        files = [
            ('files', ('test-sample-1.mp3', audio_file, 'audio/mpeg')),
            ('files', ('test-sample-2.txt', text_file, 'text/plain'))
        ]
        response = client.post("/transcribe", files=files)

        # Extract and validate the first entry (correct)
        first_entry = response.json()["results"][0]
        assert first_entry["filename"] == "test-sample-1"
        assert "transcription" in first_entry
        assert first_entry["transcription"] == "My name is ethan. I was asked to come here by 11. Now it is already 3 p.m. They did not even serve me any food or drinks. Terrible."

        # Extract and validate the second entry (wrong format)
        second_entry = response.json()["results"][1]
        assert second_entry["filename"] == "test-sample-2.txt"
        error_message = second_entry["error"]

        # Define the expected formats
        expected_formats = [".mp3", ".ogg", ".webm", ".mpga", ".wav", ".m4a", ".mp4", ".flac", ".mpeg"]

        # Check that each expected format is present in the error message
        for fmt in expected_formats:
            assert fmt in error_message, f"Format {fmt} not found in error message"

def test_list_transcriptions(snapshot):
    response = client.get("/transcriptions?page=1&limit=10")

    # Convert the response JSON to a string
    response_json_str = json.dumps(response.json(), indent=2)

    # Use snapshot to compare the response
    snapshot.assert_match(response_json_str, 'list_transcriptions_response')

def test_search_transcription_files(snapshot):
    response = client.get("/search?filename=test&page=1&limit=10")

    # Convert the response JSON to a string
    response_json_str = json.dumps(response.json(), indent=2)

    # Use snapshot to compare the response
    snapshot.assert_match(response_json_str, 'search_transcription_files_response')

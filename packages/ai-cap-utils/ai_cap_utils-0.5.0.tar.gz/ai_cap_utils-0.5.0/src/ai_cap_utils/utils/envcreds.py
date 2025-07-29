import json
import os
import tempfile


def _set_google_credentials(google_credentials: str | dict | None = None):
    if google_credentials:
        # Save the credentials in a temp json file
        # and point to that temp file
        if isinstance(google_credentials, dict):
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".json"
            ) as tmp_file:
                json.dump(google_credentials, tmp_file)
                tmp_file_name = tmp_file.name

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_file_name

        # A path is passed in
        elif isinstance(google_credentials, str):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials


def _set_openai_key(openai_api_key: str | None = None):
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

#!/usr/bin/env python3
"""
YouTube Video Upload via API
Brutal, no-nonsense video uploader
"""

import os
import random
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Scopes required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# API service details
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Valid privacy statuses
VALID_PRIVACY_STATUSES = ("private", "public", "unlisted")

# Maximum retry attempts
MAX_RETRIES = 3

# Retriable exceptions
RETRIABLE_EXCEPTIONS = (HttpError,)

# Retriable status codes
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def authenticate():
    """
    Handle OAuth2 authentication flow
    Returns authenticated service object
    """
    creds = None

    # Token file stores user's access and refresh tokens
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You need to download client_secret.json from Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def upload_video(
    service,
    video_file,
    title,
    description,
    tags=None,
    category_id="22",
    privacy_status="private",
):
    """
    Upload video to YouTube

    Args:
        service: Authenticated YouTube service
        video_file: Path to video file
        title: Video title
        description: Video description
        tags: List of tags (optional)
        category_id: YouTube category ID (default: People & Blogs)
        privacy_status: 'private', 'public', or 'unlisted'

    Returns:
        Video ID if successful, None if failed
    """

    if privacy_status not in VALID_PRIVACY_STATUSES:
        raise ValueError(f"Invalid privacy status: {privacy_status}")

    # Video metadata
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,  # Required field
        },
    }

    # Create media upload object
    media = MediaFileUpload(
        video_file,
        chunksize=-1,  # Upload in single chunk
        resumable=True,
        mimetype="video/*",
    )

    # Call the API's videos.insert method
    insert_request = service.videos().insert(
        part=",".join(body.keys()), body=body, media_body=media
    )

    # Execute upload with retry logic
    return resumable_upload(insert_request)


def resumable_upload(insert_request):
    """
    Handle resumable upload with retry logic
    """
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                print("Maximum retries exceeded. Upload failed.")
                return None

            max_sleep = 2**retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...")
            time.sleep(sleep_seconds)

    if "id" in response:
        print(f"Video uploaded successfully! Video ID: {response['id']}")
        print(f"URL: https://www.youtube.com/watch?v={response['id']}")
        return response["id"]
    else:
        print(f"Upload failed with unexpected response: {response}")
        return None


def main():
    """
    Main execution function
    """
    # File to upload
    video_file = "path/to/your/video.mp4"

    # Video details
    title = "My Video Title"
    description = """
    Video description here.
    Can include multiple lines.
    """
    tags = ["tag1", "tag2", "tag3"]

    # Authenticate and get service
    try:
        service = authenticate()
        print("Authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    # Upload video
    try:
        video_id = upload_video(
            service=service,
            video_file=video_file,
            title=title,
            description=description,
            tags=tags,
            privacy_status="private",  # Keep it private
        )

        if video_id:
            print(f"Success! Video uploaded with ID: {video_id}")
        else:
            print("Upload failed!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

"""
DEPENDENCIES (install with pip):
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

SETUP REQUIREMENTS:
1. Google Cloud Console project with YouTube Data API v3 enabled
2. OAuth2 credentials (client_secret.json)
3. Video file to upload
4. Proper scopes and permissions

CATEGORY IDs (common ones):
- 1: Film & Animation
- 2: Autos & Vehicles  
- 10: Music
- 15: Pets & Animals
- 17: Sports
- 19: Travel & Events
- 20: Gaming
- 22: People & Blogs (default)
- 23: Comedy
- 24: Entertainment
- 25: News & Politics
- 26: Howto & Style
- 27: Education
- 28: Science & Technology

PRIVACY STATUS OPTIONS:
- 'private': Only you can see it
- 'unlisted': Anyone with link can see it
- 'public': Everyone can find and watch it
"""

from googleapiclient.discovery import build


def get_comments(video_id, api_key, next_page_token=None):
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100,
        pageToken=next_page_token,
    )
    response = request.execute()

    return response


def fetch_all_comments(video_id, api_key):
    next_page_token = None
    with open("comments.txt", "w", encoding="utf-8") as file:
        while True:
            response = get_comments(video_id, api_key, next_page_token)
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author = item["snippet"]["topLevelComment"]["snippet"][
                    "authorDisplayName"
                ]
                file.write(f"Comment by {author}: {comment}\n")

            next_page_token = response.get("nextPageToken")
            if next_page_token is None:
                break


if __name__ == "__main__":
    api_key = (
        "AIzaSyCWw-kqZTdKtR6G7c7KDjdZvKgh3f5qlkk"  # Replace with your actual API key
    )
    video_id = "4k6Xgjqkad4"  # Replace with the ID of the video you want to fetch comments from
    fetch_all_comments(video_id, api_key)

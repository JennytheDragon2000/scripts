import youtube_dl
import sys


def get_rss_feed_url(video_url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        if "channel_id" in info_dict:
            channel_id = info_dict["channel_id"]
            rss_feed_url = (
                f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            )
            return rss_feed_url
        else:
            return "Channel ID not found."


# Example usage
# video_url = "https://www.youtube.com/watch?v=aLx2q-UnH6M"
video_url = sys.argv[1]
rss_feed_url = get_rss_feed_url(video_url)
print(rss_feed_url)

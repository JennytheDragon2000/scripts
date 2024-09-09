#!/usr/bin/python3
import os
import sys

import assemblyai as aai
from moviepy.editor import VideoFileClip


def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = video_file.rsplit(".", 1)[0] + ".wav"
    audio.write_audiofile(audio_file)
    video.close()
    return audio_file


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_file>")
        sys.exit(1)

    video_file = sys.argv[1]

    if not video_file.lower().endswith((".mp4", ".mkv")):
        print("Error: Input file must be an MP4 or MKV file.")
        sys.exit(1)

    # Extract audio from video
    audio_file = extract_audio(video_file)

    # Transcribe audio
    aai.settings.api_key = "54f7cd570f054d41afce93000bbf56f2"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    # Generate subtitles
    subtitles = transcript.export_subtitles_srt()

    # Write subtitles to file
    output_file = os.path.splitext(video_file)[0] + ".srt"
    with open(output_file, "w") as f:
        f.write(subtitles)

    # Clean up temporary audio file
    os.remove(audio_file)

    print(f"Subtitles saved to {output_file}")


if __name__ == "__main__":
    main()

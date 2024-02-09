#! /usr/bin/python3

import sys

audio_file_name = sys.argv[1]

import assemblyai as aai

aai.settings.api_key = "54f7cd570f054d41afce93000bbf56f2"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_file_name)
# transcript = transcriber.transcribe("./my-local-audio-file.wav")
subtitles = transcript.export_subtitles_srt()

splitted = audio_file_name.split("/")[-1].split(".")[0]


f = open(f"{splitted}.srt", "a")
f.write(subtitles)
f.close

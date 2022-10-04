import os
import pathlib


given_audio_file_path = os.path.join(pathlib.Path(
    __file__).parent.absolute(), "files", "artist_audio_music.mp3")

given_cover_file_path = os.path.join(pathlib.Path(
    __file__).parent.absolute(), "files", "artist_cover_music.jpg")

given_files = {"audio_file": ("artist_audio_music.mp3", open(given_audio_file_path, "rb"), "audio/mpeg"), "cover_file": (
    "artist_cover_music.jpg", open(given_cover_file_path, "rb"), "image/jpeg")}

given_wrong_files = {"cover_file": ("artist_audio_music.mp3", open(given_audio_file_path, "rb"), "audio/mpeg"), "audio_file": (
    "artist_cover_music.jpg", open(given_cover_file_path, "rb"), "image/jpeg")}

given_music = {"music_title": "music", "music_genre": "Pop"}

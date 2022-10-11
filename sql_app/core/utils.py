
from fastapi import HTTPException, status


async def check_files_types(audio_file, cover_file):
    errors = {}
    if audio_file.content_type != "audio/mpeg" and audio_file.content_type != "audio/wav":
        errors["audio_file"] = "Audio file must be mp3 or wav"
    if cover_file.content_type != "image/jpeg" and cover_file.content_type != "image/png":
        errors["cover_file"] = "Cover file must be jpeg or png"

    if len(errors.keys()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=errors)

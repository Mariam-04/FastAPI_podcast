from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from podcast_generator import (
    generate_podcast_script_text,
    parse_script_to_segments,
    generate_and_combine_audio_from_segments
)

load_dotenv()
app = FastAPI()

class PodcastRequest(BaseModel):
    topic: str
    llm_model: str = "gpt-4"
    llm_provider: str = "openai"
    host_voice: str = "default_host_id"
    guest_voice: str = "default_guest_id"
    output_audio_filename: str = "podcast.mp3"
    output_script_filename: str = "podcast_script.txt"

class PodcastResponse(BaseModel):
    success: bool
    message: str
    audio_path: str
    script_path: str

@app.post("/generate_podcast", response_model=PodcastResponse)
async def generate_podcast(data: PodcastRequest):
    try:
        script = generate_podcast_script_text(data.topic, data.llm_model, data.llm_provider)
        with open(data.output_script_filename, "w", encoding="utf-8") as f:
            f.write(script)

        segments = parse_script_to_segments(script)
        if not segments:
            raise HTTPException(status_code=400, detail="Script parsing failed.")

        generate_and_combine_audio_from_segments(
            segments,
            data.host_voice,
            data.guest_voice,
            data.output_audio_filename
        )

        return PodcastResponse(
            success=True,
            message="Podcast generated successfully.",
            audio_path=data.output_audio_filename,
            script_path=data.output_script_filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

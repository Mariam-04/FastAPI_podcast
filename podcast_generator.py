from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

from podcast_generator import (
    generate_podcast_script_text,
    parse_script_to_segments,
    generate_and_combine_audio_from_segments
)

app = FastAPI()

class PodcastRequest(BaseModel):
    topic: str
    llm_model: str = "gpt-3.5-turbo"
    llm_provider: str = "openai"
    host_voice: str = "your_host_voice_id"
    guest_voice: str = "your_guest_voice_id"
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
        script_text = generate_podcast_script_text(
            topic=data.topic,
            llm_model=data.llm_model,
            llm_provider=data.llm_provider
        )

        with open(data.output_script_filename, "w", encoding="utf-8") as f:
            f.write(script_text)

        segments = parse_script_to_segments(script_text)
        if not segments:
            raise HTTPException(status_code=400, detail="No valid dialogue segments parsed.")

        generate_and_combine_audio_from_segments(
            segments,
            host_voice_id=data.host_voice,
            guest_voice_id=data.guest_voice,
            output_path=data.output_audio_filename
        )

        return PodcastResponse(
            success=True,
            message="Podcast generated successfully.",
            audio_path=data.output_audio_filename,
            script_path=data.output_script_filename
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

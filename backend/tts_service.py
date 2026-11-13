import os
import asyncio
import logging
from pathlib import Path
import edge_tts
from .config import AUDIO_DIR

logger = logging.getLogger(__name__)

# Available High-Quality IELTS Accents
IELTS_VOICES = {
    "british_female": "en-GB-SoniaNeural",
    "british_male": "en-GB-RyanNeural",
    "australian_female": "en-AU-NatashaNeural",
    "australian_male": "en-AU-WilliamNeural",
    "american_female": "en-US-JennyNeural",
    "american_male": "en-US-GuyNeural"
}

async def generate_speech(text: str, voice_key: str = "british_female", filename: str = None) -> str:
    """
    Generates an audio file from text using edge-tts.
    Returns the relative path from the server root e.g. /audio/filename.mp3
    """
    if not filename:
        import hashlib
        h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]
        filename = f"listening_{h}.mp3"
    
    file_path = AUDIO_DIR / filename
    if file_path.exists():
        return f"/audio/{filename}"

    voice = IELTS_VOICES.get(voice_key, "en-GB-SoniaNeural")
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await asyncio.wait_for(communicate.save(str(file_path)), timeout=5.0)
        logger.info("Generated TTS audio at %s using voice %s", file_path, voice)
        return f"/audio/{filename}"
    except Exception as e:
        logger.warning("Could not generate TTS audio (offline or timeout): %s", e)
        # Create an empty or placeholder file so client doesn't break
        if not file_path.exists():
            file_path.write_bytes(b"")
        return f"/audio/{filename}"

async def generate_ielts_dialogue(dialogue_script: list, output_filename: str) -> str:
    """
    Generates a dialogue between two speakers (e.g., Section 1 hotel booking or Section 3 tutorial)
    dialogue_script = [
       {"voice": "british_female", "text": "Good morning, city library, how can I help?"},
       {"voice": "british_male", "text": "Hi, I'd like to sign up for a student membership please."}
    ]
    """
    out_path = AUDIO_DIR / output_filename
    if out_path.exists():
        return f"/audio/{output_filename}"

    # For simple seamless dialogue, concatenate text or generate individual pieces
    # In edge-tts, we can concatenate audio bytes
    combined_audio = bytearray()
    
    for item in dialogue_script:
        voice = IELTS_VOICES.get(item.get("voice", "british_female"), "en-GB-SoniaNeural")
        comm = edge_tts.Communicate(item["text"], voice)
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                combined_audio.extend(chunk["data"])
    
    with open(out_path, "wb") as f:
        f.write(combined_audio)
        
    return f"/audio/{output_filename}"

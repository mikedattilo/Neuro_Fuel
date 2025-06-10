# Create main function
def script_to_audio(api_key, script, voice_id):
    import requests

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": script,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to generate audio: {response.status_code} - {response.text}")
    else:
        print(f"Audio generated successfully: {response.status_code}")

    return response.content

def openai_tts_audio(api_key, script, voice_id):
    import requests
    import os

    # If script is a path to a file, read the file contents
    if os.path.isfile(script):
        with open(script, "r", encoding="utf-8") as f:
            script_text = f.read()
    else:
        script_text = script  # Use the string as-is

    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tts-1-hd",
        "input": script_text,
        "voice": voice_id,
        "response_format": "mp3"
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError:
        print(f"\n[OpenAI API Error] {response.status_code} {response.reason}")
        print("Response:", response.text)
        raise

def play_audio_bytes(audio_bytes):
    import pygame
    import tempfile
    import os
    import time

    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name
        tmp.write(audio_bytes)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Fully shut down the mixer
    finally:
        time.sleep(0.2)  # Still give Windows a moment
        try:
            os.remove(tmp_path)
        except PermissionError:
            print(f"⚠️ Couldn't delete temp file (still in use): {tmp_path}")
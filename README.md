**NeuroFuel:** Automated YouTube Shorts Creator
NeuroFuel is a Python-based pipeline that generates short, engaging scripts, converts them to realistic speech, and produces ready-to-upload vertical videos—perfect for YouTube Shorts, TikTok, or Instagram Reels.

**What It Does**
**Script Generation:** Uses the Groq API to generate short-form, motivational scripts tailored to the day of the week.

**Voice Synthesis:** Converts scripts to high-quality speech using OpenAI’s TTS or ElevenLabs.

**Visual Creation:** Downloads a random vertical stock video from Pexels for use as a dynamic background.

**Video Editing:** Combines text, audio, and video—overlaying the script on the background and syncing video length to audio duration.

**Automated Output:** Saves each component (script, audio, video) and the final video to a dated project folder for easy management.

**Key Features**
Fully automated end-to-end video generation (run_all_content.py).

Modular, easy-to-extend code for each major task:

**Script generation:** generate_text_script.py

**Audio synthesis:** text_to_voice.py

**Background selection:** choose_background.py

**Asset management:** utils.py

**Video assembly:** create_video.py

API keys are loaded securely from a .env file.

**Quickstart**
Set your API keys in variables.env (GROQ_API_KEY, OPENAI_API_KEY, PEXELS_API_KEY).

**Run the pipeline:** python run_all_content.py
Find your video in the video_projects/<YYYY-MM-DD>/ directory.

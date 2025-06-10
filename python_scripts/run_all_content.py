from generate_text_script import initialize_groq_client, generate_text_script
from text_to_voice import openai_tts_audio
from utils import get_todays_date, check_api_key, load_api_key
from choose_background import get_background_video, get_random_query
from choose_background import get_stock_media_files, get_stock_media_path
from create_video import match_video_and_audio_duration, merge_text_audio_video, save_edited_media
from utils import save_string_as_txt, save_audio_bytes, save_background_video
from utils import check_create_dated_folder, check_create_components_folder

def main():
    # Get today's date
    todays_date = get_todays_date()

    # Check and/or create output directories for final video & video components
    output_dir_folder = r'video_projects'
    dated_output_dir = check_create_dated_folder(todays_date, output_dir_folder) # Finished video output directory
    final_output_path = f"{dated_output_dir}\\output_video.mp4"

    components_output_dir = check_create_components_folder(dated_output_dir, "video_components") # Components output directory
    
    # Get all API keys from the environment
    variables_file = "variables.env"
    env_var_names = ["GROQ_API_KEY", "OPENAI_API_KEY"]

    api_keys = {} # Create empty dictionary to store API keys

    for env_var_name in env_var_names:
        api_key = load_api_key(env_var_name, variables_file) # Load API key from variables.env
        check_api_key(api_key) # Check if the API key is set
    
        key_name = env_var_name.lower() 
        api_keys[key_name] = api_key

    # Initialize Groq client
    groq_client = initialize_groq_client(api_keys["groq_api_key"])

    # Generate a script
    script = generate_text_script(groq_client)
    print(f"Script successfully generated.")

    # Create a dictionary of voice IDs and pick one
    openai_voices = {
    1: "alloy",
    2: "echo",
    3: "fable",
    4: "nova",
    5: "onyx",
    6: "shimmer",
    7: "ash",
    8: "sage",
    9: "coral"
    }

    voice_id = openai_voices[7]

    # Generate audio from the script
    audio_bytes = openai_tts_audio(api_keys["openai_api_key"], script, voice_id) # binary MP3 data

    # Select a random stock media video
    import random
    video_files = get_stock_media_files('stock_media')     # List of video filenames
    chosen_video = random.choice(video_files)              # Pick one at random
    video_file_path = get_stock_media_path(chosen_video)   # Get the correct Path object

    # Read the video as bytes (if you still need the bytes for your saving function)
    with open(video_file_path, 'rb') as f:
        background_video = f.read()

    # Save the script, audio, and background video to established file directory
    text_file_path = save_string_as_txt(script, "txt", components_output_dir)
    audio_file_path = save_audio_bytes(audio_bytes, "mp3", components_output_dir)
    video_file_path = save_background_video(background_video, "mp4", components_output_dir)

    # Edit the video to match the audio
    edited_video = match_video_and_audio_duration(audio_file_path, video_file_path)
    edited_video_file_path = save_edited_media(edited_video, components_output_dir)
    
    # Merge everything and create the final video
    merge_text_audio_video(text_file_path, audio_file_path, edited_video_file_path, final_output_path)

if __name__ == "__main__":
    main()
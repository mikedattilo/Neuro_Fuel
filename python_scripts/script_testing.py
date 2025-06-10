from utils import save_string_as_txt, save_audio_bytes, save_background_video
from utils import get_todays_date, check_create_dated_folder, check_create_components_folder
from utils import load_api_key, check_api_key
from text_to_voice import openai_tts_audio
from create_video import match_video_and_audio_duration, merge_text_audio_video, save_edited_media

todays_date = get_todays_date()

# Check and/or create output directories for final video & video components
output_dir_folder = r'video_projects'
dated_output_dir = check_create_dated_folder(todays_date, output_dir_folder) # Finished video output directory
final_output_path = f"{dated_output_dir}\\output_video.mp4"

components_output_dir = check_create_components_folder(dated_output_dir, "video_components") # Components output directory

text_file_path = r'c:\Users\miked\OneDrive\Documents\GitHub\Neuro_Fuel\video_projects\2025-05-26\video_components\test_script.txt'
audio_file_path = r'c:\Users\miked\OneDrive\Documents\GitHub\Neuro_Fuel\video_projects\2025-05-26\video_components\test_audio.mp3'
video_file_path = r'c:\Users\miked\OneDrive\Documents\GitHub\Neuro_Fuel\video_projects\2025-05-26\video_components\test_background.mp4'
variables_file = "variables.env"
output_dir_folder = r'test_variables'
env_var_name = "OPENAI_API_KEY"

api_key = load_api_key(env_var_name, variables_file)  # Load API key from variables.env
check_api_key(api_key)  # Check if the API key is set

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

voice_id = openai_voices[1]  # This will set voice_id to "alloy"


edited_video = match_video_and_audio_duration(audio_file_path, video_file_path)
edited_video_file_path = save_edited_media(edited_video, components_output_dir)

# Merge everything and create the final video
merge_text_audio_video(text_file_path, audio_file_path, edited_video_file_path, final_output_path)



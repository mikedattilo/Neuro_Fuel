# Function to match video and audio durations
def match_video_and_audio_duration(audio_file_path, video_file_path):
    import math
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.editor import concatenate_videoclips

    # State what is happening
    print("Checking and matching audio and video durations...")

    # Load clips
    audio_clip = AudioFileClip(str(audio_file_path))
    video_clip = VideoFileClip(str(video_file_path))
    audio_duration = audio_clip.duration
    print("Audio duration (seconds):", audio_duration)
    video_duration = video_clip.duration
    print("Video duration (seconds):", video_duration)

    target_duration = audio_duration + 1  # Add 1 second buffer

    if video_duration < target_duration:
        print("Video is shorter than audio. Repeating video to match target duration.")
        n_repeats = math.ceil(target_duration / video_duration)
        repeated_clips = [video_clip] * n_repeats
        combined_video = concatenate_videoclips(repeated_clips)
        edited_video = combined_video.subclip(0, target_duration)
    else:
        print("Video is longer than target duration. Trimming video to match target duration.")
        edited_video = video_clip.subclip(0, target_duration)

    print("Edited video duration (seconds):", edited_video.duration)

    return edited_video

# Function to save edited audio and video files to components directory
def save_edited_media(edited_video, save_dir):
    import os

    video_output_path = os.path.join(save_dir, "edited_background.mp4")

    print(f"Saving edited video to {video_output_path} ...")
    edited_video.write_videofile(video_output_path, codec='libx264', audio_codec='aac')

    print("Save complete.")

    return video_output_path

# Function to merge text, audio, and video into a final video
def merge_text_audio_video(text_path, audio_path, video_path, output_video_path):
    import os
    from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip
    import moviepy.config as mpy_config
    from pathlib import Path

    # Establish the path to ImageMagick
    print("Establishing ImageMagick path...")
    project_root = Path(__file__).parent
    imagemagick_dirs = [d for d in project_root.iterdir() if d.is_dir() and d.name.startswith("ImageMagick-")]
    if not imagemagick_dirs:
        raise FileNotFoundError("No ImageMagick portable folder found in the project directory.")
    magick_path = imagemagick_dirs[0] / "magick.exe"

    if not magick_path.exists():
        raise FileNotFoundError(f"'magick.exe' not found in {imagemagick_dirs[0]}. Please extract the portable ImageMagick release here.")

    mpy_config.change_settings({"IMAGEMAGICK_BINARY": str(magick_path)})
    print(f"ImageMagick path established: {magick_path}")

    # Check if the output path is a file
    if os.path.isdir(output_video_path):
        raise ValueError(f"Output path must be a file, not a directory: {output_video_path}")

    # Load audio and video clips
    video_clip = VideoFileClip(str(video_path))
    audio_clip = AudioFileClip(str(audio_path))

    # Merge audio and video
    with open(text_path, 'r', encoding='utf-8') as f:
        overlay_text = f.read()

    # txt_clip = TextClip(overlay_text)
    txt_clip = TextClip(
        overlay_text, fontsize=50, color='white', size=video_clip.size, method='caption', align='center', font='Arial'
    ).set_duration(video_clip.duration)

    # Composite video + text
    video_with_text = CompositeVideoClip([video_clip, txt_clip.set_position('center')])

    # Set audio
    video_with_text = video_with_text.set_audio(audio_clip)

    # Export with audio
    video_with_text.write_videofile(str(output_video_path), codec='libx264', audio_codec='aac')

    # Return raw bytes
    with open(output_video_path, 'rb') as file:
        video_bytes = file.read()
    return video_bytes
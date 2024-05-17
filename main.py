import requests
from decouple import config
from fastapi import FastAPI
import assemblyai as aai
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


# Set up the AssemblyAI client
aai.settings.api_key = config("ASSEMBLYAI_API_KEY")
transcriber = aai.Transcriber()


# Define a function to download a video file from a URL
def download_video(url, filename):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        # Open a local file in binary write mode
        with open(filename, 'wb') as file:
            # Write the content of the response to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


# Define a function to extract audio from a video file
def extract_audio_from_video(video_file_path, output_audio_path):
    # Load the video file
    video = VideoFileClip(video_file_path)
    # Extract the audio from the video
    audio = video.audio
    # Write the audio to a file
    audio.write_audiofile(output_audio_path)
    # Close the video file to free up resources
    video.close()


# Define a function to get the resolution and duration of a video file
def get_resolution_and_duration_from_video(video_file_path):
    # Load the video file
    video = VideoFileClip(video_file_path)
    # Get the resolution of the video
    resolution = video.size
    # Get the duration of the video
    duration = video.duration
    # Close the video file to free up resources
    video.close()
    return resolution, duration


# Create a FastAPI instance
app = FastAPI()


# Define a route handler for the default route, for health checks
@app.get("/")
async def version():
    return {"version": "v0.1"}


# Define a route handler for the /process_video route
@app.get("/process_video")
async def process_video(video_url: str):
    # Download the video file from the URL and save it locally
    print("Downloading video...")
    video_filename = "video.mp4"
    download_video(video_url, video_filename)

    # Get audio from video file with MoviePy
    print("Extracting audio from video...")
    audio_filename = "audio.mp3"
    extract_audio_from_video(video_filename, audio_filename)

    # Get resolution and duration of the video
    print("Getting resolution and duration...")
    resolution, duration = get_resolution_and_duration_from_video(video_filename)
    # Format the resolution as a string
    resolution = f"{resolution[0]}x{resolution[1]}"

    # Transcribe the audio with AssemblyAI
    print("Transcribing audio...")
    transcript = transcriber.transcribe(audio_filename)

    # Generate tags for the video
    print("Generating tags...")
    prompt_tags = ("Generate a list of tags (max 5) for this video."
                   "Return only the tags, separated by commas and nothing else.")
    result = transcript.lemur.task(prompt_tags)
    tags = result.response.replace("\n", " ").split(",")
    # Trim the tags
    tags = [tag.strip() for tag in tags]
    # Limit the number of tags to 5
    tags = tags[:5]

    # Generate the categories for the video
    print("Generating categories...")
    prompt_categories = ("Generate a list of categories (max 3) for this video."
                         "Return only the categories, separated by commas and nothing else.")
    result = transcript.lemur.task(prompt_categories)
    categories = result.response.replace("\n", " ").split(",")
    # Trim the categories
    categories = [category.strip() for category in categories]
    # Limit the number of categories to 3
    categories = categories[:3]

    # Delete the video and audio files
    print("Cleaning up...")
    os.remove(video_filename)
    os.remove(audio_filename)

    # Return the tags and categories
    print("Processing complete!")
    record = {"tags": tags, "categories": categories, "resolution": resolution, "duration": duration}
    print(record)
    return record

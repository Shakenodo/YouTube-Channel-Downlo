import subprocess
import os
import json

def fetch_channel_videos(channel_url, num_videos=5, sort_by='date'):
    """
    Fetches video URLs from a channel, sorts them, and returns a list of video URLs.

    :param channel_url: The URL of the channel.
    :param num_videos: Number of videos to fetch.
    :param sort_by: Sorting method, 'date' for newest first, 'popular' for most popular.
    :return: List of video URLs.
    """
    # Fetch video metadata using yt-dlp
    command = [
        'yt-dlp',
        '--flat-playlist',
        '--dump-json',
        channel_url
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        videos = [json.loads(line) for line in result.stdout.splitlines()]

        if sort_by == 'popular':
            videos.sort(key=lambda v: v.get('view_count', 0), reverse=True)
        elif sort_by == 'date':
            videos.sort(key=lambda v: v.get('upload_date', ''), reverse=True)

        # Return only the top `num_videos` URLs
        return [f"https://www.youtube.com/watch?v={video['id']}" for video in videos[:num_videos]]

    except subprocess.CalledProcessError as e:
        print(f"Error fetching video metadata: {e}")
        return []

def download_video(url, output_dir='downloads', extract_audio=False, additional_options=None):
    """
    Downloads a video using yt-dlp.

    :param url: The URL of the video to download.
    :param output_dir: The directory to save the downloaded video.
    :param extract_audio: If True, extracts audio only.
    :param additional_options: Additional options for yt-dlp.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [
        'yt-dlp',
        url,
        '-o', f'{output_dir}/%(title)s.%(ext)s'
    ]

    if extract_audio:
        command.extend(['-x', '--audio-format', 'mp3'])
    else:
        command.extend(['--merge-output-format', 'mp4'])

    if additional_options:
        command.extend(additional_options)

    try:
        subprocess.run(command, check=True)
        print(f"Download completed: {url}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while downloading {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def download_channel_videos(channel_url, num_videos=5, sort_by='date', extract_audio=False, output_dir='downloads'):
    """
    Downloads a set number of videos from a channel, sorted by date or popularity.

    :param channel_url: The URL of the channel to download videos from.
    :param num_videos: The number of videos to download.
    :param sort_by: Sorting method, 'date' or 'popular'.
    :param extract_audio: If True, extracts audio only.
    :param output_dir: The directory to save the downloaded videos.
    """
    video_urls = fetch_channel_videos(channel_url, num_videos=num_videos, sort_by=sort_by)

    for url in video_urls:
        download_video(url, output_dir=output_dir, extract_audio=extract_audio)

def main():
    channel_url = 'https://www.youtube.com/' # Enter channel link here
    num_videos = 5
    sort_by = 'popular'  # Change to 'date' for newest videos or 'popular' for most popular videos
    extract_audio = True  # Set to True to extract audio only

    download_channel_videos(channel_url, num_videos=num_videos, sort_by=sort_by, extract_audio=extract_audio)

if __name__ == '__main__':
    main()

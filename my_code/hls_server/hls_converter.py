import os
from werkzeug.utils import secure_filename
import subprocess
import json


def get_audio_info(file_path):
    """
    Get information about an audio file using ffprobe.

    Args:
        file_path (str): The path to the audio file.

    Returns:
        dict: A dictionary containing information about the audio file.
    """
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-select_streams",
        "a",
        file_path,
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = json.loads(result.stdout)
    if "streams" not in info or len(info["streams"]) == 0:
        raise ValueError(f"No audio streams found in file {file_path}")
    return info


def convert_to_hls(file_path):
    """
    Convert an audio file into a full HLS streaming m3u8 URL.

    This function receives a path to an audio file, converts it into a HLS streaming m3u8 URL
    and returns the URL for further processing.
    """
    filename = secure_filename(os.path.basename(file_path))
    file_dir = os.path.dirname(file_path)

    if filename is None:
        return "Invalid file name"

    # Get information about the audio file
    info = get_audio_info(os.path.join(file_dir, filename))
    audio_info = info["streams"][0]

    # Set the audio codec for the output file based on the input file
    audio_codec = "pcm_s16le" if audio_info["sample_fmt"] in ["s16", "s16p"] else "aac"

    # Ensure the output directory exists
    output_dir = "./my_code/assets/hls"
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            os.path.join(file_dir, filename),
            "-c:a",
            audio_codec,
            "-start_number",
            "0",
            "-hls_time",
            "10",
            "-hls_list_size",
            "0",
            "-f",
            "hls",
            os.path.join(output_dir, filename + ".m3u8"),
        ]
    )
    return os.path.join(output_dir, filename + ".m3u8")


if __name__ == "__main__":
    print(
        convert_to_hls(
            "/Users/hassen/Dev/Jeenie/whisper-live-fork/WhisperLive/my_code/assets/audio/audio_1_resampled.wav"
        )
    )

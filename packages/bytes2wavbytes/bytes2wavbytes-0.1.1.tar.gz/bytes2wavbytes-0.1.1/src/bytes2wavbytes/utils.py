import io
import tempfile
import subprocess
import magic

def detect_mime_type(input_bytes):
    """
    Use python-magic to detect mime type from bytes.
    """
    mime = magic.Magic(mime=True)
    return mime.from_buffer(input_bytes)

def guess_suffix_from_mime(mime_type):
    """
    Guess file extension from mime type for tempfile.
    """
    mapping = {
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/x-pcm": ".pcm",
        "audio/mp3": ".mp3",
        "audio/mpeg": ".mp3",
        "audio/flac": ".flac",
        "audio/x-flac": ".flac",
        "audio/aac": ".aac",
        "audio/ogg": ".ogg",
        "audio/x-vorbis+ogg": ".ogg",
        "audio/opus": ".opus",
        "audio/x-opus+ogg": ".opus",
        "audio/webm": ".webm",
        "audio/amr": ".amr",
        "video/mp4": ".mp4",
        "video/quicktime": ".mov",
        "video/x-matroska": ".mkv",
        "video/webm": ".webm",
        "video/avi": ".avi",
        "video/x-msvideo": ".avi",
        "video/mpeg": ".mpeg",
        "video/3gpp": ".3gp",
        "video/ogg": ".ogv"
    }
    return mapping.get(mime_type, ".bin")

def is_streamable_mime(mime_type):
    """
    Return True if the given mime type is streamable (can be piped to ffmpeg stdin).
    """
    streamable_mimes = {
        "audio/wav",
        "audio/x-wav",
        "audio/x-pcm",
        "audio/mpeg",
        "audio/mp3",
        "audio/flac",
        "audio/x-flac",
        "audio/aac",
        "audio/ogg",
        "audio/x-vorbis+ogg",
        "audio/opus",
        "audio/x-opus+ogg",
        "audio/webm",
        "audio/amr"
    }
    return mime_type in streamable_mimes

def is_video_mime(mime_type):
    """
    Return True if the given mime type is a common video format.
    """
    video_mimes = {
        "video/mp4",
        "video/quicktime",
        "video/x-matroska",
        "video/webm",
        "video/avi",
        "video/x-msvideo",
        "video/mpeg",
        "video/3gpp",
        "video/ogg"
    }
    return mime_type in video_mimes

def convert_bytes_to_wav_using_tempfile(input_bytes, mime_type):
    """
    Write bytes to a temp file and use ffmpeg to convert to wav.
    """
    suffix = guess_suffix_from_mime(mime_type)
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as temp_input, \
         tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_output:
        temp_input.write(input_bytes)
        temp_input.flush()
        cmd = [
            'ffmpeg', '-y', '-i', temp_input.name, '-vn',
            '-acodec', 'pcm_s16le',
            temp_output.name
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {proc.stderr.decode(errors='replace')}")
        temp_output.seek(0)
        wav_bytes = temp_output.read()
    return wav_bytes

def convert_bytes_to_wav_using_pipe(input_bytes):
    """
    Pipe streamable bytes to ffmpeg and get wav bytes from stdout.
    """
    cmd = [
        'ffmpeg', '-y', '-i', 'pipe:0', '-vn',
        '-acodec', 'pcm_s16le',
        '-f', 'wav', 'pipe:1'
    ]
    proc = subprocess.run(cmd, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not proc.stdout:
        raise RuntimeError(f"FFmpeg error: {proc.stderr.decode(errors='replace')}")
    return proc.stdout

def bytes2wavbytes(input_bytes):
    """
    Main function: Convert input bytes (audio/video) to WAV byte stream.
    Detects format, chooses approach, and robustly handles errors.
    """
    mime_type = detect_mime_type(input_bytes)
    try:
        if is_video_mime(mime_type) or not is_streamable_mime(mime_type):
            wav_bytes = convert_bytes_to_wav_using_tempfile(input_bytes, mime_type)
        else:
            wav_bytes = convert_bytes_to_wav_using_pipe(input_bytes)
        if not wav_bytes or len(wav_bytes) < 48:  # Minimal WAV header size
            raise RuntimeError("Output WAV data seems empty or corrupt.")
        return wav_bytes
    except Exception as e:
        raise RuntimeError(f"Failed to convert input to WAV: {e}")

if __name__ == "__main__":
    import sys
    # Example CLI usage: python bytes_to_wav.py input.file output.wav
    if len(sys.argv) != 3:
        print("Usage: python bytes_to_wav.py input.file output.wav")
        sys.exit(1)
    with open(sys.argv[1], "rb") as fin:
        input_bytes = fin.read()
    try:
        wav_bytes = bytes2wavbytes(input_bytes)
        with open(sys.argv[2], "wb") as fout:
            fout.write(wav_bytes)
        print(f"Conversion successful: {sys.argv[2]}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)
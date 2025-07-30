import pytest
from bytes2wavbytes import bytes2wavbytes
import wave

@pytest.fixture
def input_path():
    return "./test/example_input.mp4"

@pytest.fixture
def output_path():
    return "./test/example_output.wav"

def test_conversion_basic(input_path, output_path):
    """Test basic conversion from MP4 to WAV"""
    with open(input_path, "rb") as fin:
        input_bytes = fin.read()
        
    wav_bytes = bytes2wavbytes(input_bytes)
    
    with open(output_path, "wb") as fout:
        fout.write(wav_bytes)
    
    # Validate output is a valid WAV file
    with open(output_path, "rb") as f:
        wf = wave.open(f)
        assert wf.getnchannels() > 0
        assert wf.getsampwidth() > 0
        assert wf.getframerate() > 0

def test_librosa_compatibility(input_path):
    """Test basic conversion from MP4 to WAV"""
    import io
    import librosa
    with open(input_path, "rb") as fin:
        input_bytes = fin.read()
    
    wav_bytes = bytes2wavbytes(input_bytes)
    bytes_ = io.BytesIO(wav_bytes)
    y, sr = librosa.load(bytes_)

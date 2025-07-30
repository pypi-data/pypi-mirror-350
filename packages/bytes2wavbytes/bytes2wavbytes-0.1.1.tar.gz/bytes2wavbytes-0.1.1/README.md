# Bytes2wavbytes

## What is this?
- converts bytes to wav format
- as part of audio transcription pipeline

## Why is repo?
- audio loading library, such as librosa, soundfile, and audioread, does not support loading audio from video format, such as mp4, webm.
- high level audio transcription server (vLLM) does not support video (yet)
- this repo bridges the gap by converting any media format to WAV ( a lossless format)
- this repo is intended to be a component of a larger audio transcription pipeline, such as librosa and vLLM

## Convert bytes to wav format bytes

```python
from bytes2wavbytes import bytes2wavbytes

input_file = "example_input.mp4"
output_file = "example_output.wav"
with open(input_file, "rb") as fin:
    input_bytes = fin.read()

    wav_bytes = bytes2wavbytes(input_bytes)
    with open(output_file, "wb") as fout:
        fout.write(wav_bytes)
```

## Compatibility with librosa

```python
import io
import librosa
from bytes2wavbytes import bytes2wavbytes

input_file = "example_input.mp4"
with open(input_path, "rb") as fin:
    input_bytes = fin.read()

wav_bytes = bytes2wavbytes(input_bytes)
bytes_ = io.BytesIO(wav_bytes)
y, sr = librosa.load(bytes_)
```
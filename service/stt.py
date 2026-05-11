from datetime import datetime
import tempfile
from faster_whisper import WhisperModel
import os

# Load model
model = WhisperModel("base")
# model = WhisperModel("base", device="cuda", compute_type="float16")

def audio_file_to_text(audio_file: str):
    segments, info = model.transcribe(audio_file, beam_size=5)
    print(f"Detected language: {info.language}")
    print(f"Probability: {info.language_probability:.2f}\n")
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        # yield segment.start, segment.end, segment.text
        
def audio_stream_to_text(audio_bytes: bytes):
    start = datetime.now()
    print("✅1 Received audio bytes, processing...")
    temp_path = None
    print("✅2")
 
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False
        ) as temp_audio:
            print("✅3")
            temp_audio.write(audio_bytes)
            print("✅4")
            temp_path = temp_audio.name
            print("✅5")

        # File is now CLOSED here
        print("✅6")
        segments, info = model.transcribe(
            temp_path,
            beam_size=5
        )
        print("✅7")
        text = ""
        print("✅8")
        for segment in segments:
            text += segment.text + " "

        print("✅9")
        return text.strip()

    finally:
        print("✅10")
        # Cleanup
        if temp_path and os.path.exists(temp_path):
            print("✅11")
            os.remove(temp_path)

def _1audio_stream_to_text(audio_bytes: bytes):
    # Save bytes temporarily
    with tempfile.NamedTemporaryFile(suffix=".webm") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()

        segments, info = model.transcribe(
            temp_audio.name,
            beam_size=5
        )

        print("Language:", info.language)

        text = ""

        for segment in segments:
            text += segment.text + " "

        return text.strip()
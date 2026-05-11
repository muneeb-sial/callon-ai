import tempfile
from faster_whisper import WhisperModel

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

audio_file_to_text("./audio.webm")
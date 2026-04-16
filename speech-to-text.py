
from faster_whisper import WhisperModel

# Load model
model = WhisperModel("base", device="cuda", compute_type="float16")

def audio_file_to_text(audio_file: str):
    segments, info = model.transcribe(audio_file, beam_size=5)
    print(f"Detected language: {info.language}")
    print(f"Probability: {info.language_probability:.2f}\n")
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        # yield segment.start, segment.end, segment.text
        
def audio_stream_to_text(audio_stream):
    # popbabliy will feed to buffer
    pass

audio_file_to_text("./audio.mp3")
from datetime import datetime
from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(
    lang_code='a',
    # repo_id='kakaobrain/kokoro-tts-v1',
    # device="cuda"
    )

def text_to_audio_file(text:str):
    generator = pipeline(text, voice='af_heart')
    start = datetime.now()
    for i, (_, _, audio) in enumerate(generator):
        sf.write(f'output_{i}.wav', audio, 24000)
    end = datetime.now()
    print("Total time taken:", (end - start).total_seconds(), "seconds")


def text_to_audio_stream(text: str):
    generator = pipeline(text, voice='af_heart')
    for i, (gs, ps, audio) in enumerate(generator):
        yield gs, ps, audio
        
        
# text_to_audio_file("Hello, this is a test of the text-to-audio conversion. Hello, this is a test of the text-to-audio conversion. Hello, this is a test of the text-to-audio conversion.")
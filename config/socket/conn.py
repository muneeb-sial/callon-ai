from collections import defaultdict
from datetime import datetime
from fileinput import filename
from pathlib import Path
from scipy.io.wavfile import write
import socketio
from service.stt import audio_pcm_stream_to_text, audio_stream_to_text

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)
sio_app = socketio.ASGIApp(socketio_server=sio)

text_tokens = defaultdict(str)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    
@sio.on("audio:receive:tokens")
async def audio_receive_tokens(sid, data: str):
    text_tokens[sid] += data
    print(f"[token]: {data}")
    print(f"[text]: {text_tokens[sid]}")
    
@sio.on("audio:received")
async def audio_receive_tokens(sid):
    print(f"Generating output for text: {text_tokens[sid]}")


# @sio.on("audio:receive")
# async def audio_receive(sid, data):
#     chunk_count = 20
#     audio_buffers[sid].extend(data)

#     audio_chunk_counts[sid] += 1
#     audio_chunk_text[sid] += ""

#     # wait for 5 chunks
#     if audio_chunk_counts[sid] < chunk_count:
#         return

#     raw = bytes(audio_buffers[sid])

#     start = datetime.now()
#     text = audio_pcm_stream_to_text(raw)
#     end = datetime.now()
#     audio_chunk_text[sid] += f"{text} "
#     print(f"Processing: {end - start}, Text: {audio_chunk_text[sid]}")
#     # reset buffer
#     audio_buffers[sid].clear()
#     audio_chunk_counts[sid] = 0


@sio.on("audio:receive:all")
async def audio_receive_all(sid, data: bytes):
    start = datetime.now()
    text = audio_stream_to_text(data)
    end = datetime.now()
    print(f"Transcribed text: {text}")
    print(f"Processing time: {end - start}ms")
    await sio.emit("audio:receive:all:response", {"reply": f"{text}"}, to=sid)

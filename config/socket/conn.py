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
    # logger=True,
    # engineio_logger=True,
)
sio_app = socketio.ASGIApp(socketio_server=sio)

audio_dir = Path("audio")
audio_dir.mkdir(parents=True, exist_ok=True)

audio_buffers = defaultdict(bytearray)
audio_chunk_counts = defaultdict(int)
audio_chunk_text = defaultdict(str)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.on("audio:receive")
async def audio_receive(sid, data):
    chunk_count = 20
    audio_buffers[sid].extend(data)

    audio_chunk_counts[sid] += 1
    audio_chunk_text[sid] += ""

    # wait for 5 chunks
    if audio_chunk_counts[sid] < chunk_count:
        return

    raw = bytes(audio_buffers[sid])

    start = datetime.now()
    text = audio_pcm_stream_to_text(raw)
    end = datetime.now()
    audio_chunk_text[sid] += f"{text} "
    print(f"Processing: {end - start}, Text: {audio_chunk_text[sid]}")
    # reset buffer
    audio_buffers[sid].clear()
    audio_chunk_counts[sid] = 0


# @sio.on("audio:receive")
# async def audio_receive(sid, data):
#     audio_buffers[sid].extend(data)
#     raw = data
#     # raw = audio_buffers[sid]
#     pcm = np.frombuffer(raw, dtype=np.int16)
#     start = datetime.now()
#     filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

#     filepath = audio_dir / f"{filename}-debug.wav"
#     write(str(filepath), 16000, pcm)

#     text = audio_pcm_stream_to_text(data)
#     end = datetime.now()
#     print(f"Transcribed text: {text}")
#     print(f"Processing time: {end - start}ms")
#     # await sio.emit("audio:receive:all:response", {"reply": f"{text}"}, to=sid)


@sio.on("audio:receive:all")
async def audio_receive_all(sid, data: bytes):
    start = datetime.now()
    text = audio_stream_to_text(data)
    end = datetime.now()
    print(f"Transcribed text: {text}")
    print(f"Processing time: {end - start}ms")
    await sio.emit("audio:receive:all:response", {"reply": f"{text}"}, to=sid)

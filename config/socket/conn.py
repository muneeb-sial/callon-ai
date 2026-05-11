from datetime import datetime

import socketio
from service.stt import audio_stream_to_text

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    # logger=True,
    # engineio_logger=True,
)

sio_app = socketio.ASGIApp(socketio_server=sio)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.on("audio:receive")
async def audio_receive(sid, data: bytes):
    start = datetime.now()
    text = audio_stream_to_text(data)
    end = datetime.now()
    print(f"Transcribed text: {text}")
    print(f"Processing time: {end - start}ms")
    await sio.emit("audio:receive:all:response", {"reply": f"{text}"}, to=sid)


@sio.on("audio:receive:all")
async def audio_receive_all(sid, data: bytes):
    start = datetime.now()
    text = audio_stream_to_text(data)
    end = datetime.now()
    print(f"Transcribed text: {text}")
    print(f"Processing time: {end - start}ms")
    await sio.emit("audio:receive:all:response", {"reply": f"{text}"}, to=sid)

from collections import defaultdict
import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)
sio_app = socketio.ASGIApp(socketio_server=sio)

text_tokens = defaultdict(str)


@sio.event
async def connect(sid,_):
    print(f"Client connected: {sid}")
    
@sio.on("audio:receive:tokens")
async def audio_receive_tokens(sid, data: str):
    text_tokens[sid] += data
    print(f"[token]: {data}")
    print(f"[text]: {text_tokens[sid]}")
    
@sio.on("audio:received")
async def audio_receive_tokens(sid):
    print(f"Generating output for text: {text_tokens[sid]}")
    await sio.emit("audio:generate", text_tokens[sid])
    text_tokens[sid] = ""


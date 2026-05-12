from collections import defaultdict
import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)
sio_app = socketio.ASGIApp(socketio_server=sio)

text_tokens = defaultdict(str)

    
import config.socket.connect
import config.socket.audio_received
import config.socket.audio_receive_tokens


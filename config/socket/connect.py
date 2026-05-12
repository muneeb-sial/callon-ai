from config.socket.main import sio, text_tokens

@sio.event
async def connect(sid,_):
    print(f"Client connected: {sid}")
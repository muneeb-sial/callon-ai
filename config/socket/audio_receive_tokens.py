from config.socket.main import sio, text_tokens


@sio.on("audio:receive:tokens")
async def audio_receive_tokens(sid, data: str):
    text_tokens[sid] += data

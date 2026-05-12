from config.socket.main import sio, text_tokens

@sio.on("audio:received")
async def audio_received(sid):
    print(f"Generating output for text: {text_tokens[sid]}")
    await sio.emit("audio:generate", text_tokens[sid])
    text_tokens[sid] = ""
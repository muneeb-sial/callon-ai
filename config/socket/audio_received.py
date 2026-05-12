from config.socket.main import sio, text_tokens
from service.agent import AgentService

agent = AgentService()

@sio.on("audio:received")
async def audio_received(sid):
    response = await agent.run(text_tokens[sid])
    await sio.emit("audio:generate", response, to=sid)
    text_tokens[sid] = ""
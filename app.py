from fastapi import FastAPI, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from llm import llm_generate

app = FastAPI()

# Allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can set your React origin here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI Audio Stream Server is Running!"}

@app.get("/stream-audio")
def stream_audio():
    def iterfile():
        with open("output_1.wav", mode="rb") as file:
            chunk = file.read(1024)
            while chunk:
                yield chunk
                chunk = file.read(1024)
    return Response(iterfile(), media_type="audio/wav")


@app.websocket("/ws/audio")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()

    with open("audio.mp3", "rb") as f:
        LIMIT = 16
        chunk = f.read(1024 * LIMIT)
        while chunk:
            await websocket.send_bytes(chunk)  # send binary data
            await asyncio.sleep(0.1)         # simulate stream delay
            chunk = f.read(1024 * LIMIT)

    await websocket.close()
    
# @app.websocket("/ws/test")
# async def audio_stream(websocket: WebSocket):
#     await websocket.accept()
#     audio_data = llm_generate("What is the name of ther capital city of Japan")
#     chunk_size = 1024 * 32  
#     for i in range(0, len(audio_data), chunk_size):
#         await websocket.send_bytes(audio_data[i:i+chunk_size])
#         await asyncio.sleep(0.01)
#     await websocket.close()
    
@app.websocket("/ws/test")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    await llm_generate("What is the name of ther capital city of Japan",websocket)
    await websocket.close()

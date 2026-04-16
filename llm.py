from langchain.llms import LlamaCpp
from fastapi import WebSocket
import io
import asyncio
from kokoro import KPipeline
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
from tts import text_to_audio
import tempfile
import os

pipeline = KPipeline(lang_code='a')

from langchain.callbacks.base import BaseCallbackHandler

class CustomHandler(BaseCallbackHandler):
    def __init__(self,websocket:WebSocket):
         self.tokens = []
         self.audio = b""
         self.buffer = ""
         self.websocket = websocket
         self.loop = asyncio.get_event_loop()
         
    def on_llm_new_token(self, token: str, **kwargs):
        print(token + "", end="", flush=True)
        self.tokens.append(token)
        asyncio.run_coroutine_threadsafe(
            self.stream_token_audio("".join(self.tokens)), self.loop
        )
        
    def on_llm_end(self, response, **kwargs):
        # self.audio = text_to_audio(response.generations[0][0].text)
        print("response output:", response.generations[0][0].text)

    async def stream_token_audio(self, text):
        print("Sending audio for:", text)

        for i, (gen, phonemes, audio) in enumerate(text_to_audio(text)):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                import soundfile as sf
                sf.write(tmp.name, audio, 24000)
                tmp.seek(0)
                await self.websocket.send_bytes(tmp.read())
                os.remove(tmp.name)



llm = LlamaCpp(
    model_path="../../langchain/deepseek-llm-7b-chat.Q5_K_M.gguf",  # Path to GGUF model
    temperature=0.1,
    max_tokens=36,
    verbose=False,
    streaming=True,
    # callbacks=[CustomHandler()],
    n_gpu_layers=30
)

# def llm_generate(user_query: str,websocket:WebSocket) -> bytes:
#     handler = CustomHandler(websocket=websocket)
#     llm.callbacks = [handler]
#     llm(user_query)
#     return handler.audio


async def llm_generate(user_query: str, websocket: WebSocket):
    handler = CustomHandler(websocket=websocket)
    llm_instance = LlamaCpp(
        model_path="../../langchain/deepseek-llm-7b-chat.Q5_K_M.gguf",
        temperature=0.1,
        max_tokens=100,
        streaming=True,
        callbacks=[handler],
        n_gpu_layers=30,
        verbose=False
    )

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, lambda: llm_instance(user_query))
    
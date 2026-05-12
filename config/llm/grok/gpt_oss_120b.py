from langchain_groq import ChatGroq
from env import get_env

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=get_env("AI_API_KEY"),
    temperature=0,
    top_p=1,
    max_tokens=2048,
)

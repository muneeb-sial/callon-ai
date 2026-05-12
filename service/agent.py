from langchain.agents import create_agent
from config.llm.grok.gpt_oss_120b import llm
from config.llm.prompts.system_prompt import system_prompt


class AgentService:
    def __init__(
        self,
        llm=llm,
        tools: list = None,
        name: str = "CallonAgent",
    ):
        print("🚧 Initializing AgentService...")
        self.agent = create_agent(
            model=llm,
            tools=tools or [],
            name=name,
            system_prompt=system_prompt,
        )
        print("✅ AgentService initialized.")

    async def run(self, query: str) -> str:
        response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return response["messages"][-1].content

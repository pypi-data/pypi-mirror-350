import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent,
    Runner,
)
import set_agents_env as set_env
class StreamAgent:
    def __init__(self, agent: Agent, input: str):
        self.agent = agent
        self.input = input
        self.final_result = ""

    async def run(self):
        result = Runner.run_streamed(self.agent, input=self.input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta_text = event.data.delta
                self.final_result += delta_text
                print(delta_text, end="", flush=True)
                
        print("")   
        
        return self.final_result  

async def main():
    input = "你是谁？"
    # 设置环境
    set_env.set_env()
    model_name = "qwq-32b"

    agent = Agent(
        name="ZxAgent",
        instructions="",
        model=model_name,
    )
    
    stream_agent = StreamAgent(
        agent=agent,
        input=input,
    )
    await stream_agent.run()

if __name__ == "__main__":
    asyncio.run(main())
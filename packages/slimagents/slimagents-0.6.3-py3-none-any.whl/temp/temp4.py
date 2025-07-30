import inspect
from slimagents import Agent, ToolResult

agent = Agent()

ret = agent.run_sync("Hello, how are you?")

print(ret)
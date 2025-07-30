import inspect
from slimagents import Agent, ToolResult

agent = Agent()

obj = object()

ret = inspect.iscoroutinefunction(obj.__call__)

print(ret)
from pprint import pprint
from slimagents.core import Agent, ToolResult

calc_agent = Agent(
    name="Calculator",
    instructions="You are a human calculator.",
    tools=[],
    model="gpt-4o-mini",
    response_format=float,
)

def calculator():
    """
    Transfer the question to the calculator agent. Always use this tool when the user asks a question that can be answered by the calculator.
    """
    return ToolResult(agent=calc_agent, is_final_answer=True)

master = Agent(
    name="Master",
    instructions="You are a master agent that can handle all tasks.",
    tools=[calculator],
    model="gpt-4o-mini",
)

memory = []

value = master.apply("What is 2 + 2?", memory=memory)

pprint(memory)
print(value)


from slimagents.core import Agent, ToolResult


def calculator(expression: str) -> float:
    """
    Calculate the result of the expression.
    """
    value = eval(expression)
    return ToolResult(value=value)

calc_agent = Agent(
    name="Calculator",
    instructions="You are not good at math, but you have a calculator.",
    tools=[calculator],
    model="gpt-4o-mini",
)

memory = []

calc_agent.apply("What is 2 + 2?", memory=memory)

print(memory)

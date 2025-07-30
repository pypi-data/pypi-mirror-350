import logging
from slimagents import Agent, run_demo_loop
from slimagents.core import Response, ToolResult

logging.basicConfig(level=logging.INFO)

def calculator(input: str) -> str:
    """
    Calculates mathematical expressions.

    Args:
        input(str): A mathematical expression to calculate.

    Returns:
        float: The result of the mathematical expression.
    """
    return ToolResult(value=eval(input), is_final_answer=True)

agent = Agent(model="gpt-4o-mini", tools=[calculator], instructions="You always use the calculator tool to calculate mathematical expressions.")
agent.logger.setLevel(logging.INFO)

run_demo_loop(agent)
# run_demo_loop(agent, stream=True)

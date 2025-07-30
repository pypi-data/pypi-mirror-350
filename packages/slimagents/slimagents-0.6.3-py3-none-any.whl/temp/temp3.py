from slimagents import Agent

def python_evaluator(expression: str) -> str:
    """Evaluate a Python expression. Always use this tool for calculations and other complex operations."""
    print(f"--- Evaluating {expression}")
    # Obviously not secure, but for the sake of this example we'll just eval the expression.
    ret = str(eval(expression))
    print(f"--> {ret}")
    return ret

agent = Agent(
    instructions="You are a helpful assistant. When given a task you always try to solve it by using tools, never rely on your own knowledge.",
    tools=[python_evaluator],
)

prompt = "How many R's are in the word 'STRAWBERRY'?"
print(f"User: {prompt}")
response = agent.run_sync(prompt)
print(f"Agent: {response.value}")
print(response.memory_delta)
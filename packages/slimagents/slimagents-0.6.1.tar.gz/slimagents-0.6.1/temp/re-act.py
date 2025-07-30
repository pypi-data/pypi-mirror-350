import asyncio
from datetime import datetime
import logging
import random
from slimagents import Agent, ToolResult
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def add(a: float, b: float) -> float:
    """Add two numbers."""
    print(f"Adding {a} and {b}")
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    print(f"Subtracting {a} and {b}")
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    print(f"Multiplying {a} and {b}")
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    print(f"Dividing {a} and {b}")
    return a / b

def thought(description: str, final_answer: str):
    """Always register your thought before calling another tool.
    Arguments:
        description (str): The description of your thought.
        final_answer (str): The final answer to the user's question. Leave empty if you have not reached a solution yet.
    """
    print(f"\n### Thought: {description}")
    if final_answer:
        return ToolResult(is_final_answer=final_answer)
    return "OK"

def thought(description: str, final_answer: str):
    """This is a special tool call that is used to register your reasoning for the next step, or why you have reached a solution.
    Arguments:
        description (str): The description of your thought. Describe which tool calls you will make next, or why you have reached a solution.
        final_answer (str): The final answer to the user's question. Leave empty if you have not reached a solution yet.
    """
    print(f"\n### Thought: {description}")
    if final_answer:
        print("-->", "Final answer reached:", final_answer)
        return ToolResult(value=final_answer, is_final_answer=True)
    return "OK"

def final_answer(answer: str):
    """Register your final answer."""
    print(f"--- Final answer: {answer}")
    return ToolResult(is_final_answer=answer)

def calculator(expression: str) -> float:
    """Calculate the result of an expression. IMPORTANT: Always use this tool for calculations, never try to do it yourself."""
    print(f"--- Calculating {expression}")  
    ret = eval(expression)
    print("-->", str(ret))
    return ret

def show_on_screen(text: str):
    """Show text on the screen."""
    print(f"--- Showing on screen: {text}")
    ret = "The message was shown on the screen."
    print("-->", ret)
    return ret

def get_profit_and_loss_report(month: int, year: int) -> str:
    """Get the profit and loss report for a given month and year.
    Arguments:
        month (int): The month to get the profit and loss report for. 1 - 12.
        year (int): The year to get the profit and loss report for.
    """
    print(f"--- Getting profit and loss report for {month}/{year}")
    ret = """
    | Account               | Amount  |
    |-----------------------|---------|
    | Sales                 | 1000    |
    | Cost of goods sold    | 500     |
    | Other expenses        | 300     |
    """
    print("-->", ret)
    return ret

def get_weather(location: str) -> str:
    """Get the weather for a given location."""
    print(f"--- Getting weather for {location}")
    temperature = random.randint(10, 30)
    weather = random.choice(["sunny", "cloudy", "rainy", "snowy"])
    ret = f"It's {weather} and {temperature} degrees."
    print("-->", ret)
    return ret

def get_current_date(today: str) -> str:
    """Get the current date. Always use "today" as the input."""
    print("--- Getting current date")
    ret = datetime.now().strftime("%Y-%m-%d")
    print("-->", ret)
    return ret

instructions = """
You are a helpful assistant. Your task is to come up with the next step to answer the question. 
You have access to a set of tools, and you will *always* use the tools to solve the problem. 
For each request, you will generate AT LEAST two tool calls:
1. ALWAYS generate a tool call to register your reasoning for the next step, or why you have reached a solution.
2. One or more tool calls to actually solve the problem, if you have not reached a solution yet.
3. Or a tool call to register your final answer, if you have reached a solution. ALWAYS generate this tool call before the end of the request.

IMPORTANT: In some cases the result of one tool call will be the input for the another tool call. 
In that case, only generate the first tool call. In other words, only generate tool calls that are 
independent of each other and that can be executed in any order.

REMEMBER: Always use the tool calls "thought" and "final_answer" when you have reached a solution.
"""

instructions = """
You are a helpful assistant. Your task is to come up with THE NEXT STEP to answer the user's question. 
You have access to a set of tools, and you will use the tools to solve the next step, if possible. 

In some cases the result of one or more tool calls will be the input for other tool calls. 
In that case, only generate the first tool calls. In other words, only generate tool calls that are 
independent of each other and that can be executed in any order.

If no appropriate tool call is available you can answer the question yourself from your knowledge.
IMPORTANT: Never make up any answers. If you don't know the answer, say so.
"""

instructions = """
You are a helpful assistant. Your task is to come up with THE NEXT STEP to answer the user's question. 
You have access to a set of tools, and you will use the tools to solve the next step, if possible. 

In some cases the result of one or more tool calls will be the input for other tool calls. 
In that case, only generate the first tool calls. In other words, only generate tool calls that are 
independent of each other and that can be executed in any order.

If no appropriate tool call is available you can answer the question yourself from your knowledge.
IMPORTANT: Never make up any answers. If you don't know the answer, say so.
"""

instructions = """
You are a helpful assistant. Your task is to come up with the next step to answer the incoming question. 
You have access to a set of tools, and you will always use the tools to generate the answer, if possible. 

You will ALWAYS start by generating a tool call to "thought". This is a special tool call that is used to register your reasoning for the next step, or the final answer.

You may also generate one or more tool calls to actually solve the problem, if you have not reached a solution yet.

IMPORTANT: Remember to always include the "thought" tool call"""

async def main():
    agent = Agent(
        instructions=instructions,
        # tools=[thought, final_answer, add, subtract, multiply, divide],
        # tools=[thought, final_answer, calculator, show_on_screen, get_profit_and_loss_report, get_weather],
        tools=[thought, calculator, show_on_screen, get_profit_and_loss_report, get_weather, get_current_date],
        # model="gemini/gemini-1.5-flash-002",
        model="gemini/gemini-2.0-flash-exp",
        parallel_tool_calls=None,
        # response_format=MyResult,
        # extra_llm_params={"drop_params": True},
    )

    agent.logger.setLevel(logging.DEBUG)

    # response = await agent.run("What is 3 + 3 * 4 - 2 / 2? Show the result on the screen.")
    response = await agent.run("What was the profit last month? Show the result on the screen.")
    # response = await agent.run("What is the temperature difference betweeen Oslo and Stockholm? Show the result on the screen.")
    print(response.value)


if __name__ == "__main__":
    asyncio.run(main())

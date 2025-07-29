import asyncio
from datetime import datetime
import logging
import random
from slimagents import Agent, ToolResult
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

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

def thought(description: str):
    """Describe your thoughts. This is a special tool that you will always use first."""
    print(f"\n### Thought: {description}")
    return "Thought registered"

def final_answer(answer: str):
    """Register your final answer. Never use this tool in combination with any calls to normal tools."""
    print(f"--- Final answer: {answer}")
    return ToolResult(value=answer, is_final_answer=True)



instructions = """
# INSTRUCTIONS
You are a helpful assistant. You have access to a set of tools, and you will always use the tools to generate the answer, if possible. 

# TOOLS

Two of the tools are special:
- "thought": Describe your thought.
- "final_answer": Provide the final answer to the user's question.
These tools will be referred to as "special tools".

The other tools are tools that can actually be used to solve the problem. These tools will be referred to as "normal tools".

# RESPONSE PROTOCOL

## WITH NORMAL TOOL CALLS
Use this protocol when you will use normal tools to solve the problem.
- Always start by generating a tool call to the "thought" tool. Describe which tool calls you will make and why.
- Then generate one or more tool calls to actually solve the problem, if you have not reached a solution yet.

IMPORTANT
- In this scenario, you will never generate a tool call to the "final_answer" tool.
- Only generate tool calls that are independent, i.e. they do not depend on the results of other tool calls that have not been executed yet.

## WITH SPECIAL TOOL CALLS
Use this protocol when you have reached a solution based on normal tool calls, or if you can answer the user's question directly.
- Always start by generating a tool call to the "thought" tool. Describe why you think you have reached a solution and how you will formulate the final answer.
- Then generate a tool call to the "final_answer" tool containing the final answer.

IMPORTANT
- In this scenario, you will never generate a tool call to any normal tool.
- The user does not have access to your thought process and the results of the tool calls. Take this into account when generating the final answer. Make sure to include all relevant information.
"""

async def main():
    agent = Agent(
        instructions=instructions,
        # tools=[thought, final_answer, add, subtract, multiply, divide],
        # tools=[thought, final_answer, calculator, show_on_screen, get_profit_and_loss_report, get_weather],
        tools=[thought, final_answer, calculator, show_on_screen, get_profit_and_loss_report, get_weather, get_current_date],
        tool_choice="required",
        # model="gemini/gemini-1.5-flash-002",
        # model="gemini/gemini-2.0-flash-exp",
        # parallel_tool_calls=None,
        # response_format=MyResult,
        # extra_llm_params={"drop_params": True},
    )

    agent.logger.setLevel(logging.DEBUG)

    # response = await agent.run("What is 3 + 3 * 4 - 2 / 2? Show the result on the screen.")
    # response = await agent.run("What was the profit last month? Show the result on the screen.")
    response = await agent.run("What is the temperature difference betweeen Oslo and Stockholm? Show the result on the screen.")
    print(response.value)


if __name__ == "__main__":
    asyncio.run(main())

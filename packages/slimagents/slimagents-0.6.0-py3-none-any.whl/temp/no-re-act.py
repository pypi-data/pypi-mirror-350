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
    print("-->", str(ret), "\n")
    return ret

def show_on_screen(text: str) -> str:
    """Show text on the screen. The returned value describes if the task was successful or not."""
    print(f"--- Showing on screen: {text}")
    ret = random.choice(["success", "failure"])
    print("-->", ret, "\n")
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
    print("-->", ret, "\n")
    return ret

def get_weather(location: str, year: int, month: int, day: int) -> str:
    """Get the weather for a given location on a given date."""
    print(f"--- Getting weather for {location} on {year:04d}-{month:02d}-{day:02d}")
    temperature = random.randint(10, 30)
    weather = random.choice(["sunny", "cloudy", "rainy", "snowy"])
    ret = f"It's {weather} and {temperature} degrees."
    print("-->", ret, "\n")
    return ret

def get_current_date(today: str) -> str:
    """Get the current date. Always use "today" as the input."""
    # Gemini does not work with no argument tool calls...
    print("--- Getting current date")
    ret = datetime.now().strftime("%Y-%m-%d")
    print("-->", ret, "\n")
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
# MISSION
You are a helpful assistant who excels at planning and executing tasks by using tools.

# INSTRUCTIONS
- Always use the provided tools to solve the problem, if possible. 
- If you cannot use the tools to solve the problem, then you will have to use your own knowledge to solve the problem.
- Never make up answers. If you don't know the answer, then you should say so.
- Never generate tool calls that depend on the results of other tool calls that have not been executed yet.
- If you generate several tool calls it is important that they are independent, i.e. they can be executed in any order.

# IMPORTANT
- The user does not have access to your thought process and the results of the tool calls. Take this into account when generating the final answer.
"""

class MyAgent(Agent):
    def _before_chat_completion(self) -> None:
        print("### New iteration\n")

agent = MyAgent(
    instructions=instructions,
    # tools=[thought, final_answer, add, subtract, multiply, divide],
    # tools=[thought, final_answer, calculator, show_on_screen, get_profit_and_loss_report, get_weather],
    tools=[calculator, show_on_screen, get_profit_and_loss_report, get_weather, get_current_date],
    # tool_choice="required",
    # model="gemini/gemini-1.5-flash-002",
    # model="gemini/gemini-2.0-flash-exp",
    parallel_tool_calls=None,
    # response_format=MyResult,
    # extra_llm_params={"drop_params": True},
)


agent.logger.setLevel(logging.DEBUG)

# query = "What is 3 + 3 * 4 - 2 / 2? Show the result on the screen."
# response = await agent.run("What is 3 + 3 * 4 - 2 / 2? Show the result on the screen.")

# query = "What was the profit last month? Show the result on the screen."
# print("QUERY:", query, "\n")
# response = agent.run_sync(query)
# print("ANSWER:", response.value, "\n")

query = "What is the temperature difference betweeen Oslo and Stockholm? Show the result on the screen."
print("QUERY:", query, "\n")
response = agent.run_sync(query)
print("ANSWER:", response.value, "\n")

# query = "Calculate the average temperature difference between Oslo and Stockholm the last 4 days."
# print("QUERY:", query, "\n")
# response = agent.run_sync(query)
# print("ANSWER:", response.value, "\n")


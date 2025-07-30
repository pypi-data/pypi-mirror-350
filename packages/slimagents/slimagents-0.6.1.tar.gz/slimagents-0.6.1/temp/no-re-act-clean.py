import asyncio
from datetime import datetime
import logging
import random

import aiohttp
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from slimagents import Agent, ToolResult
from dotenv import load_dotenv
from pydantic import BaseModel
from slimagents.repl import run_demo_loop

load_dotenv()

def calculator(expression: str) -> float:
    """Calculate the result of an expression. IMPORTANT: Always use this tool for calculations, never try to do it yourself."""
    print(f"--- Calculating {expression}")  
    ret = eval(expression)
    print("-->", str(ret), "\n")
    return ret

def python_evaluator(expression: str) -> str:
    """Evaluate a Python expression. Use this tool for calculations and other complex operations."""
    print(f"--- Evaluating {expression}")  
    ret = str(eval(expression))
    print("-->", str(ret), "\n")
    return ret

def show_on_screen(text: str) -> str:
    """Show text on the screen. This tool is used to display important messages. The returned value describes if the operation was successful or not."""
    print(f"--- Showing on screen: {text}")
    ret = random.choice(["success", "failure"])
    print("-->", ret, "\n")
    # return "Unable to show on screen. Screen is broken."
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

async def get_web_page_content_as_markdown(url: str) -> str:
    """Get the content of a URL formatted as markdown."""
    print(f"Getting content of {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text and clean it up
            text = soup.get_text()
            # Break into lines and remove leading/trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = ' '.join(chunk for chunk in chunks if chunk)

            print(f"Got content of {url}")
            
            return text
        
async def duckduckgo_search(query: str) -> list[tuple[str, str]]:
    """Search DuckDuckGo for a query and return the search results as list of (url, description) pairs."""
    base_url = f"https://duckduckgo.com/html/?q={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract search results
            results = []
            for result in soup.find_all('div', class_='result'):
                title = result.find('a', class_='result__a')
                url = title.get('href') if title else None
                description = result.find('a', class_='result__snippet')
                
                if title and url and description:
                    results.append(("https://"+url, description.text.strip()))
            
            return results[:5]  # Return top 5 results


instructions = """
# MISSION
You are a helpful assistant who excels at planning and executing tasks by using tools.

# INSTRUCTIONS
- Always use the provided tools to solve the problem, if possible. In particular, always use the python_evaluator tool if it is possible to use it.
- If you cannot use the tools to solve the problem, then you will have to use your own knowledge to solve the problem.
- Never make up answers. If you don't know the answer, then you should say so.
- Never generate tool calls that depend on the results of other tool calls that have not been executed yet.
- If you generate several tool calls it is important that they are independent, i.e. that they can be executed in any order.

# IMPORTANT
- The user does not have access to your thought process and the results of the tool calls. Take this into account when generating the final answer.
"""

python_function_writer_instructions = """
# IDENTITY
You are a helpful assistant who excels at writing Python code.

# MISSION
You will be given a problem to solve and you will have to write a Python function that solves the problem.

# INSTRUCTIONS
- You always try to generalize the function as much as possible. Create suitable arguments for the function.
- You always try to make the function as simple as possible.
"""

class MyAgent(Agent):
    def _before_chat_completion(self) -> None:
        print("### New iteration\n")

    def python_evaluator(self, expression: str) -> str:
        function_writer_agent = Agent(
            instructions="You are a helpful assistant who excels at writing Python code.",
            # tools=[],
        )
        function_writer_agent.run_sync(expression)

agent = Agent(
    instructions=instructions,
    tools=[
        python_evaluator, 
        calculator, 
        # show_on_screen, 
        get_profit_and_loss_report, 
        get_weather, 
        get_current_date, 
        duckduckgo_search, 
        get_web_page_content_as_markdown,
    ],
    model="o3-mini"
)


query = "What is the temperature difference between Oslo and Stockholm? Show the result on the screen."
query = "How many R's are in the word 'STRAWBERRY'?"

# print("QUERY:", query, "\n")
# response = agent.run_sync(query)
# print("ANSWER:", response.value, "\n")

run_demo_loop(agent, log_level=logging.INFO)



# query = "What is 3 + 3 * 4 - 2 / 2? Show the result on the screen."
# response = await agent.run("What is 3 + 3 * 4 - 2 / 2? Show the result on the screen.")

# query = "What was the profit last month? Show the result on the screen."
# print("QUERY:", query, "\n")
# response = agent.run_sync(query)
# print("ANSWER:", response.value, "\n")

# query = "Calculate the average temperature difference between Oslo and Stockholm the last 4 days."
# print("QUERY:", query, "\n")
# response = agent.run_sync(query)
# print("ANSWER:", response.value, "\n")


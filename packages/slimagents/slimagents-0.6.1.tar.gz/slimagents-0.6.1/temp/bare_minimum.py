import logging
import aiohttp
from slimagents import Agent
from dotenv import load_dotenv
import asyncio
from markdownify import markdownify as md
from bs4 import BeautifulSoup

load_dotenv()

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

async def get_url_(url: str, max_chars: int = None) -> str:
    """Get the content of a URL. Use max_chars to limit the response if needed."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()[:max_chars] if max_chars else await response.text()

async def get_url(url: str) -> str:
    """Get the content of a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

            return (await response.text())[:10000]

async def get_web_page_content_as_text(url: str) -> str:
    """Get the content of a URL as text, using BeautifulSoup to extract readable text."""
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

def register_thoughts(thoughts: str):
    """Register your thoughts. Always use this tool when you are using another tool."""
    return "Thoughts registered"
        

agent = Agent(
    name="Agent",
    instructions="You are a helpful agent. You will always use the tools to solve the problem, if possible.",
    tools=[add, subtract, multiply, divide],
)

agent.logger.setLevel(logging.DEBUG)

#     agent = Agent(
#         name="Agent",
#         instructions="""You are a web research agent. You will always answer the question based on information found online using the provided tools.
# You will first analyze the question and determine what tools you need to use to answer the question. You will then use the register_thoughts tool to register your thoughts that describe what you are doing and why you are using the tool.
# You will keep calling tools until you have answered the question completely or you have no more tools to use.
# """,
#         functions=[register_thoughts, add, subtract, multiply, divide, get_web_page_content_as_text, duckduckgo_search],
#     )

# messages = [{"role": "user", "content": "Hva er hovedoppslaget på https://www.nrk.no, https://www.vg.no, https://www.aftenposten.no?"}]
# messages = [{"role": "user", "content": "Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?"}]
response = agent.run_sync("What is 3 + 3 * 4 - 2 / 2?")
print(response.value)

async def test():
    results = await duckduckgo_search("How fast can a human run?")
    print(results)

asyncio.run(test())
import json
import asyncio
import logging

from slimagents import Response

from slimagents.config import logger
from slimagents.core import Agent


async def process_and_print_streaming_response(response):
    content = ""
    last_sender = ""

    async for chunk in response:
        if isinstance(chunk, Response):
            return chunk
        
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # End of response message
            content = ""


def pretty_print_messages(messages) -> None:
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")


def enable_logging(log_level: int = logging.ERROR) -> None:
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(log_level)


async def run_demo_loop_async(agent: Agent, stream=False, log_level: int = None) -> None:
    if log_level is not None:
        enable_logging(log_level)

    print("Starting SlimAgents CLI 🪶")

    memory = []

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        response = await agent.run(user_input, stream=stream, memory=memory, stream_response=True, stream_delimiters=True, stream_tokens=False, stream_tool_calls=True)
        if stream:
            response = await process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.memory_delta)

        agent = response.agent


def run_demo_loop(agent, stream=False, log_level: int = None):
    """Synchronous wrapper for run_demo_loop_async"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(run_demo_loop_async(agent, stream, log_level))

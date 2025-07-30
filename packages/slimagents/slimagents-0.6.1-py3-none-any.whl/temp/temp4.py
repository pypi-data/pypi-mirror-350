from collections import defaultdict
import copy
from textwrap import dedent
import litellm
from litellm.caching.caching import Cache

litellm.cache = Cache(type="disk", disk_cache_dir="./test_cache")

def merge_fields(target, source):
    for key, value in source.items():
        if isinstance(value, str):
            target[key] += value
        elif value is not None and isinstance(value, dict):
            merge_fields(target[key], value)

def merge_chunk_(final_response: dict, delta: dict) -> None:
    delta.pop("role", None)
    merge_fields(final_response, delta)

    tool_calls = delta.get("tool_calls")
    if tool_calls and len(tool_calls) > 0:
        tool_call = tool_calls[0]
        index = tool_call.pop("index")
        type_ = tool_call.pop("type", None)
        final_tool_call = final_response["tool_calls"][index]
        merge_fields(final_tool_call, tool_call)
        if type_ and not final_tool_call.get("type"):
            # type = "function" is always returned by LiteLLM in the delta. Bug?
            # This ensures that the type is only set once.
            final_tool_call["type"] = type_

def merge_chunk(final_response: dict, delta: dict) -> None:
    delta.pop("role", None)
    merge_fields(final_response, delta)

    tool_calls = delta.get("tool_calls")
    if tool_calls:
        for tool_call in tool_calls:
            index = tool_call.pop("index")
            # type_ = tool_call.pop("type", None)
            final_tool_call = final_response["tool_calls"][index]
            merge_fields(final_tool_call, tool_call)
            # if type_ and not final_tool_call.get("type"):
            #     # type = "function" is always returned by LiteLLM in the delta. Bug?
            #     # This ensures that the type is only set once.
            #     final_tool_call["type"] = type_

completion_params = {
    "stream": True,
    "caching": True,
    "temperature": 0.0,
    "model": "gpt-4.1",
    "tools": [
        {
            'type': 'function', 
            'function': {
                'name': 'calculator', 
                'description': 
                'Calculate the result of the expression.', 
                'parameters': {
                    'type': 'object', 
                    'properties': {
                        'expression': {'type': 'string'}
                    }, 
                    'required': ['expression']
                }
            }
        }
    ],
    "messages": [
        {
            "role": "system",
            "content": dedent(
                """\
                # RULES YOU MUST FOLLOW
                - You always use the calculator to answer questions. 
                - You always generate two calculator tool calls in your response.
                - You answer with a comma separated list of numbers.
                """
            ),
        },
        {
            "role": "user",
            "content": "What is 2 + 2 and what is 4 * 4?"
        },
    ]
}

message_template = {
    "content": "",
    "role": "assistant",
    "function_call": None,
    "tool_calls": defaultdict(
        lambda: {
            "function": {"arguments": "", "name": ""},
            "id": "",
            "type": "",
        }
    ),
}

async def run():
    completion = await litellm.acompletion(**completion_params)
    message = copy.deepcopy(message_template)
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        print("DELTA:")
        print(delta)
        print("---")
        delta.pop("role", None)
        merge_chunk(message, delta)

    result1 = str(message)
    print("RESULT1:")
    print(result1)
    print("---")

    print("================================================")

    completion = await litellm.acompletion(**completion_params)
    message = copy.deepcopy(message_template)
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        print("DELTA:")
        print(delta)
        print("---")
        delta.pop("role", None)
        merge_chunk(message, delta)

    result2 = str(message)
    print("RESULT2:")
    print(result2)
    print("---")
    assert result1 == result2

import asyncio
asyncio.run(run())

"""
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x12a9f1c60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_o7S5j3ovMqFAQqJKk74t58mX', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_ev7jYDWHG7KOIrHch6PhDWCz', 'type': 'function'}})}
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x12a9f1c60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_2kQY4KtxmThZFVT5C1fXYlGi', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_6eq6HnTs5ivrwfy2zVpV3sTj', 'type': 'function'}})}
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x119121c60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_o7S5j3ovMqFAQqJKk74t58mX', 'type': 'function'}})}


{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x117506b60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_CJKTvRnUruMByt5ceQ2xVEbJ', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_a0iKQjJC2hbrbs7e3IEjXWMS', 'type': 'function'}})}
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x117506b60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_HWKbzcVLXx4pkAoSGr6Ers2p', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_5bBE8QgrswsVk5S2OLDl4x3t', 'type': 'function'}})}
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x107aeab60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_CJKTvRnUruMByt5ceQ2xVEbJ', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_a0iKQjJC2hbrbs7e3IEjXWMS', 'type': 'function'}})}
{'content': '', 'role': 'assistant', 'function_call': None, 'tool_calls': defaultdict(<function <lambda> at 0x123d12b60>, {0: {'function': {'arguments': '{"expression": "2 + 2"}', 'name': 'calculator'}, 'id': 'call_CJKTvRnUruMByt5ceQ2xVEbJ', 'type': 'function'}, 1: {'function': {'arguments': '{"expression": "4 * 4"}', 'name': 'calculator'}, 'id': 'call_a0iKQjJC2hbrbs7e3IEjXWMS', 'type': 'function'}})}
"""

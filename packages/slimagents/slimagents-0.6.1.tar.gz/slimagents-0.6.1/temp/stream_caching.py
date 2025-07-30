import litellm
from litellm.caching.caching import Cache

# litellm.cache = Cache(type="disk", disk_cache_dir="./test_cache")
litellm.cache = Cache()

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
            "role": "user",
            "content": "Count to 10"
        },
    ]
    # "messages": [
    #     {
    #         "role": "system",
    #         "content": "You always use the calculator to answer questions."
    #     },
    #     {
    #         "role": "user",
    #         "content": "What is 2 + 2?"
    #     },
    # ]
}

async def run():
    completion = await litellm.acompletion(**completion_params)
    deltas1 = []
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas1.append(str(delta))
        print(f"DELTA: {delta}")
        print("---")

    print("================================================")

    completion = await litellm.acompletion(**completion_params)
    deltas2 = []
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas2.append(str(delta))
        print(f"DELTA: {delta}")
        print("---")

    assert deltas1 == deltas2

def run_sync():
    completion = litellm.completion(**completion_params)
    deltas1 = []
    for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas1.append(str(delta))
        print(f"DELTA: {delta}")
        print("---")

    print("================================================")

    completion = litellm.completion(**completion_params)
    deltas2 = []
    for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas2.append(str(delta))
        print(f"DELTA: {delta}")
        print("---")

    assert deltas1 == deltas2

run_sync()

# import asyncio
# asyncio.run(run())

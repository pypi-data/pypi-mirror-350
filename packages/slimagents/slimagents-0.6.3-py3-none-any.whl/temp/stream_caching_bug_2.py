import asyncio
import litellm
from litellm.caching.caching import Cache

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
                'description': 'Calculate the result of the expression.', 
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
            "content": "What is 2 + 2? Use the calculator."
        },
    ]
}

async def run():
    completion = await litellm.acompletion(**completion_params)
    deltas1 = []
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas1.append(str(delta))
        print(f"DELTA: {delta}")

    print("================================================")

    completion = await litellm.acompletion(**completion_params)
    deltas2 = []
    async for chunk in completion:
        delta = chunk.choices[0].delta.model_dump()
        deltas2.append(str(delta))
        print(f"DELTA: {delta}")

    assert deltas1 == deltas2

asyncio.run(run())
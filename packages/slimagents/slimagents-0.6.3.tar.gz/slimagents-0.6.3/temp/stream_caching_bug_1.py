import litellm
from litellm.caching.caching import Cache

litellm.cache = Cache()

completion_params = {
    "stream": True,
    "caching": True,
    "temperature": 0.0,
    "model": "gpt-4.1",
    "messages": [
        {
            "role": "user",
            "content": "Count to 10"
        },
    ]
}

completion = litellm.completion(**completion_params)
deltas1 = []
for chunk in completion:
    delta = chunk.choices[0].delta.model_dump()
    deltas1.append(str(delta))
    print(f"DELTA: {delta}")

print("================================================")

completion = litellm.completion(**completion_params)
deltas2 = []
for chunk in completion:
    delta = chunk.choices[0].delta.model_dump()
    deltas2.append(str(delta))
    print(f"DELTA: {delta}")

assert deltas1 == deltas2

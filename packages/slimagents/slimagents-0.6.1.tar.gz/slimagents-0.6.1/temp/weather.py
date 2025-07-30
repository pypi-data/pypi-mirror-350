# !pip install python-weather

from slimagents.core import Agent
import python_weather

class WeatherAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful assistant who answers questions about the weather.",
            tools=[self.get_temperature],
        )

    async def get_temperature(self, location: str) -> float:
        """Get the current temperature in a given location, in degrees Celsius."""
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            print(f"--- Getting temperature for {location}")
            weather = await client.get(location)
            print(f"--> Temperature in {location}: {weather.temperature}")
            return weather.temperature

agent = WeatherAgent()
prompt = "What is the temperature difference between London and Paris?"
print(f"User: {prompt}")
response = agent.run_sync(prompt)
print(f"Agent: {response.value}")

from slimagents import Agent
from slimagents.repl import run_demo_loop

class StrictAgent(Agent):
    def __init__(self, max_responses: int):
        super().__init__(
            tools=[self.update_responses_left],
        )
        self._answers_left = max_responses + 1

    @property
    def instructions(self) -> str:
        if self._answers_left > 0:
            return f"""
You are a helpful assistant. 
You currently have {self._answers_left} responses left.
ALWAYS call the `update_responses_left` tool before you respond."""
        else:
            return "You always answer 'I can't answer that.'."

    def update_responses_left(self):
        """IMPORTANT! You ALWAYS call this tool before you respond, no matter what the user says."""
        self._answers_left -= 1
        return "Good! You may now answer the question."

agent = StrictAgent(2)
run_demo_loop(agent)

from thinagents import Agent

Agent(
    name="test",
    model="gpt-3.5-turbo",
    api_key="test",
    api_base="https://api.openai.com/v1",
    api_version="v1",
).run("Hello world")
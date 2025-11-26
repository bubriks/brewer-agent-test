from pathlib import Path

from hopsworks_brewer.framework import Agent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.personality import personality

def build_agent():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.join(personality, Agent.read(location / "instructions.md")),
        llm=Registry().get(),
    )

agent = build_agent()

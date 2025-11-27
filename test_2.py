from hopsworks_brewer.framework import Agent
from hopsworks_brewer.models import Registry

def test_2():
    return Agent(
        name=Agent.initializer_name(),
        description="aaaa",
        system_prompt="bbbb",
        llm=Registry().get(),
    )

def add_to_team(team):
    team.add_agent_initializer(test_2)
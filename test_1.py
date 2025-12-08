from hopsworks_brewer.framework import Agent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.framework import AgentProvider

def test_1():
    brewer = AgentProvider(repo='https://github.com/bubriks/brewer-agent-test.git')
    return Agent(
        name=Agent.initializer_name(),
        description="aaaa",
        system_prompt="bbbb",
        llm=Registry().get(),
        agents=["test_2", brewer / "talker"]
    )

def add_to_team(team):
    team.add_agent_initializer(test_1)

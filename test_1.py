from hopsworks_brewer.framework import Agent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.framework import Team

def test_1():
    brewer_team = Team(repo='https://github.com/logicalclocks/brewer.git') # What about this? =) Could work, i guess less changes to existing code (everything is a team, just we can use agents from different teams by specifying repo)
    return Agent(
        name=Agent.initializer_name(),
        description="aaaa",
        system_prompt="bbbb",
        llm=Registry().get(),
        agents=["test_2", "sum", brewer_team / "talker"]
    )

def add_to_team(team):
    team.add_agent_initializer(test_1)

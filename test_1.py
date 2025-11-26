from hopsworks_brewer.framework import Agent, AgentProvider

provider = AgentProvider(repo='https://github.com/logicalclocks/brewer.git')

def build_agent():
    return Agent(
        name="test",
        description="aaaa",
        system_prompt="bbbb",
        llm=None,
        agents=[
            provider.get_agent("hopsworks_brewer.server.test_agent_garden_tmp.test_2")
        ],
    )

agent = build_agent()
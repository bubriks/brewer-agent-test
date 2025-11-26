from hopsworks_brewer.framework import Agent, AgentProvider

provider = AgentProvider(repo='https://github.com/logicalclocks/brewer-agent-test.git')

def build_agent():
    return Agent(
        name="test",
        description="aaaa",
        system_prompt="bbbb",
        llm=None,
        agents=[
            provider.get_agent("test_2")
        ],
    )

agent = build_agent()

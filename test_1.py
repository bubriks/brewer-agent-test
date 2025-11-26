from hopsworks_brewer.framework import Agent, AgentProvider

provider = AgentProvider(repo='https://github.com/bubriks/brewer-agent-test.git')

def build_agent():
    return Agent(
        name="test",
        description="aaaa",
        system_prompt="bbbb",
        llm=None,
        agents=[
            provider.get_agent("test_2"),
            provider.get_agent("sum")
        ],
    )

agent = build_agent()

from hopsworks_brewer.framework import Agent

def build_agent():
    return Agent(
        name="test_2",
        description="aaaa",
        system_prompt="bbbb",
        llm=None,
        agents=[],
    )

agent = build_agent()
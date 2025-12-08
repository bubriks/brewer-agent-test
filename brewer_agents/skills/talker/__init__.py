from pathlib import Path

from llama_index.core.workflow import Context

from hopsworks_brewer.framework import Agent, Constants, Team
from hopsworks_brewer.models import Registry
from hopsworks_brewer.personality import personality


async def postprocess(ctx: Context):
    tool_calls = await ctx.store.get("pending_tool_calls")
    if tool_calls and tool_calls[0].tool_name == Constants.HANDOFF_PREFIX + "set_title":
        return  # Title is being set, no need to verify
    # Verify that the title is set
    if not await ctx.store.get("is_title_set", False):
        raise ValueError(
            "Chat title has not been set. Please set the title using the corresponding tool."
        )


def talker():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.join(personality, Agent.read(location / "instructions.md")),
        llm=Registry().get(),
        postprocessor=postprocess,
        agents=["chart_drawer", "feature_engineer", "set_title"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(talker)

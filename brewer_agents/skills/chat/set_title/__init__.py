from pathlib import Path

from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.events import TitleEvent
from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.framework.events import WrappedEvent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


class SetTitleOutput(BaseModel):
    title: str = Field(description="The appropriate chat title.")


async def postprocessor(ctx: Context):
    output_data = await ctx.store.get("output_data")
    Session().change_title(output_data.title)
    ctx.write_event_to_stream(WrappedEvent(event=TitleEvent(to=output_data.title)))
    await ctx.store.set("is_title_set", True)


def set_title():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get("gpt-4.1-nano"),
        output_model=SetTitleOutput,
        postprocessor=postprocessor,
        functional=True,
    )


def add_to_team(team: Team):
    team.add_agent_initializer(set_title)

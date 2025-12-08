from pathlib import Path
from typing import Any

import yaml
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from pydantic import BaseModel, ConfigDict, Field

from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.models import Registry
from hopsworks_brewer.personality import personality


class TargetFeatureSpecification(BaseModel):
    name: str
    description: str
    type: str
    primary: bool = Field(default=False)
    event_time: bool = Field(default=False)

    model_config = ConfigDict(extra="allow")


class TargetFeatureGroupSpecification(BaseModel):
    name: str
    version: int
    description: str
    features: list[TargetFeatureSpecification]

    model_config = ConfigDict(extra="allow")


class FeatureGroupSpecification(BaseModel):
    inputs: list[Any]
    target_feature_group: TargetFeatureGroupSpecification
    requirements: list[Any]
    expectations: list[Any]
    guidelines: Any
    job_settings: Any


async def set_feature_group_specification(specification: str, ctx: Context) -> None:
    """Set feature group specification to be used in create_feature_group; this tool should be called before them."""
    await ctx.store.set("feature_group_specification", None)
    try:
        spec = FeatureGroupSpecification.model_validate(yaml.safe_load(specification))
    except Exception as e:
        raise ValueError(f"The YAML in specification is incorrect. {e}") from e
    await ctx.store.set("feature_group_specification", spec)


def feature_engineer():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.join(personality, Agent.read(location / "instructions.md")),
        llm=Registry().get(),
        agents=[
            "talker",
            "create_feature_group",
            "preview_file_data",
            "preview_feature_group",
        ],
        tools=["set_feature_group_specification"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(feature_engineer)
    team.add_tool(FunctionTool.from_defaults(set_feature_group_specification))

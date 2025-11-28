import uuid
from pathlib import Path
from typing import Any

import jsonschema
import yaml
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from pydantic import BaseModel

from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.models import Registry
from hopsworks_brewer.personality import personality


class ChartAggregationSpecification(BaseModel):
    input: Any
    preprocessing: Any


class ChartSpecification(BaseModel):
    json_schema: Any
    aggregation: ChartAggregationSpecification
    visualization: Any


async def set_chart_specification(specification: str, ctx: Context) -> None:
    """Set chart specification to be used in aggregate_chart_data and visualize_chart_data; this tool should be called before them."""
    await ctx.store.set("chart_specification", None)
    try:
        spec = ChartSpecification.model_validate(yaml.safe_load(specification))
    except Exception as e:
        raise ValueError(f"The YAML in specification is incorrect. {e}") from e
    try:
        jsonschema.Draft202012Validator.check_schema(spec.json_schema)
    except Exception as e:
        raise ValueError(
            f"The json_schema of the YAML specification is incorrect. {e}"
        ) from e
    await ctx.store.set("chart_specification", spec)
    await ctx.store.set("chart_id", str(uuid.uuid4()))


def chart_drawer():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.join(personality, Agent.read(location / "instructions.md")),
        llm=Registry().get(),
        agents=[
            "talker",
            "aggregate_chart_data",
            "visualize_chart_data",
            "preview_file_data",
            "preview_feature_group",
        ],
        tools=["set_chart_specification"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(chart_drawer)
    team.add_tool(FunctionTool.from_defaults(set_chart_specification))

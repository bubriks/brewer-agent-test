from pathlib import Path
from typing import Literal

import orjson
import yaml
from jinja2 import Template
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.events import ChartEvent
from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.framework.events import WrappedEvent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


class VisualizeChartDataOutput(BaseModel):
    title: str = Field(description="The title of the chart.")
    description: str = Field(
        description="A brief description of the chart including where the data comes from."
    )
    plugins_needed: Literal["boxplot", "matrix", "treemap"] | None = Field(
        description=(
            "Specify which Chart.js plugins are needed based on chart type: "
            "'boxplot' for box/violin plots, 'matrix' for heatmaps, 'treemap' for treemaps, "
            "or null for standard Chart.js types (bar, line, pie, scatter, etc.)."
        )
    )
    script: str = Field(
        description=(
            "The JavaScript code that goes inside the {SCRIPT} placeholder. "
            "Must start with chart configuration and NOT include any HTML elements, CSS styles, additional script tags, or try-catch blocks. "
            "Should only contain Chart.js initialization code that works with the pre-defined chartData variable."
        )
    )


async def preprocessor(ctx: Context):
    # Validation (no mutations, can raise exceptions)
    spec = await ctx.store.get("chart_specification", None)
    if spec is None:
        raise ValueError(
            "You should first set the chart specfication to use by calling set_chart_specification"
        )

    # Preparation (no exceptions, can mutate)
    memory = await ctx.store.get("memory")
    await memory.aput(
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=f"The aggregated data follows this JSON schema:\n\n{orjson.dumps(spec.json_schema).decode()}",
        )
    )
    await memory.aput(
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=f"The visualization script should follow this chart design specification:\n\n{yaml.safe_dump(spec.visualization)}",
        ),
    )


async def postprocessor(ctx: Context):
    output_data = await ctx.store.get("output_data")
    chart_id = await ctx.store.get("chart_id")
    chart_path = Path("charts") / chart_id
    html_path = chart_path / "chart.html"

    json_path_str = str(
        Session().chat_root(path=chart_path / "data.json").relative_to("/")
    )

    # fill in html template
    location = Path(__file__).parent
    html_template = Template(Agent.read(location / "template.html.jinja"))
    html = html_template.render(
        TITLE=output_data.title,
        DATA_PATH=Path("/hopsworks-api/api/project/")
        / str(Session().project.id)
        / "dataset/download/with_auth"
        / json_path_str,
        SCRIPT=output_data.script,
        PLUGINS=get_plugin_scripts(output_data.plugins_needed)
        if output_data.plugins_needed
        else "",
    )

    Session().chat_upload(html_path, html)

    Session().add_chart_to_hopsworks(
        title=output_data.title,
        description=output_data.description,
        path=html_path,
        job_id=await ctx.store.get("chart_job_id"),
    )

    ctx.write_event_to_stream(WrappedEvent(event=ChartEvent(path=html_path)))


def get_plugin_scripts(plugins_needed: str) -> str:
    """Generate plugin script tags based on required plugins."""
    plugin_map = {
        "boxplot": '<script src="https://cdn.jsdelivr.net/npm/@sgratzl/chartjs-chart-boxplot"></script>',
        "matrix": '<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix"></script>',
        "treemap": '<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-treemap"></script>',
        "none": "",
    }
    return plugin_map.get(plugins_needed, "")


def visualize_chart_data():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get(),
        preprocessor=preprocessor,
        output_model=VisualizeChartDataOutput,
        postprocessor=postprocessor,
        functional=True,
    )


def add_to_team(team: Team):
    team.add_agent_initializer(visualize_chart_data)

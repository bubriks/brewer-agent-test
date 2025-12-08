from pathlib import Path

import jsonschema
import orjson
import yaml
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.events import FileEvent
from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.framework.events import WrappedEvent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


class AggregateChartDataOutput(BaseModel):
    script: str = Field(
        description="The Python code aggregating the data according to the given specification."
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
            content=f"The output of the aggregation script should be a JSON following this JSON schema:\n\n{orjson.dumps(spec.json_schema).decode()}",
        )
    )
    await memory.aput(
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=f"The aggregation script should use the following inputs and do the following data preparation steps:\n\n{yaml.safe_dump(spec.aggregation.model_dump())}",
        ),
    )


async def postprocessor(ctx: Context):
    output_data = await ctx.store.get("output_data")
    chart_id = await ctx.store.get("chart_id")
    script_path: Path = Path("charts") / chart_id / "aggregate.py"
    Session().chat_upload(script_path, output_data.script)
    ctx.write_event_to_stream(WrappedEvent(event=FileEvent(path=script_path)))
    res = await Session().worker_execute(
        script_path, "Logs of the aggregation script execution:"
    )
    if res.data.returncode != 0:
        raise Exception(
            f"Worker execution failed. Return code: {res.data.returncode}. The logs:\n\n{res.data.output}"
        )

    spec = await ctx.store.get("chart_specification")
    jsonschema.Draft202012Validator(spec.json_schema).validate(
        orjson.loads(Session().chat_download(Path("charts") / chart_id / "data.json"))
    )

    chart_job = Session().create_job(name=f"chart_{chart_id}", path=script_path)
    await ctx.store.set("chart_job_id", chart_job.id)


def aggregate_chart_data():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get("gpt-4.1"),
        preprocessor=preprocessor,
        output_model=AggregateChartDataOutput,
        postprocessor=postprocessor,
        functional=True,
        tools=["install_python_requirements"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(aggregate_chart_data)

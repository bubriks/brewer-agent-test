from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Template
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.events import FileEvent
from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.framework.events import WrappedEvent
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


if TYPE_CHECKING:
    from hopsworks_brewer.skills.pipelines.feature.feature_engineer import (
        FeatureGroupSpecification,
    )


location = Path(__file__).parent


class CreateFeatureGroupOutput(BaseModel):
    script: str = Field(
        description="The Python code creating a feature group according to the given specification."
    )


async def preprocessor(ctx: Context):
    # Validation (no mutations, can raise exceptions)
    spec: FeatureGroupSpecification | None = await ctx.store.get(
        "feature_group_specification", None
    )
    if spec is None:
        raise ValueError(
            "You should first set the feature group specification to use by calling set_feature_group_specification"
        )

    # Preparation (no exceptions, can mutate)
    memory = await ctx.store.get("memory")
    template: Template = Template(Agent.read(location / "dynamic.md.jinja"))
    await memory.aput(
        ChatMessage(role=MessageRole.SYSTEM, content=template.render(spec=spec))
    )


async def postprocessor(ctx: Context):
    spec: FeatureGroupSpecification = await ctx.store.get("feature_group_specification")
    tfg = spec.target_feature_group

    output_data = await ctx.store.get("output_data")
    script_path: Path = Path(f"create_{tfg.name}_v{tfg.version}.py")
    Session().chat_upload(script_path, output_data.script)
    ctx.write_event_to_stream(WrappedEvent(event=FileEvent(path=script_path)))
    res = await Session().worker_execute(
        script_path, "Logs of the feature group creation script:"
    )
    if res.data.returncode != 0:
        raise Exception(
            f"Worker execution failed. Return code: {res.data.returncode}. The logs:\n\n{res.data.output}"
        )

    # For now, we just validate that there a feature group exist named as in the spec
    fs = Session().project.get_feature_store()
    feature_group = fs.get_feature_group(tfg.name, tfg.version)
    if not feature_group:
        raise ValueError(
            f"Feature group {tfg.name} (version {tfg.version}) was not created."
        )


def create_feature_group():
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get("gpt-4.1"),
        preprocessor=preprocessor,
        output_model=CreateFeatureGroupOutput,
        postprocessor=postprocessor,
        functional=True,
        tools=["install_python_requirements"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(create_feature_group)

from pathlib import Path

from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


class FeaturePreview(BaseModel):
    name: str | None = Field(
        default=None, description="The name of the feature, if any."
    )
    description: str | None = Field(
        default=None, description="The description of the feature, if any."
    )
    values: list[str] = Field(
        default_factory=list,
        description="The preview values from this feature.",
    )


class PreviewFeatureGroupOutput(BaseModel):
    features: list[FeaturePreview]


class PreviewFeatureGroupInput(BaseModel):
    name: str = Field(description="The name of the feature group to preview.")


async def preprocess(context: Context):
    # Ensure the feature group is real
    data: PreviewFeatureGroupInput = await context.store.get("input_data")
    if Session().project.get_feature_store().get_feature_group(data.name) is None:
        raise FileNotFoundError(f"Feature group not found: {data.name}")


def preview_feature_group() -> Agent:
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get(),
        preprocessor=preprocess,
        input_model=PreviewFeatureGroupInput,
        output_model=PreviewFeatureGroupOutput,
        functional=True,
        tools=["save_file", "execute_python", "install_python_requirements"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(preview_feature_group)

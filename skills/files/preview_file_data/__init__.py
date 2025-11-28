from pathlib import Path

from llama_index.core.workflow import Context
from pydantic import BaseModel, Field

from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.models import Registry
from hopsworks_brewer.session import Session


class ColumnPreview(BaseModel):
    name: str | None = Field(
        default=None, description="The name of the column, if any."
    )
    values: list[str] = Field(
        default_factory=list,
        description="The preview values from this column.",
    )
    comments: str = Field(
        default="",
        description="Any comments about this column.",
    )


class PreviewFileDataOutput(BaseModel):
    columns: list[ColumnPreview]
    comments: str = Field(
        default="",
        description="Any comments about the dataset.",
    )


class PreviewFileDataInput(BaseModel):
    path: Path = Field(description="The path to the file to preview.")


async def preprocess(context: Context):
    # Ensure the file is real
    data: PreviewFileDataInput = await context.store.get("input_data")
    if (
        not Session()
        .project.get_dataset_api()
        .exists(Session().chat_root(data.path).as_posix())
    ):
        raise FileNotFoundError(f"File not found: {data.path}")


def preview_file_data() -> Agent:
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get(),
        preprocessor=preprocess,
        input_model=PreviewFileDataInput,
        output_model=PreviewFileDataOutput,
        functional=True,
        tools=["save_file", "execute_python", "install_python_requirements"],
    )


def add_to_team(team: Team):
    team.add_agent_initializer(preview_file_data)

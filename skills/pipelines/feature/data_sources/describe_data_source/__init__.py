from pathlib import Path

from pydantic import BaseModel, Field

from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.models import Registry


class DescribeDataSourceInput(BaseModel):
    source: str = Field(description="Data source credentials (storage connector) name")
    database: str = Field(description="Database name")
    group: str = Field(description="Table group name")
    table: str = Field(description="Table name")


class FeatureMetadata(BaseModel):
    """Metadata for a single feature."""

    original_name: str = Field(description="The original column name")
    new_name: str = Field(description="The proposed new feature name")
    type: str = Field(
        description="Feature data type (e.g., 'string', 'bigint', 'timestamp', 'decimal')"
    )
    description: str = Field(description="Human-readable description of the feature")


class DescribeDataSourceOutput(BaseModel):
    features: list[FeatureMetadata] = Field(
        description="All features with completed types and descriptions"
    )
    suggested_primary_key: list[str] = Field(
        description="Suggested primary key column names"
    )
    suggested_event_time: str | None = Field(
        description="Suggested event time column name", default=None
    )


def describe_data_source():
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get(),
        input_model=DescribeDataSourceInput,
        output_model=DescribeDataSourceOutput,
        tools=["preview_data_source"],
        functional=True,
    )


def add_to_team(team: Team):
    team.add_agent_initializer(describe_data_source)

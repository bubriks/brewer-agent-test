import uuid

from llama_index.core.tools import FunctionTool

from hopsworks_brewer.framework import Team


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def add_to_team(team: Team):
    team.add_tool(FunctionTool.from_defaults(generate_uuid))

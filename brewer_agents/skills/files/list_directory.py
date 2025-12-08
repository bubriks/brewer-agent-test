# TODO: Move to Hopsworks MCP
from pathlib import Path

from llama_index.core.tools import FunctionTool

from hopsworks_brewer.session import Session


def list_directory(path: Path) -> list[str]:
    """List the contents of a directory."""
    return (
        Session().project.get_dataset_api().list(Session().chat_root(path).as_posix())
    )


def add_to_team(team):
    team.add_tool(FunctionTool.from_defaults(list_directory))

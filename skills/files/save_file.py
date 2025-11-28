# TODO: Move to Hopsworks MCP
from pathlib import Path

from llama_index.core.tools import FunctionTool

from hopsworks_brewer.framework import Team
from hopsworks_brewer.session import Session


def save_file(path: Path, content: str) -> None:
    """Saves a file into the chat directory."""
    Session().chat_upload(Path(path), content)


def add_to_team(team: Team):
    team.add_tool(FunctionTool.from_defaults(save_file))

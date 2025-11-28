# TODO: Move to Hopsworks MCP
from pathlib import Path

from llama_index.core.tools import FunctionTool

from hopsworks_brewer.framework import Team
from hopsworks_brewer.session import Session


def read_file(path: Path) -> str:
    """Reads a file from the chat directory."""
    return Session().chat_download(path)


def add_to_team(team: Team):
    team.add_tool(FunctionTool.from_defaults(read_file))

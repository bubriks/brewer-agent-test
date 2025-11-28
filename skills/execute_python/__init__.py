# TODO: Move to Hopsworks MCP
from pathlib import Path
from typing import Annotated

from fastmcp.exceptions import ToolError
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from pydantic import BaseModel

from hopsworks_brewer.events import StepEvent
from hopsworks_brewer.framework import Team
from hopsworks_brewer.session import Session


class ExecutionResult(BaseModel):
    output: str = ""
    returncode: int | None = None


async def execute_python(
    path: Path,
    logs_prefix: Annotated[
        str,
        "A sentence prefixing the logs of the execution, for example 'The logs of the data aggregation script:'.",
    ],
    ctx: Context,
) -> ExecutionResult:
    """Execute the Python script at path."""
    path = Path(path)
    try:
        Session().yielder(StepEvent(title="Starting Python..."))
        result = await Session().worker_execute(path, logs_prefix)
    except ToolError as e:
        return ExecutionResult(output=f"Tool Error: {str(e)}", returncode=1)
    except Exception as e:
        return ExecutionResult(output=f"System error occurred: {str(e)}", returncode=1)
    return ExecutionResult(
        output=result.data.output,
        returncode=result.data.returncode,
    )


async def install_python_requirements(requirements: str, ctx: Context) -> str | None:
    """Install a bunch of Python requirements, specified in the requirements.txt style.

    Returns an error message if installation failed, None otherwise.
    """
    if not requirements.strip():
        return None

    Session().chat_upload(Path("requirements.txt"), requirements)

    installer = Path("requirements_installer.py")
    Session().chat_upload(
        installer,
        "import sys\n"
        "import subprocess\n"
        "subprocess.check_call(\n"
        "    [\n"
        "        sys.executable,\n"
        '        "-m",\n'
        '        "pip",\n'
        '        "install",\n'
        '        "--no-cache-dir",\n'
        '        "-r",\n'
        '        "requirements.txt",\n'
        "    ]\n"
        ")\n",
    )

    res = await execute_python(
        installer, "The logs of pip requirements installation:", ctx
    )
    if res.returncode:
        return (
            f"Return code is {res.returncode}.\n\n" + res.output
            or f"Unknown error during installation (the return code is {res.returncode})."
        )
    return None


def add_to_team(team: Team):
    team.add_tool(
        FunctionTool.from_defaults(execute_python),
        FunctionTool.from_defaults(install_python_requirements),
    )

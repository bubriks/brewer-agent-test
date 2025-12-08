# brewer-agents

brewer-agents is a small collection of agent definitions and helper skills used with the `hopsworks_brewer` framework. The repository contains reusable agent initializers, Pydantic models for agent inputs/outputs, prompt and instruction templates, and lightweight tool integrations.

**Goal**: make it easy to define, document, and register agents (conversational or procedural) that interact with data, tooling, and LLMs.

**Contents**:
- `skills/`: agent implementations, tools, and helper modules.
- `team.py`: central place to register agent initializers with a `Team`.

**How agents are defined**

Agents in this repo follow a simple pattern:

1. Define Pydantic models for the input and output schemas.
2. Create an initializer function that returns an `Agent` configured with a description, system prompt, LLM, and optional tools.
3. Expose a small `add_to_team(team: Team)` function that registers the initializer with the `Team`.


Abstract agent template

Below is a generic, minimal template that shows the common structure for any agent initializer in this repository. Replace `InputModel`, `OutputModel`, field names, and `tools` with your agent's specifics.

```python
from pydantic import BaseModel, Field
from hopsworks_brewer.framework import Agent, Team
from hopsworks_brewer.framework.agent_provider import AgentProvider
from hopsworks_brewer.models import Registry
from pathlib import Path


class InputModel(BaseModel):
    # declare inputs the agent expects
    example_field: str = Field(description="Example input field")


class OutputModel(BaseModel):
    # declare outputs the agent will return
    result: str


def my_agent_initializer():
    provider = AgentProvider(repo="repoUrl", version_specifier="versionConstraint")
    location = Path(__file__).parent
    return Agent(
        name=Agent.initializer_name(),
        description=Agent.read(location / "description.md"),
        system_prompt=Agent.read(location / "instructions.md"),
        llm=Registry().get(),
        input_model=InputModel,
        output_model=OutputModel,
        agents=["optional_agent_name", "optional_agent_name", provider / "optional_agent_name"],
        tools=["optional_tool_name"],
        functional=True,
    )


def add_to_team(team: Team):
    # register this initializer so the central `Team` includes it
    team.add_agent_initializer(my_agent_initializer)
```

Key points:
- **Input / Output models**: declare the expected fields and types using `pydantic.BaseModel`. These are used for validation and API contracts.
- **Descriptions & prompts**: keep human-facing `description.md` and `instructions.md` together with the agent's code and load them at runtime with `Agent.read()`.
- **LLM selection**: configure which LLM instance the agent uses (for example via `Registry().get()`), or pass an explicit LLM object to the `Agent`.
- **Agents**: enumerate agents the agent may call; the framework injects agent implementations by name if local and provider when the agent is stored in a separate repository.
- **Tools**: enumerate tool names (strings) the agent may call; the framework injects tool implementations by name.
- **Registration**: expose `add_to_team(team: Team)` which calls `team.add_agent_initializer(...)` so your initializer becomes part of the central `Team`.

Adding a new agent

1. Create a new subfolder under `skills/` (for example `skills/my_agent/`).
2. Add your implementation file (e.g., `__init__.py`) with Pydantic models and an initializer that returns an `Agent`.
3. Add `description.md` and `instructions.md` in the same folder for human-readable documentation and system prompts.
4. Expose `add_to_team(team: Team)` and import/use it in `team.py` to register the initializer.

Helpful conventions
- Use `Agent.initializer_name()` for consistent initializer naming.
- Keep long instruction text in `instructions.md` (these will be loaded at runtime with `Agent.read`).
- Keep the agent file focused on wiring: models, prompts, and the `Agent(...)` call.

Contributions welcome!
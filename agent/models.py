from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from yaml import safe_load

SUPPORTED_EXTENSIONS = [".yaml", ".yml"]


class Node(BaseModel):
    """One workflow node: prompt plus optional skills under the skills directory."""

    model_config = ConfigDict(extra="forbid")

    name: str
    """Node title; normalized to a sandbox function id for DynamicWorkflow."""

    instructions: str = ""
    """Instructions for this node agent."""

    skills: list[str] = Field(default_factory=list)
    """Skill directory names under agent/skills/ to load for this node."""


class PlaybookSpec(BaseModel):
    """Declarative playbook: ordered nodes YAML that builds an orchestrator Agent."""

    model_config = ConfigDict(extra="forbid")

    name: str
    """Playbook title; also used as the orchestrator agent name."""

    description: str | None = None
    """One-line summary of the playbook purpose."""

    model: dict[str, object] = Field(default_factory=dict)
    """Default model settings for the orchestrator and nodes."""

    instructions: str | None = None
    """Shared instructions injected into the orchestrator and node agents."""

    nodes: list[Node] = Field(default_factory=list)
    """Ordered workflow nodes exposed as DynamicWorkflow sub-agents."""

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PlaybookSpec":
        """Load a playbook spec from a YAML file."""

        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f"Playbook file not found: {file}")
        if not file.is_file():
            raise ValueError(f"Playbook path is not a file: {file}")
        if file.suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported playbook extension {file.suffix!r}; "
                f"expected one of {SUPPORTED_EXTENSIONS}"
            )

        spec_dict = safe_load(file.read_bytes())
        return cls.model_validate(spec_dict)

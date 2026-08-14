import os
import re
from pathlib import Path

from fastmcp.client.transports import StdioTransport
from pydantic_ai import Agent
from pydantic_ai.capabilities import WebFetch
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai_harness.dynamic_workflow import DynamicWorkflow
from pydantic_ai_skills import SkillsCapability

from .models import Node, PlaybookSpec

AGENTS_DIR = Path(".agents")
SKILLS_DIRS = [AGENTS_DIR / "skills"]


def _normalize_agent_name(name: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_]+", "_", name.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "agent"
    if cleaned[0].isdigit():
        cleaned = f"a_{cleaned}"
    return cleaned.lower()


def _scan_target_skills(
    skills: list[str], directories: list[Path | str] | None = None
) -> list[Path]:
    if not directories:
        directories = SKILLS_DIRS

    skill_dirs: list[Path] = []

    for dir in directories:
        base_path = Path(dir)

        for skill_name in skills:
            skill_path = base_path / skill_name
            if not skill_path.is_dir():
                raise ValueError(
                    f"Skill {skill_name} not found under {directories}. "
                    "Ensure the skill git submodule is initialized."
                )
            skill_file = skill_path / "SKILL.md"
            if not skill_file.exists():
                raise ValueError(f"Skill {skill_name} is missing SKILL.md at {skill_file}")
            skill_dirs.append(skill_path)
    return skill_dirs


def _make_gitlab_mcptools():
    api_url = os.environ.get("GITLAB_API_URL")
    if not api_url:
        return []

    pat = os.environ.get("GITLAB_PERSONAL_ACCESS_TOKEN")

    return [
        MCPToolset(
            StdioTransport(
                command="npx",
                args=[
                    "-y",
                    "--registry=https://registry.npmmirror.com",
                    "@zereight/mcp-gitlab",
                ],
                env={"GITLAB_API_URL": api_url, "GITLAB_PERSONAL_ACCESS_TOKEN": pat},
            ),
        )
    ]


def _make_model(config: dict[str, object]) -> Model:
    model_name = config.pop("model", None)
    if not model_name:
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    base_url = config.pop("base_url", None)
    if not base_url:
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    api_key = config.pop("api_key", None)

    settings = ModelSettings(**config)
    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    return OpenAIChatModel(model_name, provider=provider, settings=settings)


def _build_node_hint(node: Node) -> str:
    skills = ", ".join(node.skills) if node.skills else "(none)"
    prompt_preview = (
        node.instructions.strip().splitlines()[0] if node.instructions.strip() else "No prompt."
    )
    if len(prompt_preview) > 120:
        prompt_preview = prompt_preview[:117] + "..."
    return (
        f"- `{_normalize_agent_name(node.name)}` ({node.name}; skills: {skills}): {prompt_preview}"
    )


def _build_instructions(playbook: PlaybookSpec) -> str:
    prompts: list[str] = []

    if playbook.description:
        prompts.append(f"You orchestrate a multi-agent workflow: {playbook.description.strip()}")

    if playbook.instructions and playbook.instructions.strip():
        prompts.append(playbook.instructions.strip())

    prompts.append(
        "Fetch the user-provided commit/MR/PR URL before running nodes:\n"
        "- GitHub URLs (github.com): use WebFetch only.\n"
        "- GitLab URLs (gitlab.com or self-hosted GitLab): use gitlab MCP tools only; "
        "do not use WebFetch for GitLab.\n"
        "Then run the workflow nodes in the declared order via `run_workflow`, "
        "passing prior outputs into later `task` strings."
    )

    if playbook.nodes:
        catalog = "\n".join(_build_node_hint(node) for node in playbook.nodes)
        prompts.append(
            "Use the `run_workflow` tool to coordinate these nodes "
            f"(call each as an async function with `task=...`):\n{catalog}"
        )

    prompts.append(
        "Write a Python script inside `run_workflow` that calls the nodes in order, "
        "passes prior outputs into later `task` strings, and returns the final result."
    )
    return "\n\n".join(prompts)


def build_agent(playbook: PlaybookSpec, directories: list[Path | str] | None = None) -> Agent:
    default_model = _make_model(playbook.model)

    node_agents: list[Agent] = []
    seen: set[str] = set()

    for node in playbook.nodes:
        normalized_node_name = _normalize_agent_name(node.name)
        if normalized_node_name in seen:
            raise ValueError(
                f"Duplicate sub-agent name {normalized_node_name} after normalizing {node.name}."
            )
        seen.add(normalized_node_name)

        capabilities: list = []
        if node.skills:
            skill_dirs = _scan_target_skills(node.skills, directories)
            capabilities.append(SkillsCapability(directories=skill_dirs))

        node_agents.append(
            Agent(
                default_model,
                name=normalized_node_name,
                instructions=node.instructions,
                capabilities=capabilities or None,
            )
        )

    return Agent(
        default_model,
        name=_normalize_agent_name(playbook.name),
        description=playbook.description or playbook.name,
        instructions=_build_instructions(playbook),
        capabilities=[
            WebFetch(local=True),
            DynamicWorkflow(agents=node_agents),
        ],
        toolsets=[*_make_gitlab_mcptools()] or None,
    )

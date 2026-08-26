# agent-playbook

[中文](README_CN.md) | [English](README.md)

agent-playbook is YAML-configured multi-agent workflows powered by pydantic-ai DynamicWorkflow and Agent Skills.

## Features

- YAML playbooks under [`.agents/`](.agents/) on [pydantic-ai](https://ai.pydantic.dev/) + [pydantic-ai-harness](https://github.com/pydantic/pydantic-ai-harness) `DynamicWorkflow`
- Each node declares `instructions` and optional `skills` (loaded via [pydantic-ai-skills](https://github.com/DougTrajano/pydantic-ai-skills) from `.agents/skills/`)
- Built-in `codereview` playbook: fetch a GitHub or GitLab commit/PR/MR URL, then first-principles → 5-whys → code-review
- GitHub via WebFetch; GitLab via [mcp-gitlab](https://github.com/zereight/gitlab-mcp) when `GITLAB_API_URL` is set
- Web chat UI via `agent.to_web()`

## Installation

Python 3.10+. Uses [uv](https://docs.astral.sh/uv/) for dependencies:

```bash
git clone --recurse-submodules https://github.com/lhp0630/agent-playbook.git && cd agent-playbook
uv sync --all-groups
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

Skill packages live under `.agents/skills/` (`first-principles-skill`, `5-whys-skill`, `code-review-skill`).

## Quick Start

Copy `.env.example` to `.env` and set credentials:

```bash
OPENAI_MODEL=your-model-name
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=sk-xxx

# Optional — enable GitLab MCP for GitLab URLs
GITLAB_API_URL=https://gitlab.example.com/api/v4
GITLAB_PERSONAL_ACCESS_TOKEN=glpat-xxx
```

Run a playbook (`-n` must match the YAML `name`; omit to pick at random). Paste a GitHub commit `.diff` / PR URL, or a GitLab commit / MR URL:

```bash
agent -n codereview
```

Optional listen address (defaults `127.0.0.1:8000`):

```bash
agent -n codereview --host 127.0.0.1 --port 8000
```

## Example

| GitHub | GitLab | Result |
| --- | --- | --- |
| ![Web UI — GitHub](./readme_assets/web_1.png) | ![Web UI — GitLab](./readme_assets/web_gitlab.png) | ![Web UI — result](./readme_assets/web_2.png) |

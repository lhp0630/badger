# agent-playbook

[中文](README_CN.md) | [English](README.md)

agent-playbook 是基于 pydantic-ai DynamicWorkflow 与 Agent Skills 的 YAML 多智能体工作流。

## 功能

- Playbook 配置位于 [`.agents/`](.agents/)，基于 [pydantic-ai](https://ai.pydantic.dev/) + [pydantic-ai-harness](https://github.com/pydantic/pydantic-ai-harness) `DynamicWorkflow`
- 每个节点配置 `instructions` 与可选 `skills`（通过 [pydantic-ai-skills](https://github.com/DougTrajano/pydantic-ai-skills) 从 `.agents/skills/` 加载）
- 内置 `codereview`：拉取 GitHub / GitLab 的 commit、PR/MR，再按第一性原理 → 5-whys → 代码评审执行
- GitHub 使用 WebFetch；配置 `GITLAB_API_URL` 后，GitLab 走 [mcp-gitlab](https://github.com/zereight/gitlab-mcp)
- 通过 `agent.to_web()` 提供 Web 聊天界面

## 安装

Python 3.10+，依赖管理使用 [uv](https://docs.astral.sh/uv/)：

```bash
git clone --recurse-submodules https://github.com/lhp0630/agent-playbook.git && cd agent-playbook
uv sync --all-groups
```

若已克隆但未拉取子模块：

```bash
git submodule update --init --recursive
```

技能包位于 `.agents/skills/`（`first-principles-skill`、`5-whys-skill`、`code-review-skill`）。

## 快速开始

复制 `.env.example` 为 `.env`，填入凭证：

```bash
OPENAI_MODEL=your-model-name
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=sk-xxx

# 可选 — 启用 GitLab MCP，用于 GitLab 地址
GITLAB_API_URL=https://gitlab.example.com/api/v4
GITLAB_PERSONAL_ACCESS_TOKEN=glpat-xxx
```

运行 Playbook。粘贴 GitHub commit `.diff` / PR，或 GitLab commit / MR 地址：

```bash
agent
```

可选监听地址（默认 `127.0.0.1:8000`）：

```bash
agent -n codereview --host 127.0.0.1 --port 8000
```

## Playbook YAML

| 字段 | 必填 | 说明 |
| --- | :---: | --- |
| `name` | ✓ | 唯一 ID，如 `codereview` |
| `description` | | 一句话摘要，每次会话根据摘要匹配 Playbook |
| `instructions` | | orchestrator 运行规程 |
| `model` | | LLM 配置：`model`、`base_url`、`api_key`、`temperature` 等 |
| `mcp_servers` | | MCP 工具列表 |
| `mcp_servers[].name` | ✓ | MCP 名称，如 `gitlab` |
| `mcp_servers[].commands` | ✓ | 命令数组，首项为可执行文件 |
| `mcp_servers[].env_vars` | | 环境变量名列表，或 `key: value` 字典 |
| `directories` | | Skill 库路径，默认 `.agents/skills` |
| `nodes` | ✓ | 工作流节点，按列表顺序执行 |
| `nodes[].name` | ✓ | 节点名，规范化后作为 `run_workflow` 函数名 |
| `nodes[].instructions` | | 节点提示词 |
| `nodes[].skills` | ✓ | Skill 或 URI，如 `https://github.com/anthropics/skills.git` |

## 示例

| GitHub | GitLab | 结果 |
| --- | --- | --- |
| ![Web UI — GitHub](./readme_assets/web_1.png) | ![Web UI — GitLab](./readme_assets/web_gitlab.png) | ![Web UI — result](./readme_assets/web_2.png) |

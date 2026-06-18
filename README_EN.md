# Debate

A multi-persona AI debate simulator built with LangChain. Configure virtual characters with distinct personalities and let them debate a topic in an office setting.

All code in this project is written by [MiMo](https://github.com/XiaomiMiMo/MiMo).

## Features

- Configurable Moderator and multiple Personas, each with unique personality, stance, and speaking style
- Moderator auto-generates debate topics, or set one manually
- Each persona can use a different LLM
- Three-tier config priority: `.env` < YAML global config < per-instance config
- Automatic model health check before debate starts

## Installation

Requires Python 3.10+. Uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
git clone https://github.com/lhp0630/debate.git && cd debate
uv sync
```

## Usage

Copy `.env.example` to `.env` and fill in your model settings:

```bash
OPENAI_MODEL=your-model-name
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=sk-xxx
```

Env vars are the lowest priority fallback. If a value is set in YAML, the env var is ignored.

```bash
uv run debate                          # Use .work/personas.yaml
uv run debate --config path/to/yaml    # Use a specific config
uv run python -m debate                # Equivalent
```

The app runs a model health check first, then generates a topic and starts the debate.

## Configuration

On first run, the app creates `.work/personas.yaml` in the project root (copied from `debate/config/personas.yaml`). Edit that file to customize personas.

You can also point to a different config with `--config`:

```bash
uv run debate --config /path/to/personas.yaml
```

Config structure:

```yaml
llm:                          # Global model config (fallback)
  # model: "gpt-4o-mini"
  # base_url: ""
  # api_key: ""

max_rounds: 3
temperature: 0.8

moderator:                    # Debate host
  name: "Dr. Morgan Lee"
  personality: "..."
  topic_directions:           # Topic focus areas
    - "Technology adoption"
  # llm:                      # Per-instance model override
  #   model: "claude-3-haiku"

personas:                     # Debate participants
  - name: "Alice Chen"
    role: "CTO"
    personality: "Pragmatic, data-driven"
    # llm:
    #   model: "gpt-4o"
```

## License

[MIT](LICENSE)

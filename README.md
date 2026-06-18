# Debate

[中文](README.md) [English](README_EN.md)

一个基于 LangChain 的多角色 AI 辩论模拟工具。配置不同人格的虚拟角色，让他们在办公室场景中围绕一个话题展开辩论。

本项目全部代码由 [MiMo](https://github.com/XiaomiMiMo/MiMo) 编写。

## 功能

- 可配置的 Moderator 和多个 Persona，每个角色有独立的人格、立场和说话风格
- Moderator 自动生成辩题，或手动指定
- 每个角色可单独配置不同的 LLM 模型
- 支持 `.env` 环境变量和 YAML 配置文件，三级优先级：`.env` < yaml 全局配置 < 子实例配置
- 启动前自动检查所有模型连通性

## 安装

需要 Python 3.10+，使用 [uv](https://docs.astral.sh/uv/) 管理依赖：

```bash
git clone https://github.com/lhp0630/debate.git && cd debate
uv sync
```

## 运行

复制 `.env.example` 为 `.env`，填入模型信息：

```bash
OPENAI_MODEL=your-model-name
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=sk-xxx
```

环境变量作为最低优先级的 fallback，yaml 中配置了则不使用环境变量。

```bash
uv run debate                          # 使用 .work/personas.yaml
uv run debate --config path/to/yaml    # 指定配置文件
uv run python -m debate                # 等效
```

程序会先进行模型健康检查，通过后自动生成辩题并开始辩论。

## 配置

首次运行时，程序会在项目根目录下创建 `.work/personas.yaml`，内容从 `debate/config/personas.yaml` 复制而来。编辑 `.work/personas.yaml` 即可自定义角色。

也可以通过 `--config` 参数指定其他配置文件：

```bash
uv run debate --config /path/to/personas.yaml
```

配置结构：

```yaml
llm:                          # 全局模型配置（fallback）
  # model: "gpt-4o-mini"
  # base_url: ""
  # api_key: ""

max_rounds: 3
temperature: 0.8

moderator:                    # 主持人
  name: "Dr. Morgan Lee"
  personality: "..."
  topic_directions:           # 辩题方向
    - "Technology adoption"
  # llm:                      # 可单独配置模型
  #   model: "claude-3-haiku"

personas:                     # 辩论参与者
  - name: "Alice Chen"
    role: "CTO"
    personality: "Pragmatic, data-driven"
    # llm:
    #   model: "gpt-4o"
```

## License

[MIT](LICENSE)

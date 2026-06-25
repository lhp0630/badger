from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class LlmConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str = ""
    base_url: str = ""
    api_key: str = ""


class RoleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str = ""
    llm: LlmConfig = Field(default_factory=LlmConfig)


class StepConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str
    system_prompt: str = ""
    input: str = ""


class StageConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str = ""
    steps: list[StepConfig] = Field(default_factory=list)


class FlowDef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = ""
    description: str = ""
    stages: list[StageConfig] = Field(default_factory=list)


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    llm: LlmConfig = Field(default_factory=LlmConfig)
    temperature: float = 0.8
    max_rounds: int = 3
    instructions: str = ""
    topic: str = ""
    roles: list[RoleConfig] = Field(default_factory=list)
    flow: FlowDef = Field(default_factory=FlowDef)

    def resolve_topic(self, config_dir: Path | None = None) -> str:
        if not self.topic:
            return ""

        if self.topic.startswith("file:"):
            file_path = self.topic[5:]
            if config_dir and not Path(file_path).is_absolute():
                file_path = config_dir / file_path
            return Path(file_path).read_text(encoding="utf-8").strip()

        return self.topic

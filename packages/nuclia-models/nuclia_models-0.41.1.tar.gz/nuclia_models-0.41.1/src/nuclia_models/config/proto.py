import typing

from pydantic import BaseModel, Field

from nuclia_models.worker.proto import UserLearningKeys


class LLMConfig(BaseModel):
    user_keys: typing.Optional[UserLearningKeys] = Field(default=None)
    generative_model: str = Field(default="")
    generative_provider: str = Field(default="")
    generative_prompt_id: str = Field(default="")


class VLLMExtractionConfig(BaseModel):
    rules: list[str] = Field(default_factory=list)
    llm: typing.Optional[LLMConfig] = Field(default=None)


class AITables(BaseModel):
    llm: typing.Optional[LLMConfig] = Field(default=None)


class SplitConfig(BaseModel):
    max_paragraph: int = Field(default=0)


class ExtractConfig(BaseModel):
    """
    Hey, developer! Keep this in sync with corresponding pydantic model in learning_config.models
    """

    name: str = Field(default="")
    vllm_config: typing.Optional[VLLMExtractionConfig] = Field(default=None)
    ai_tables: typing.Optional[AITables] = Field(default=None)
    split: typing.Optional[SplitConfig] = Field(default=None)

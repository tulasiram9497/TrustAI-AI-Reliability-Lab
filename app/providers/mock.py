from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UsageMetadata(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ProviderResponse(BaseModel):
    output: str
    provider: str
    model_id: str
    usage: UsageMetadata | None = Field(default_factory=UsageMetadata)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MockProvider:
    """Deterministic, offline model provider used for tests and local evaluation."""

    def __init__(self, model_id: str = "mock-model-v1", provider: str = "mock") -> None:
        self.model_id = model_id
        self.provider = provider

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        normalized = (prompt or "").strip().lower()
        if "2 + 2" in normalized or "2+2" in normalized:
            output = "4"
        elif "capital of france" in normalized:
            output = "Paris"
        elif "hello" in normalized:
            output = "Hi there!"
        else:
            output = "mock-output"

        usage = UsageMetadata(
            prompt_tokens=max(1, len(prompt.split())),
            completion_tokens=max(1, len(output.split())),
        )
        usage.total_tokens = usage.prompt_tokens + usage.completion_tokens

        return ProviderResponse(
            output=output,
            provider=self.provider,
            model_id=self.model_id,
            usage=usage,
            metadata={
                "system_prompt": system_prompt,
                "timeout": timeout,
                "request_kwargs": kwargs,
            },
        )

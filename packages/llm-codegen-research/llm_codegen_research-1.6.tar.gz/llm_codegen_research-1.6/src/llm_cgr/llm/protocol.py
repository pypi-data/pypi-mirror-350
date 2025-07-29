"""Protocol for the completion API of an LLM service."""

from typing import Any, Protocol


class GenerationProtocol(Protocol):
    """
    Protocol that describes how to access the generation API of an LLM service.
    """

    def generate(
        self,
        user: str,
        system: str | None = None,
        model: str | None = None,
        samples: int = 1,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> list[str]:
        pass

    def chat(
        self,
        user: str,
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        pass

    @property
    def history(self) -> list[dict[str, Any]]:
        pass

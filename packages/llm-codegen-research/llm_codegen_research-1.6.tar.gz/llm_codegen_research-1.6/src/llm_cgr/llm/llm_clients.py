"""Classes for access to generation APIs of LLM services."""

from typing import Any

import anthropic
import openai
import together

from llm_cgr.defaults import DEFAULT_MAX_TOKENS
from llm_cgr.llm.llm_base import Base_LLM
from llm_cgr.llm.protocol import GenerationProtocol


def get_llm(
    model: str,
    system: str | None = None,
) -> GenerationProtocol:
    """
    Initialise the correct LLM client for the given model.
    """
    if "claude" in model:
        return Anthropic_LLM(model=model, system=system)

    if "gpt" in model or "o1" in model:
        return OpenAI_LLM(model=model, system=system)

    return TogetherAI_LLM(model=model, system=system)


class OpenAI_LLM(Base_LLM):
    """Class to access LLMs via the OpenAI API."""

    def __init__(
        self,
        model: str | None = None,
        system: str | None = None,
    ) -> None:
        """
        Initialise the OpenAI client.

        Requires the OPENAI_API_KEY environment variable to be set.
        """
        super().__init__(model=model, system=system)
        self._client = openai.OpenAI()

    def _build_message(
        self,
        role: str,
        content: str,
    ) -> dict[str, str]:
        """Build an OpenAI model message."""
        return {"role": role, "content": content}

    def _build_input(
        self,
        user: str,
        system: str | None = None,
    ) -> list[dict[str, Any]]:
        """Build the full OpenAI model input."""
        input = []
        if system:
            input.append(self._build_message(role="system", content=system))
        input.append(self._build_message(role="user", content=user))
        return input

    def _get_response(
        self,
        input: list[dict[str, Any]],
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Generate a model response from the OpenAI API."""
        response = self._client.responses.create(
            input=input,
            model=model or self._model,
            temperature=temperature or openai.NOT_GIVEN,
            max_output_tokens=max_tokens or openai.NOT_GIVEN,
        )
        return response.output_text


class TogetherAI_LLM(Base_LLM):
    """Class to access LLMs via the TogetherAI API."""

    def __init__(
        self,
        model: str | None = None,
        system: str | None = None,
    ) -> None:
        """
        Initialise the TogetherAI client.

        Requires the TOGETHER_API_KEY environment variable to be set.
        """
        super().__init__(model=model, system=system)
        self._client = together.Together()

    def _build_message(
        self,
        role: str,
        content: str,
    ) -> dict[str, str]:
        """Build a TogetherAI model message."""
        return {"role": role, "content": content}

    def _build_input(
        self,
        user: str,
        system: str | None = None,
    ) -> list[dict[str, Any]]:
        """Build the full TogetherAI model input."""
        input = []
        if system:
            input.append(self._build_message(role="system", content=system))
        input.append(self._build_message(role="user", content=user))
        return input

    def _get_response(
        self,
        input: list[dict[str, Any]],
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Generate a model response from the TogetherAI API."""
        response = self._client.chat.completions.create(
            model=model or self._model,
            messages=input,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


class Anthropic_LLM(Base_LLM):
    """Class to access LLMs via the Anthropic API."""

    def __init__(
        self,
        model: str | None = None,
        system: str | None = None,
    ) -> None:
        """
        Initialise the Anthropic client.

        Requires the ANTHROPIC_API_KEY environment variable to be set.
        """
        super().__init__(model=model, system=system)
        self._client = anthropic.Anthropic()

    def _build_message(
        self,
        role: str,
        content: str,
    ) -> dict[str, str | list[dict[str, str]]]:
        """Build an Anthropic model message."""
        return {
            "role": role,
            "content": [
                {
                    "type": "text",
                    "text": content,
                }
            ],
        }

    def _build_input(
        self,
        user: str,
        system: str | None = None,
    ) -> list[dict[str, Any]]:
        """Build the full Anthropic model input."""
        return [self._build_message(role="user", content=user)]

    def _get_response(
        self,
        input: list[dict[str, Any]],
        system: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Generate a model response from the Anthropic API."""
        response = self._client.messages.create(
            model=model or self._model,
            system=system or self._system or anthropic.NOT_GIVEN,
            messages=input,
            temperature=temperature or anthropic.NOT_GIVEN,
            max_tokens=max_tokens or DEFAULT_MAX_TOKENS,
        )
        return response.content[0].text

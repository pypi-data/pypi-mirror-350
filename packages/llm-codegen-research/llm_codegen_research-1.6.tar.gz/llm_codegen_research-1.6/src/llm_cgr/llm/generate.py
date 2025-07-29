"""API utilities for interfacing with the generation models."""

from llm_cgr.defaults import DEFAULT_MODEL
from llm_cgr.llm.llm_clients import get_llm
from llm_cgr.llm.prompts import BOOL_SYSTEM_PROMPT, LIST_SYSTEM_PROMPT


def generate(
    user: str,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    temperature: float | None = None,
    **generate_kwargs,
) -> str:
    """
    Simple function to quickly prompt a model for a response.
    """
    client = get_llm(model=model, system=system)
    [result] = client.generate(
        user=user,
        system=system,
        temperature=temperature,
        **generate_kwargs,
    )
    return result


def generate_list(
    user: str,
    system: str = LIST_SYSTEM_PROMPT,
    model: str = DEFAULT_MODEL,
) -> list[str]:
    """
    Simple function to quickly prompt a model for a list of words.
    """
    _response = generate(
        user=user,
        system=system,
        model=model,
    )
    _response = _trim_code_block(text=_response)

    try:
        _list = eval(_response)
    except Exception as e:
        print(f"Error evaluating response.\nresponse: {_response}\nexception: {e}")
        _list = []

    if not isinstance(_list, list):
        print(f"Error querying list. Response is not a list: {_list}")
        _list = []

    if any(not isinstance(item, str) for item in _list):
        print(f"Error querying list. Response contains non-string items: {_list}")
        _list = []

    return _list


def generate_bool(
    user: str,
    system: str = BOOL_SYSTEM_PROMPT,
    model: str = DEFAULT_MODEL,
) -> bool:
    """
    Simple function to quickly prompt a model for a boolean value.
    """
    _response = generate(
        user=user,
        system=system,
        model=model,
    )
    _response = _trim_code_block(text=_response)

    try:
        _bool = eval(_response)
    except Exception as e:
        print(f"Error evaluating response.\nresponse: {_response}\nexception: {e}")
        _bool = False

    if not isinstance(_bool, bool):
        print(f"Error querying boolean. Response is not a boolean: {_bool}")
        _bool = False

    return _bool


def _trim_code_block(
    text: str,
) -> str:
    """
    Cut the response from any potential code block.
    """
    text = text.strip()
    if text.startswith("```python"):
        text = text.split("```python")[1]
    if text.endswith("```"):
        text = text.split("```")[0]
    return text.strip()

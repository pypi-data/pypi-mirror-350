from dataclasses import dataclass
from functools import lru_cache
from inspect import isclass
from typing import Callable, Optional, List, Union
import sys

from pydantic import BaseModel, Field, validator

from chaiverse.inferno import InfernoModel, InfernoCallableMixin, InfernoPartial


class _PromptFormatter(InfernoCallableMixin):
    memory_template: Optional[str] = Field(default = "{bot_name}'s Persona: {memory}\n####\n")
    prompt_template: Optional[str] = Field(
        default="{prompt}\n<START>\n"
    )
    bot_template: str = Field(default="{bot_name}: {message}\n")
    user_template: str = Field(default="{user_name}: {message}\n")
    response_template: str = Field(default="{bot_name}:")
    truncate_by_message: Optional[bool] = Field(default=False)
    scorer: Optional[Union[Callable, InfernoPartial]]


class PygmalionFormatter(_PromptFormatter):
    pass


class VicunaFormatter(_PromptFormatter):
    memory_template: str = "### Instruction:\n{memory}\n"
    prompt_template: str = "### Input:\n{prompt}\n"
    bot_template: str = "{bot_name}: {message}\n"
    user_template: str = "{user_name}: {message}\n"
    response_template: str = "### Response:\n{bot_name}:"


class ChatMLFormatter(_PromptFormatter):
    memory_template: str = "<|im_start|>system\n{memory}<|im_end|>\n"
    prompt_template: str = "<|im_start|>user\n{prompt}<|im_end|>\n"
    bot_template: str = "<|im_start|>assistant\n{bot_name}: {message}<|im_end|>\n"
    user_template: str = "<|im_start|>user\n{user_name}: {message}<|im_end|>\n"
    response_template: str = "<|im_start|>assistant\n{bot_name}:"


class EmptyFormatter(_PromptFormatter):
    memory_template: str = ""
    prompt_template: str = ""
    bot_template: str = ""
    user_template: str = ""
    response_template: str = ""


class XLRewardFormatter(_PromptFormatter):
    memory_template: str = ""
    prompt_template: str = ""
    bot_template: str = Field(default="{bot_name}: {message}\n")
    user_template: str = Field(default="{user_name}: {message}\n")
    response_template: str = ""


class ModeratorFormatter(_PromptFormatter):
    memory_template: str = "{memory}\n"
    prompt_template: str = "{prompt}\n"
    bot_template: str = "{bot_name}: {message}\n"
    user_template: str = "{user_name}: {message}\n"
    response_template: str = ""


@lru_cache()
def get_available_formatters():
    formatters = {}
    current_module = sys.modules[__name__]
    for key in dir(current_module):
        cls = getattr(current_module, key)
        if isclass(cls) and issubclass(cls, _PromptFormatter) and ("PromptFormatter" not in key):
            key = key.replace("Formatter", "")
            formatters[key] = cls()
    return formatters


class PromptFormatter(_PromptFormatter):
    memory_template: Optional[str] = Field(
        title="Memory template",
        description="A template controlling how your model handles a bot's permanent memory. Must contain `{memory}`.",
        default = "{bot_name}'s Persona: {memory}\n####\n",
        enum=[formatter.memory_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="A template controlling how your model handles a bot temporary prompt. Must contain `{prompt}'.",
        default="{prompt}\n<START>\n",
        enum=[formatter.prompt_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    bot_template: str = Field(
        title="Bot message template",
        description="A template controlling how your model handles a bot's messages. Must contain `{bot_name}' and `{message}'.",
        default="{bot_name}: {message}\n",
        enum=[formatter.bot_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    user_template: str = Field(
        title="User message template",
        description="A template controlling how your model handles the user's messages. Must contain `{user_name}' and `{message}'.",
        default="{user_name}: {message}\n",
        enum=[formatter.user_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    response_template: str = Field(
        title="Bot response template",
        description="A template controlling how your model is prompted for a bot response. Must contain `{bot_name}'.",
        default="{bot_name}:",
        enum=[formatter.response_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    truncate_by_message: Optional[bool] = Field(
        title="Truncate by message",
        description="Truncate the conversation history in the context window on a message-by-message basis, rather than a character-by-character basis.",
        default=False,
        format="checkbox"
    )

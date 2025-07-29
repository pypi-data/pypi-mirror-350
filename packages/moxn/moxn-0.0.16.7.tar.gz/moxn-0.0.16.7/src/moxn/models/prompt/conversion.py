from itertools import chain
from typing import Literal, Sequence, overload

from moxn.base_models.blocks.context import MessageContext
from moxn.models import message as msg
from moxn_types.content import Provider
from moxn_types.type_aliases.anthropic import AnthropicMessagesParam
from moxn_types.type_aliases.google import GoogleMessagesParam
from moxn_types.type_aliases.openai_chat import OpenAIChatMessagesParam


class MessageConverter:
    """Handles conversion of messages to provider-specific formats."""

    @overload
    @staticmethod
    def to_message_params(
        messages: list[msg.Message],
        provider: Literal[Provider.ANTHROPIC],
        context: MessageContext | dict | None = None,
    ) -> Sequence[AnthropicMessagesParam]: ...

    @overload
    @staticmethod
    def to_message_params(
        messages: list[msg.Message],
        provider: Literal[Provider.OPENAI_CHAT],
        context: MessageContext | dict | None = None,
    ) -> Sequence[OpenAIChatMessagesParam]: ...

    @overload
    @staticmethod
    def to_message_params(
        messages: list[msg.Message],
        provider: Literal[Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX],
        context: MessageContext | dict | None = None,
    ) -> Sequence[GoogleMessagesParam]: ...

    @staticmethod
    def to_message_params(
        messages: list,
        provider: Provider,
        context: MessageContext | dict | None = None,
    ) -> (
        Sequence[AnthropicMessagesParam]
        | Sequence[OpenAIChatMessagesParam]
        | Sequence[GoogleMessagesParam]
    ):
        """Convert messages to provider-specific format."""
        if context is None:
            context = MessageContext.create_empty()
        elif isinstance(context, dict):
            context = MessageContext.from_variables(context)
        elif not isinstance(context, MessageContext):
            raise ValueError(f"Unsupported context type: {type(context)}")

        message_params = list(
            chain.from_iterable(
                msg.to_message_params(provider, context) for msg in messages
            )
        )
        return message_params  # type: ignore

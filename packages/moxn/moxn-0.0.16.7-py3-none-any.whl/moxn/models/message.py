from typing import Sequence, cast

from moxn import base_models
from moxn.base_models.blocks.context import MessageContext
from moxn.base_models.providers.anthropic import (
    AdapterAnthropicAssistant,
    AdapterAnthropicSystem,
    AdapterAnthropicToolCall,
    AdapterAnthropicToolResult,
    AdapterAnthropicUser,
)
from moxn.base_models.providers.base import ProviderAdapter
from moxn.base_models.providers.google_gemini import (
    AdapterGoogleGeminiModel,
    AdapterGoogleGeminiSystem,
    AdapterGoogleGeminiToolCall,
    AdapterGoogleGeminiToolResult,
    AdapterGoogleGeminiUser,
)
from moxn.base_models.providers.google_vertex import (
    AdapterGoogleVertexModel,
    AdapterGoogleVertexSystem,
    AdapterGoogleVertexToolCall,
    AdapterGoogleVertexToolResult,
    AdapterGoogleVertexUser,
)
from moxn.base_models.providers.openai_chat import (
    AdapterOpenAIChatAssistant,
    AdapterOpenAIChatDeveloper,
    AdapterOpenAIChatSystem,
    AdapterOpenAIChatToolCall,
    AdapterOpenAIChatToolResult,
    AdapterOpenAIChatUser,
)
from moxn_types import core
from moxn_types.content import (
    MessageRole,
    Provider,
)
from moxn_types.type_aliases.anthropic import (
    AnthropicMessagesParam,
)
from moxn_types.type_aliases.google import (
    GoogleMessagesParam,
)
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatMessagesParam,
)

PROVIDER_ROLE_ADAPTERS = {
    Provider.ANTHROPIC: {
        MessageRole.SYSTEM: AdapterAnthropicSystem,
        MessageRole.USER: AdapterAnthropicUser,
        MessageRole.ASSISTANT: AdapterAnthropicAssistant,
        MessageRole.TOOL_CALL: AdapterAnthropicToolCall,
        MessageRole.TOOL_RESULT: AdapterAnthropicToolResult,
    },
    Provider.OPENAI_CHAT: {
        MessageRole.SYSTEM: AdapterOpenAIChatSystem,
        MessageRole.USER: AdapterOpenAIChatUser,
        MessageRole.ASSISTANT: AdapterOpenAIChatAssistant,
        MessageRole.DEVELOPER: AdapterOpenAIChatDeveloper,
        MessageRole.TOOL_CALL: AdapterOpenAIChatToolCall,
        MessageRole.TOOL_RESULT: AdapterOpenAIChatToolResult,
    },
    Provider.GOOGLE_GEMINI: {
        MessageRole.SYSTEM: AdapterGoogleGeminiSystem,
        MessageRole.USER: AdapterGoogleGeminiUser,
        MessageRole.MODEL: AdapterGoogleGeminiModel,
        MessageRole.TOOL_CALL: AdapterGoogleGeminiToolCall,
        MessageRole.TOOL_RESULT: AdapterGoogleGeminiToolResult,
    },
    Provider.GOOGLE_VERTEX: {
        MessageRole.SYSTEM: AdapterGoogleVertexSystem,
        MessageRole.USER: AdapterGoogleVertexUser,
        MessageRole.MODEL: AdapterGoogleVertexModel,
        MessageRole.TOOL_CALL: AdapterGoogleVertexToolCall,
        MessageRole.TOOL_RESULT: AdapterGoogleVertexToolResult,
    },
}


def get_provider_role_adapter(provider: Provider, role: MessageRole) -> ProviderAdapter:
    if provider not in PROVIDER_ROLE_ADAPTERS:
        raise ValueError(f"Unsupported provider: {provider}")
    if role not in PROVIDER_ROLE_ADAPTERS[provider]:
        raise ValueError(f"Unsupported role: {role}")
    provider_adapter = cast(ProviderAdapter, PROVIDER_ROLE_ADAPTERS[provider][role])
    return provider_adapter


class Message(core.MessageBase[base_models.ContentBlock]):
    blocks: Sequence[Sequence[base_models.ContentBlock]]

    def to_message_params(
        self, provider: Provider, context: MessageContext | dict | None
    ) -> (
        Sequence[AnthropicMessagesParam]
        | Sequence[OpenAIChatMessagesParam]
        | Sequence[GoogleMessagesParam]
    ):
        adapter = cast(ProviderAdapter, get_provider_role_adapter(provider, self.role))
        if context is None:
            context = MessageContext.create_empty()
        elif isinstance(context, dict):
            context = MessageContext.from_variables(context)
        return adapter.to_message_params(self.blocks, context=context)

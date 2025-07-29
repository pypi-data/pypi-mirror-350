from typing import Literal, overload

from moxn.base_models.blocks.base import ToProviderContentBlockMixin
from moxn.base_models.blocks.context import MessageContext
from moxn_types.blocks.text import TextContentModel
from moxn_types.content import Provider
from moxn_types.type_aliases.anthropic import AnthropicTextBlockParam
from moxn_types.type_aliases.google import GooglePart
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatCompletionContentPartTextParam,
)


class ToProviderContentBlockMixinTextOnly(
    ToProviderContentBlockMixin
):  # Override the to_provider_content_block method with more specific types
    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.ANTHROPIC], context: MessageContext
    ) -> AnthropicTextBlockParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.OPENAI_CHAT], context: MessageContext
    ) -> OpenAIChatCompletionContentPartTextParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.GOOGLE_GEMINI], context: MessageContext
    ) -> GooglePart: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.GOOGLE_VERTEX], context: MessageContext
    ) -> GooglePart: ...

    # Implement the method (same as in parent class)
    def to_provider_content_block(self, provider: Provider, context: MessageContext):
        if provider == Provider.ANTHROPIC:
            return self._to_anthropic_content_block(context)
        elif provider == Provider.OPENAI_CHAT:
            return self._to_openai_chat_content_block(context)
        elif provider == Provider.GOOGLE_GEMINI:
            return self._to_google_gemini_content_block(context)
        elif provider == Provider.GOOGLE_VERTEX:
            return self._to_google_vertex_content_block(context)
        else:
            raise ValueError("Unsupported provider")

    def _to_anthropic_content_block(
        self, context: MessageContext
    ) -> AnthropicTextBlockParam:
        raise NotImplementedError

    def _to_openai_chat_content_block(
        self, context: MessageContext
    ) -> OpenAIChatCompletionContentPartTextParam:
        raise NotImplementedError

    def _to_google_gemini_content_block(self, context: MessageContext) -> GooglePart:
        raise NotImplementedError

    def _to_google_vertex_content_block(self, context: MessageContext) -> GooglePart:
        raise NotImplementedError


class TextContent(TextContentModel, ToProviderContentBlockMixinTextOnly):
    """Text content block."""

    text: str

    def _to_anthropic_content_block(
        self, context: MessageContext
    ) -> AnthropicTextBlockParam:
        return AnthropicTextBlockParam(type="text", text=self.text)

    def _to_openai_chat_content_block(
        self, context: MessageContext
    ) -> OpenAIChatCompletionContentPartTextParam:
        return OpenAIChatCompletionContentPartTextParam(type="text", text=self.text)

    def _to_google_gemini_content_block(self, context: MessageContext) -> GooglePart:
        return GooglePart.from_text(text=self.text)

    def _to_google_vertex_content_block(self, context: MessageContext) -> GooglePart:
        return GooglePart.from_text(text=self.text)

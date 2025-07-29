from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from moxn.base_models.blocks.context import MessageContext
from moxn.models import message as msg
from moxn.models.response import LLMEvent, ParsedResponse
from moxn_types import core
from moxn_types.content import Provider
from moxn_types.core import RenderableModel

from .content import PromptContent
from .conversion import MessageConverter
from .core import PromptTemplate
from .response_handler import ResponseHandler


class PromptSession(BaseModel):
    """Manages the runtime state and operations for a prompt execution."""

    id: UUID = Field(default_factory=uuid4)
    prompt: PromptTemplate
    content: PromptContent
    session_data: core.RenderableModel | None = None
    render_kwargs: dict[str, Any] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def prompt_id(self) -> UUID:
        return self.prompt.id

    @property
    def prompt_version_id(self) -> UUID:
        return self.prompt.version_id

    @property
    def messages(self) -> list[msg.Message]:
        return self.content.messages

    @classmethod
    def from_prompt_template(
        cls,
        prompt: PromptTemplate,
        session_data: core.RenderableModel | None = None,
        render_kwargs: dict[str, Any] | None = None,
        message_names: list[str] | None = None,
        messages: list[msg.Message] | None = None,
    ) -> "PromptSession":
        """Create a PromptSession from a base Prompt."""
        if message_names and messages:
            raise ValueError("Cannot specify both message_names and messages")

        selected_messages = prompt._get_selected_messages(message_names, messages)
        return cls(
            prompt=prompt,
            content=PromptContent(messages=selected_messages),
            session_data=session_data,
            render_kwargs=render_kwargs or {},
        )

    def to_message_params(
        self,
        provider: Provider,
        context: MessageContext | dict | None = None,
    ) -> Any:
        """Convert current state to provider-specific messages."""
        if provider == Provider.ANTHROPIC:
            return MessageConverter.to_message_params(
                self.messages,
                provider,
                context,
            )
        elif provider == Provider.OPENAI_CHAT:
            return MessageConverter.to_message_params(
                self.messages,
                provider,
                context,
            )
        elif provider == Provider.GOOGLE_GEMINI:
            return MessageConverter.to_message_params(
                self.messages,
                provider,
                context,
            )
        elif provider == Provider.GOOGLE_VERTEX:
            return MessageConverter.to_message_params(
                self.messages,
                provider,
                context,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def parse_provider_response(
        self,
        response: Any,
        provider: Provider,
    ) -> ParsedResponse:
        """Parse a provider response into a normalized format."""
        if provider == Provider.ANTHROPIC:
            return ResponseHandler.parse_provider_response(response, provider)
        elif provider == Provider.OPENAI_CHAT:
            return ResponseHandler.parse_provider_response(response, provider)
        elif provider == Provider.GOOGLE_GEMINI:
            return ResponseHandler.parse_provider_response(response, provider)
        elif provider == Provider.GOOGLE_VERTEX:
            return ResponseHandler.parse_provider_response(response, provider)

    def create_event(
        self,
        parsed_response: ParsedResponse,
        attributes: dict[str, Any] | None = None,
    ) -> LLMEvent:
        """Create an LLM event from the current session state."""
        return create_llm_event(
            self.messages,
            parsed_response,
            self.session_data,
            self.render_kwargs,
            attributes,
        )


def create_llm_event(
    messages: list,
    parsed_response: ParsedResponse,
    session_data: RenderableModel | None = None,
    render_kwargs: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> LLMEvent:
    """Create an LLM event from messages and parsed response."""
    return LLMEvent(
        messages=[message.model_copy(deep=True) for message in messages],
        provider=parsed_response.provider,
        raw_response=parsed_response.raw_response or {},
        parsed_response=parsed_response,
        session_data=session_data,
        rendered_input=session_data.render(**render_kwargs)
        if session_data and render_kwargs
        else None,
        attributes=attributes,
    )

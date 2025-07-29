"""
Module for parsing and normalizing LLM responses across different providers.
"""

import json
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Type, cast, overload
from uuid import uuid4

from httpx._types import ResponseContent
from pydantic import ConfigDict

from moxn.base_models.blocks.text import TextContent
from moxn.base_models.blocks.tool import ToolCall
from moxn_types.content import Provider
from moxn_types.response import (
    ParsedResponseCandidateModelBase,
    ParsedResponseModelBase,
    ResponseMetadata,
    ResponseParserProtocol,
    StopReason,
    TokenUsage,
)
from moxn_types.telemetry import LLMEventModelBase
from moxn_types.type_aliases.anthropic import (
    AnthropicContentBlock,
    AnthropicMessage,
    AnthropicToolUseBlock,
)
from moxn_types.type_aliases.google import (
    GoogleGenerateContentResponse,
    GoogleGenerateContentResponseCandidate,
)
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatCompletion,
)

if TYPE_CHECKING:
    from moxn.models.message import Message
else:
    Message = Any


class ParsedResponseCandidate(ParsedResponseCandidateModelBase[TextContent, ToolCall]):
    content_blocks: list[TextContent | ToolCall]
    metadata: ResponseMetadata


class ParsedResponse(ParsedResponseModelBase[ParsedResponseCandidate]):
    """
    Normalized response content from any LLM provider.

    Contains parsed content blocks, metadata, and original response for reference.
    """

    candidates: list[ParsedResponseCandidate]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ResponseParserAnthropic(ResponseParserProtocol[AnthropicMessage, ParsedResponse]):
    """Parser for Anthropic Claude responses."""

    @staticmethod
    def parse_candidate(
        response_content: list[AnthropicContentBlock | AnthropicToolUseBlock],
        stop_reason: StopReason,
        raw_stop_reason: str | None,
    ) -> ParsedResponseCandidate:
        """Parse a single Anthropic response candidate."""
        content_blocks: list[TextContent | ToolCall] = []

        # Parse content blocks
        if ResponseContent:
            for block in response_content:
                if block.type == "text" and block.text:
                    text_block = TextContent(text=block.text)
                    content_blocks.append(text_block)
                elif (
                    block.type == "tool_use"
                    and isinstance(block, AnthropicToolUseBlock)
                    and block.id
                    and block.name
                    and block.input
                ):
                    # Anthropic arguments are already a dict
                    tool_call = ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=cast(str | dict[str, Any] | None, block.input),
                    )
                    content_blocks.append(tool_call)

        return ParsedResponseCandidate(
            content_blocks=content_blocks,
            metadata=ResponseMetadata(
                normalized_finish_reason=stop_reason,
                raw_finish_reason=raw_stop_reason or "",
            ),
        )

    @classmethod
    def parse_response(
        cls, response: AnthropicMessage, provider: Provider = Provider.ANTHROPIC
    ) -> ParsedResponse:
        """Parse an Anthropic response into a normalized format."""
        stop_reason = StopReason.END_TURN
        raw_stop_reason = response.stop_reason

        # Anthropic stop reasons: ["end_turn", "max_tokens", "stop_sequence", "tool_use"]]
        if response.stop_reason == "end_turn":
            stop_reason = StopReason.END_TURN
        elif response.stop_reason == "tool_use":
            stop_reason = StopReason.TOOL_CALL
        elif response.stop_reason == "max_tokens":
            stop_reason = StopReason.MAX_TOKENS
        elif response.stop_reason == "stop_sequence":
            stop_reason = StopReason.END_TURN
        else:
            stop_reason = StopReason.OTHER

        # Parse candidate (Anthropic has only one candidate)
        candidates = [
            cls.parse_candidate(response.content, stop_reason, raw_stop_reason)
        ]

        # Extract token usage
        usage = TokenUsage(
            input_tokens=response.usage.input_tokens if response.usage else 0,
            completion_tokens=response.usage.output_tokens if response.usage else 0,
        )

        return ParsedResponse(
            provider=provider,
            candidates=candidates,
            stop_reason=stop_reason,
            usage=usage,
            model=response.model,
            raw_response=response.model_dump(by_alias=True, mode="json"),
        )

    @classmethod
    def extract_metadata(cls, response: AnthropicMessage) -> dict[str, Any]:
        """Extract additional metadata from Anthropic response."""
        metadata = {}

        # Add any Anthropic-specific metadata
        if hasattr(response, "id"):
            metadata["anthropic_message_id"] = response.id

        return metadata


class ResponseParserOpenAI(
    ResponseParserProtocol[OpenAIChatCompletion, ParsedResponse]
):
    """Parser for OpenAI responses."""

    @staticmethod
    def parse_candidate(message, finish_reason) -> ParsedResponseCandidate:
        """Parse a single OpenAI response candidate."""
        content_blocks: list[TextContent | ToolCall] = []

        # Map OpenAI stop reasons to our normalized format
        if finish_reason == "stop":
            stop_reason = StopReason.END_TURN
        elif finish_reason == "length":
            stop_reason = StopReason.MAX_TOKENS
        elif finish_reason in ("tool_calls", "function_call"):
            stop_reason = StopReason.TOOL_CALL
        elif finish_reason == "content_filter":
            stop_reason = StopReason.CONTENT_FILTER
        else:
            stop_reason = StopReason.OTHER

        # Parse content
        if message.content:
            content_blocks.append(TextContent(text=message.content))

        # Parse tool calls
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # OpenAI tool calls have arguments as a string that needs to be parsed
                args = tool_call.function.arguments
                try:
                    # Convert string arguments to dict
                    args_dict = json.loads(args) if isinstance(args, str) else args
                except json.JSONDecodeError:
                    args_dict = {"raw_arguments": args}

                tool_call_obj = ToolCall(
                    id=tool_call.id, name=tool_call.function.name, arguments=args_dict
                )
                content_blocks.append(tool_call_obj)

        return ParsedResponseCandidate(
            content_blocks=content_blocks,
            metadata=ResponseMetadata(
                normalized_finish_reason=stop_reason, raw_finish_reason=finish_reason
            ),
        )

    @classmethod
    def parse_response(
        cls, response: OpenAIChatCompletion, provider: Provider = Provider.OPENAI_CHAT
    ) -> ParsedResponse:
        """Parse an OpenAI response into a normalized format."""
        candidates: list[ParsedResponseCandidate] = []

        # Get the choices from the response
        if not response.choices:
            return ParsedResponse(
                provider=provider,
                candidates=[],
                stop_reason=StopReason.ERROR,
                raw_response=response.model_dump(by_alias=True, mode="json"),
            )

        # Parse each choice as a candidate
        for choice in response.choices:
            candidates.append(cls.parse_candidate(choice.message, choice.finish_reason))

        # Extract token usage
        usage = TokenUsage(
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
        )

        # Use the first candidate's stop reason for the overall response
        stop_reason = (
            candidates[0].metadata.normalized_finish_reason
            if candidates
            else StopReason.ERROR
        )

        return ParsedResponse(
            provider=provider,
            candidates=candidates,
            stop_reason=stop_reason,
            usage=usage,
            model=response.model,
            raw_response=response.model_dump(by_alias=True, mode="json"),
        )

    @classmethod
    def extract_metadata(cls, response: OpenAIChatCompletion) -> dict[str, Any]:
        """Extract additional metadata from OpenAI response."""
        metadata = {}

        # Add any OpenAI-specific metadata
        if response.id:
            metadata["openai_completion_id"] = response.id

        # Add system fingerprint if available
        if response.system_fingerprint:
            metadata["system_fingerprint"] = response.system_fingerprint

        return metadata


class ResponseParserGoogle(
    ResponseParserProtocol[GoogleGenerateContentResponse, ParsedResponse]
):
    """Parser for Google Gemini and Vertex responses."""

    @staticmethod
    def parse_candidate(
        candidate: GoogleGenerateContentResponseCandidate,
    ) -> ParsedResponseCandidate:
        content_blocks: list[TextContent | ToolCall] = []
        finish_reason = (
            candidate.finish_reason.value.upper() if candidate.finish_reason else ""
        )
        if "STOP" in finish_reason:
            stop_reason = StopReason.END_TURN
        elif "MAX_TOKENS" in finish_reason:
            stop_reason = StopReason.MAX_TOKENS
        elif "SAFETY" in finish_reason or "BLOCK" in finish_reason:
            stop_reason = StopReason.CONTENT_FILTER
        elif "RECITATION" in finish_reason:
            stop_reason = StopReason.ERROR
        else:
            stop_reason = StopReason.OTHER

        # Parse content
        content = candidate.content
        if content:
            if content.parts:
                # Extract text from parts
                for part in content.parts:
                    if part.text:
                        text_content = TextContent(text=part.text)
                        content_blocks.append(text_content)
                    if part.function_call:
                        name = part.function_call.name
                        if not name:
                            raise ValueError("Tool call name is required")
                        # Google's args are already a dict
                        args = part.function_call.args

                        tool_call = ToolCall(
                            id=str(
                                uuid4()
                            ),  # Generate a unique ID as Google doesn't provide one
                            name=name,
                            arguments=args,
                        )
                        content_blocks.append(tool_call)

        return ParsedResponseCandidate(
            content_blocks=content_blocks,
            metadata=ResponseMetadata(
                normalized_finish_reason=stop_reason, raw_finish_reason=finish_reason
            ),
        )

    @classmethod
    def parse_response(
        cls, response: GoogleGenerateContentResponse, provider: Provider
    ) -> ParsedResponse:
        """Parse a Google response into a normalized format."""
        # Ensure we have candidates
        if not response.candidates:
            return ParsedResponse(
                provider=provider,
                candidates=[],
                stop_reason=StopReason.ERROR,
                raw_response=response.model_dump(by_alias=True, mode="json"),
            )

        # Parse each candidate
        parsed_candidates = [
            cls.parse_candidate(candidate) for candidate in response.candidates
        ]

        # Extract token usage
        usage_metadata = response.usage_metadata
        if usage_metadata:
            prompt_tokens = usage_metadata.prompt_token_count or 0
            completion_tokens = usage_metadata.candidates_token_count or 0

            usage = TokenUsage(
                input_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        else:
            usage = TokenUsage()
        model = response.model_version

        return ParsedResponse(
            provider=provider,
            candidates=parsed_candidates,
            stop_reason=parsed_candidates[0].metadata.normalized_finish_reason,
            usage=usage,
            model=model,
            raw_response=response.model_dump(by_alias=True, mode="json"),
        )

    @classmethod
    def extract_metadata(
        cls, response: GoogleGenerateContentResponse
    ) -> dict[str, Any]:
        """Extract additional metadata from Google response."""
        metadata = {}

        # Add safety ratings if available
        if response.candidates:
            candidate = response.candidates[0]
            if candidate.safety_ratings:
                metadata["safety_ratings"] = candidate.safety_ratings

        return metadata


class ResponseParser:
    """
    Factory class to parse LLM responses based on provider type.

    Handles normalization of responses from different providers into
    a consistent ParsedResponse format.
    """

    _parsers: ClassVar[dict[Provider, Type[ResponseParserProtocol]]] = {
        Provider.ANTHROPIC: ResponseParserAnthropic,
        Provider.OPENAI_CHAT: ResponseParserOpenAI,
        Provider.GOOGLE_GEMINI: ResponseParserGoogle,
        Provider.GOOGLE_VERTEX: ResponseParserGoogle,
    }

    @classmethod
    def get_parser(cls, provider: Provider) -> ResponseParserProtocol:
        """Get the parser for a given provider."""
        if provider == Provider.ANTHROPIC:
            return cls._parsers[Provider.ANTHROPIC]
        elif provider == Provider.OPENAI_CHAT:
            return cls._parsers[Provider.OPENAI_CHAT]
        elif provider == Provider.GOOGLE_GEMINI:
            return cls._parsers[Provider.GOOGLE_GEMINI]
        elif provider == Provider.GOOGLE_VERTEX:
            return cls._parsers[Provider.GOOGLE_VERTEX]
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @classmethod
    @overload
    def parse(
        cls, response: AnthropicMessage, provider: Literal[Provider.ANTHROPIC]
    ) -> ParsedResponse: ...

    @classmethod
    @overload
    def parse(
        cls, response: OpenAIChatCompletion, provider: Literal[Provider.OPENAI_CHAT]
    ) -> ParsedResponse: ...

    @classmethod
    @overload
    def parse(
        cls,
        response: GoogleGenerateContentResponse,
        provider: Literal[Provider.GOOGLE_GEMINI],
    ) -> ParsedResponse: ...

    @classmethod
    @overload
    def parse(
        cls,
        response: GoogleGenerateContentResponse,
        provider: Literal[Provider.GOOGLE_VERTEX],
    ) -> ParsedResponse: ...

    @classmethod
    def parse(cls, response: Any, provider: Provider) -> ParsedResponse:
        """
        Parse an LLM response based on provider type.

        Args:
            response: The raw response from the provider
            provider: The provider type

        Returns:
            A normalized ParsedResponse object
        """
        if provider not in cls._parsers:
            raise ValueError(f"Unsupported provider: {provider}")

        parser = cls._parsers[provider]
        return parser.parse_response(response, provider)


class ResponseMetadataExtractor:
    """Utility class to extract and format response metadata for telemetry."""

    @staticmethod
    def extract_for_telemetry(parsed_response: ParsedResponse) -> dict[str, Any]:
        """
        Extract metadata from a parsed response for telemetry purposes.

        Args:
            parsed_response: The normalized parsed response

        Returns:
            A dictionary of metadata suitable for telemetry
        """
        metadata = {
            "provider": parsed_response.provider.value,
            "model": parsed_response.model,
            "stop_reason": parsed_response.stop_reason.value,
            "usage": parsed_response.usage.model_dump(),
        }

        return metadata


class LLMEvent(LLMEventModelBase[ParsedResponse, Message]):
    """Domain model for LLM interactions"""

    messages: list[Message]
    parsed_response: ParsedResponse

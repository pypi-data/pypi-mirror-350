from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, Sequence, TypeVar, cast, overload

from moxn.base_models.blocks.text import TextContent
from moxn.base_models.blocks.variable import TextVariable
from moxn.base_models.content_block import ContentBlock
from moxn_types.blocks.variable import VariableFormat
from moxn_types.content import MessageRole, Provider
from moxn_types.type_aliases.anthropic import (
    AnthropicContentBlockParam,
    AnthropicContentBlockParamSequence,
    AnthropicSystemContentBlockParamSequence,
    AnthropicTextBlockParam,  # This replaces TextBlockParam for Anthropic
)
from moxn_types.type_aliases.google import (
    GoogleContentBlock,
    GoogleContentBlockSequence,
    GooglePart,
)
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatCompletionContentPartTextParam,  # OpenAI's text parameter type
    OpenAIChatContentBlock,
    OpenAIChatContentBlockSequence,
)

# Type variable for generic BlockPair
T = TypeVar(
    "T", bound=AnthropicContentBlockParam | OpenAIChatContentBlock | GoogleContentBlock
)


@dataclass
class BlockPair(Generic[T]):
    """
    Utility class for storing an original content block paired with its
    provider-specific representation for inline variable reduction.
    """

    original_block: ContentBlock
    provider_block: T

    @property
    def is_inline_variable(self) -> bool:
        """Whether this block pair contains an inline variable."""
        return (
            isinstance(self.original_block, TextVariable)
            and self.original_block.format == VariableFormat.INLINE
        )

    @property
    def is_static_content(self) -> bool:
        return isinstance(self.original_block, TextContent)

    @property
    def is_inline_variable_or_static_content(self) -> bool:
        return self.is_inline_variable or self.is_static_content


def create_provider_block_pairs(
    block_groups: Sequence[
        Sequence[ContentBlock] | Sequence[TextContent | TextVariable]
    ],
    provider_block_groups: AnthropicSystemContentBlockParamSequence
    | AnthropicContentBlockParamSequence
    | OpenAIChatContentBlockSequence
    | GoogleContentBlockSequence,
) -> Sequence[Sequence[BlockPair]]:
    """
    Creates paired blocks by matching original content blocks with their provider-specific representations.

    Args:
        block_groups: The original content blocks
        provider_block_groups: The provider-specific blocks

    Returns:
        A sequence of sequences of paired blocks
    """
    if len(block_groups) != len(provider_block_groups):
        raise ValueError(
            f"Group count mismatch: {len(block_groups)} block groups vs {len(provider_block_groups)} provider groups"
        )

    paired_groups = []
    for block_group, provider_block_group in zip(block_groups, provider_block_groups):
        if len(block_group) != len(provider_block_group):
            raise ValueError(
                f"Block count mismatch: {len(block_group)} blocks vs {len(provider_block_group)} provider blocks"
            )

        pairs = [
            BlockPair(original_block=block, provider_block=provider_block)
            for block, provider_block in zip(block_group, provider_block_group)
        ]
        paired_groups.append(pairs)

    return paired_groups


# -------------------- Anthropic Inline Variable Reducer -------------------- #


def reduce_inline_variable_blocks_anthropic_system(
    block_pairs: Sequence[BlockPair[AnthropicContentBlockParam]],
) -> Sequence[AnthropicContentBlockParam]:
    """
    Reduces a group of Anthropic system blocks by collating sequential text blocks.

    Args:
        block_pairs: List of paired blocks

    Returns:
        A list of reduced Anthropic blocks
    """
    # Same rules apply to system messages as regular Anthropic messages
    return reduce_inline_variable_blocks_anthropic(block_pairs)


def reduce_inline_variable_blocks_anthropic(
    block_pairs: Sequence[BlockPair[AnthropicContentBlockParam]],
) -> Sequence[AnthropicContentBlockParam]:
    """
    Reduces a group of Anthropic blocks by collating sequential text blocks.

    Args:
        block_pairs: List of paired blocks

    Returns:
        A list of reduced Anthropic blocks
    """
    if not block_pairs:
        return []

    if len(block_pairs) == 1:
        return [block_pairs[0].provider_block]

    # Check that all sub node blocks are TextVariable or TextContent
    if not all(pair.is_inline_variable_or_static_content for pair in block_pairs):
        raise ValueError(
            "All sub node blocks must be Inline TextVariable or TextContent"
        )

    reduced: list[AnthropicTextBlockParam] = []
    in_inline_variable_scope = False

    for pair in block_pairs:
        provider_block = pair.provider_block

        assert isinstance(provider_block, dict) and "text" in provider_block
        if not pair.is_inline_variable and not in_inline_variable_scope:
            in_inline_variable_scope = False
            reduced.append(cast(AnthropicTextBlockParam, provider_block))

        elif not pair.is_inline_variable and in_inline_variable_scope and reduced:
            in_inline_variable_scope = False
            reduced[-1]["text"] += cast(AnthropicTextBlockParam, provider_block)["text"]

        elif pair.is_inline_variable and in_inline_variable_scope:
            raise ValueError("In scope inline variable block should already exist")

        elif pair.is_inline_variable and reduced:
            in_inline_variable_scope = True
            reduced[-1]["text"] += cast(AnthropicTextBlockParam, provider_block)["text"]

        elif pair.is_inline_variable:
            in_inline_variable_scope = True
            reduced.append(cast(AnthropicTextBlockParam, provider_block))
        else:
            raise ValueError("Text block shape invalid")

    return reduced


# -------------------- OpenAI Reducer -------------------- #


def reduce_inline_variable_blocks_openai_chat(
    block_pairs: Sequence[BlockPair[OpenAIChatContentBlock]],
) -> Sequence[OpenAIChatContentBlock]:
    """
    Reduces a group of OpenAI blocks by collating sequential text blocks.

    Args:
        block_pairs: List of paired blocks

    Returns:
        A list of reduced OpenAI blocks
    """
    if not block_pairs:
        return []

    if len(block_pairs) == 1:
        return [block_pairs[0].provider_block]

    # Check that all sub node blocks are TextVariable or TextContent
    if not all(pair.is_inline_variable_or_static_content for pair in block_pairs):
        raise ValueError(
            "All sub node blocks must be Inline TextVariable or TextContent"
        )

    reduced: list[OpenAIChatCompletionContentPartTextParam] = []
    in_inline_variable_scope = False

    for pair in block_pairs:
        provider_block = pair.provider_block

        assert isinstance(provider_block, dict) and provider_block.get("type") == "text"
        if not pair.is_inline_variable and not in_inline_variable_scope:
            # Regular text block outside inline scope
            in_inline_variable_scope = False
            reduced.append(
                cast(OpenAIChatCompletionContentPartTextParam, provider_block)
            )

        elif not pair.is_inline_variable and in_inline_variable_scope and reduced:
            # Regular text after inline variable - append to previous block
            in_inline_variable_scope = False
            reduced[-1]["text"] += cast(
                OpenAIChatCompletionContentPartTextParam, provider_block
            )["text"]

        elif pair.is_inline_variable and in_inline_variable_scope:
            raise ValueError("In scope inline variable block should already exist")

        elif pair.is_inline_variable and reduced:
            # Inline variable with preceding text - append to previous block
            in_inline_variable_scope = True
            reduced[-1]["text"] += cast(
                OpenAIChatCompletionContentPartTextParam, provider_block
            )["text"]

        elif pair.is_inline_variable:
            # First block is inline variable
            in_inline_variable_scope = True
            text_content = cast(
                OpenAIChatCompletionContentPartTextParam, provider_block
            )
            reduced.append(text_content)
        else:
            raise ValueError("Text block shape invalid")

    return reduced


# -------------------- Google Gemini/Vertex Inline Variable Reducer -------------------- #


def reduce_google_inline_variable_block_group(
    block_pairs: Sequence[BlockPair[GoogleContentBlock]],
) -> Sequence[GoogleContentBlock]:
    """
    Reduces a group of Google Gemini/Vertex blocks by collating sequential text blocks.

    Args:
        block_pairs: List of paired blocks

    Returns:
        A list of reduced Google blocks
    """
    if not block_pairs:
        return []

    if len(block_pairs) == 1:
        return [block_pairs[0].provider_block]

    # Check that all sub node blocks are TextVariable or TextContent
    if not all(pair.is_inline_variable_or_static_content for pair in block_pairs):
        raise ValueError(
            "All sub node blocks must be Inline TextVariable or TextContent"
        )

    reduced: list[GooglePart] = []
    in_inline_variable_scope = False

    for pair in block_pairs:
        provider_block = pair.provider_block
        assert (
            isinstance(provider_block, GooglePart) and provider_block.text is not None
        )

        if not pair.is_inline_variable and not in_inline_variable_scope:
            # Regular text block outside inline scope
            in_inline_variable_scope = False
            reduced.append(provider_block)

        elif not pair.is_inline_variable and in_inline_variable_scope and reduced:
            # Regular text after inline variable - append to previous block
            in_inline_variable_scope = False
            # Create new part with combined text
            if not isinstance(reduced[-1].text, str):
                raise ValueError("Previous block is not a text block")
            text_content = reduced[-1].text
            reduced[-1] = GooglePart.from_text(text=text_content + provider_block.text)

        elif pair.is_inline_variable and in_inline_variable_scope:
            raise ValueError("In scope inline variable block should already exist")

        elif pair.is_inline_variable and reduced:
            # Inline variable with preceding text - append to previous block
            in_inline_variable_scope = True
            # Create new part with combined text
            if not isinstance(reduced[-1].text, str):
                raise ValueError("Previous block is not a text block")
            text_content = reduced[-1].text
            reduced[-1] = GooglePart.from_text(text=text_content + provider_block.text)

        elif pair.is_inline_variable:
            # First block is inline variable
            in_inline_variable_scope = True
            reduced.append(provider_block)
        else:
            raise ValueError("Text block shape invalid")

    return reduced


# -------------------- Main Reducer Function -------------------- #


@overload
def reduce_inline_variable_blocks(
    provider: Literal[Provider.ANTHROPIC],
    block_groups: Sequence[Sequence[TextContent | TextVariable]],
    provider_block_groups: AnthropicSystemContentBlockParamSequence,
    role: Literal[MessageRole.SYSTEM],
) -> AnthropicSystemContentBlockParamSequence: ...


@overload
def reduce_inline_variable_blocks(
    provider: Literal[Provider.ANTHROPIC],
    block_groups: Sequence[Sequence[ContentBlock]],
    provider_block_groups: AnthropicContentBlockParamSequence,
    role: MessageRole,
) -> AnthropicContentBlockParamSequence: ...


@overload
def reduce_inline_variable_blocks(
    provider: Literal[Provider.OPENAI_CHAT],
    block_groups: Sequence[Sequence[ContentBlock]],
    provider_block_groups: OpenAIChatContentBlockSequence,
    role: Literal[MessageRole.DEVELOPER],
) -> OpenAIChatContentBlockSequence: ...


@overload
def reduce_inline_variable_blocks(
    provider: Literal[Provider.OPENAI_CHAT],
    block_groups: Sequence[Sequence[ContentBlock]],
    provider_block_groups: OpenAIChatContentBlockSequence,
    role: MessageRole,
) -> OpenAIChatContentBlockSequence: ...


@overload
def reduce_inline_variable_blocks(
    provider: Literal[Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX],
    block_groups: Sequence[Sequence[ContentBlock]],
    provider_block_groups: GoogleContentBlockSequence,
    role: MessageRole,
) -> GoogleContentBlockSequence: ...


def reduce_inline_variable_blocks(
    provider: Provider,
    block_groups: Sequence[
        Sequence[ContentBlock] | Sequence[TextContent | TextVariable]
    ],
    provider_block_groups: AnthropicSystemContentBlockParamSequence
    | AnthropicContentBlockParamSequence
    | OpenAIChatContentBlockSequence
    | GoogleContentBlockSequence,
    role: MessageRole,
) -> (
    AnthropicSystemContentBlockParamSequence
    | AnthropicContentBlockParamSequence
    | OpenAIChatContentBlockSequence
    | GoogleContentBlockSequence
):
    """
    Reduces blocks by provider type, collating sequential text and inline variable blocks.

    This function focuses solely on collating inline variables within document nodes.

    Args:
        provider: The provider to format for
        block_groups: The original content blocks
        provider_block_groups: The provider-specific blocks
        role: The role of the message containing these blocks

    Returns:
        A list of lists of reduced provider-specific blocks
    """
    # Create paired blocks
    paired_groups = create_provider_block_pairs(block_groups, provider_block_groups)

    # Select the appropriate reducer function based on provider
    if provider == Provider.ANTHROPIC:
        if role == MessageRole.SYSTEM:
            return [
                reduce_inline_variable_blocks_anthropic_system(
                    cast(Sequence[BlockPair[AnthropicContentBlockParam]], group)
                )
                for group in paired_groups
            ]
        else:
            return [
                reduce_inline_variable_blocks_anthropic(
                    cast(Sequence[BlockPair[AnthropicContentBlockParam]], group)
                )
                for group in paired_groups
            ]
    elif provider == Provider.OPENAI_CHAT:
        return [
            reduce_inline_variable_blocks_openai_chat(
                cast(Sequence[BlockPair[OpenAIChatContentBlock]], group)
            )
            for group in paired_groups
        ]
    elif provider in (Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX):
        return [
            reduce_google_inline_variable_block_group(
                cast(Sequence[BlockPair[GoogleContentBlock]], group)
            )
            for group in paired_groups
        ]
    else:
        raise ValueError(f"Unsupported provider: {provider}")

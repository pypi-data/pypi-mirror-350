from typing import Literal, Sequence, cast, overload

from anthropic.types import (
    DocumentBlockParam,
    ImageBlockParam,
    TextBlockParam,
)
from anthropic.types import (
    ToolResultBlockParam as AnthropicToolResultBlockParam,
)
from anthropic.types import (
    ToolUseBlockParam as AnthropicToolUseBlockParam,
)
from google.genai import types as google_types
from openai.types.chat.chat_completion_content_part_param import (
    ChatCompletionContentPartParam,
)
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)

from moxn.base_models.blocks.tool import (
    OpenAIChatToolResponseParam,
    OpenAIChatToolUseBlockParam,
)
from moxn_types.content import (
    GOOGLE_GEMINI_CONTENT_MESSAGE_ROLES,
    GOOGLE_GEMINI_MESSAGE_ROLES,
    GOOGLE_VERTEX_CONTENT_MESSAGE_ROLES,
    GOOGLE_VERTEX_MESSAGE_ROLES,
    MessageRole,
    Provider,
)
from moxn_types.type_aliases.anthropic import (
    AnthropicContentBlockParam,
    AnthropicContentBlockParamSequence,
    AnthropicSystemContentBlockParamSequence,
)
from moxn_types.type_aliases.google import (
    GoogleContentBlock,
    GoogleContentBlockSequence,
    GoogleSystemContentBlock,
)
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatContentBlock,
    OpenAIChatContentBlockSequence,
)

# -------------------- Anthropic Document Reducer -------------------- #


def reduce_anthropic_document_block_group(
    provider_blocks: Sequence[
        Sequence[
            TextBlockParam
            | ImageBlockParam
            | DocumentBlockParam
            | AnthropicToolUseBlockParam
            | AnthropicToolResultBlockParam
        ]
    ],
) -> Sequence[
    TextBlockParam
    | ImageBlockParam
    | DocumentBlockParam
    | AnthropicToolUseBlockParam
    | AnthropicToolResultBlockParam
]:
    """
    Reduces a group of Anthropic blocks by collating sequential text blocks.

    Args:
        provider_blocks: The provider-specific blocks

    Returns:
        A flattened list of reduced provider-specific blocks

    Raises:
        ValueError: If a batch contains multiple non-text blocks or a mix of text and non-text blocks
    """
    reduced_blocks: list[
        TextBlockParam
        | ImageBlockParam
        | DocumentBlockParam
        | AnthropicToolUseBlockParam
        | AnthropicToolResultBlockParam
    ] = []

    for batch in provider_blocks:
        if not batch:
            continue

        # Check if this batch has multiple blocks
        if len(batch) > 1:
            # For multiple blocks, they must all be text blocks
            if not all(block["type"] == "text" for block in batch):
                raise ValueError(
                    "Invalid batch structure: multiple blocks in a batch must all be text blocks"
                )

            # Collect all text content and join with newlines
            text_content = "\n\n".join(
                str(block["text"]) for block in batch if block["type"] == "text"
            )
            reduced_blocks.append(TextBlockParam(type="text", text=text_content))
        else:
            # Single block - can be any type
            reduced_blocks.append(batch[0])

    return reduced_blocks


# -------------------- OpenAI Document Reducer -------------------- #


def reduce_openai_chat_document_block_group(
    provider_blocks: Sequence[
        Sequence[
            ChatCompletionContentPartParam
            | OpenAIChatToolUseBlockParam
            | OpenAIChatToolResponseParam
        ]
    ],
) -> Sequence[
    ChatCompletionContentPartParam
    | OpenAIChatToolUseBlockParam
    | OpenAIChatToolResponseParam
]:
    """
    Reduces a group of OpenAI blocks for user or assistant messages.

    Rules:
    1. Neighboring text blocks are collapsed with a `\\n\\n` separator
    2. Non-text blocks are preserved as-is
    3. Any batch with multiple non-text blocks or a mix of text and non-text blocks is invalid

    Args:
        provider_blocks: List of batches of provider blocks

    Returns:
        A flattened list of reduced provider blocks

    Raises:
        ValueError: If a batch contains multiple non-text blocks or a mix of text and non-text blocks
    """
    reduced_blocks: list[
        ChatCompletionContentPartParam
        | OpenAIChatToolUseBlockParam
        | OpenAIChatToolResponseParam
    ] = []

    for batch in provider_blocks:
        if not batch:
            continue

        # Check if this batch has multiple blocks
        if len(batch) > 1:
            # For multiple blocks, they must all be text blocks
            if not all(
                "type" in block and "text" in block and block.get("type") == "text"
                for block in batch
            ):
                raise ValueError(
                    "Invalid batch structure: multiple blocks in a batch must all be text blocks"
                )

            # Collect all text content and join with newlines
            text_content = "\n\n".join(
                str(block.get("text", ""))
                for block in batch
                if "type" in block and "text" in block and block.get("type") == "text"
            )
            reduced_blocks.append(
                ChatCompletionContentPartTextParam(type="text", text=text_content)
            )
        else:
            # Single block - can be any type
            reduced_blocks.append(batch[0])

    return reduced_blocks


def reduce_google_document_block_group(
    provider_blocks: Sequence[
        Sequence[
            google_types.Part
            | google_types.File
            | google_types.FunctionCall
            | google_types.FunctionResponse
        ]
    ],
) -> Sequence[
    google_types.Part
    | google_types.File
    | google_types.FunctionCall
    | google_types.FunctionResponse
]:
    """
    Reduces a group of Google blocks (Gemini or Vertex) for user or assistant messages.

    Rules:
    1. Neighboring text blocks are collapsed with a `\\n\\n` separator
    2. Non-text blocks are preserved as-is
    3. Any batch with multiple non-text blocks or a mix of text and non-text blocks is invalid

    Args:
        provider_blocks: List of batches of provider blocks

    Returns:
        A flattened list of reduced provider blocks

    Raises:
        ValueError: If a batch contains multiple non-text blocks or a mix of text and non-text blocks
    """
    reduced_blocks: list[
        google_types.Part
        | google_types.File
        | google_types.FunctionCall
        | google_types.FunctionResponse
    ] = []

    for batch in provider_blocks:
        if not batch:
            continue

        # Check if this batch has multiple blocks
        if len(batch) > 1:
            # For multiple blocks, they must all be text blocks
            text_blocks = []
            for block in batch:
                # For Google, text blocks have a text attribute that's not None
                if (
                    isinstance(block, google_types.Part)
                    and getattr(block, "text", None) is not None
                ):
                    text_blocks.append(block.text) if block.text is not None else None
                else:
                    raise ValueError(
                        "Invalid batch structure: multiple blocks in a batch must all be text blocks"
                    )

            # Collect all text content and join with newlines
            text_content = "\n\n".join(text_blocks) if text_blocks else ""
            reduced_blocks.append(google_types.Part.from_text(text=text_content))
        else:
            # Single block - can be any type
            reduced_blocks.append(batch[0])

    return reduced_blocks


def reduce_anthropic_system_message(
    provider_blocks: Sequence[
        Sequence[TextBlockParam | ImageBlockParam | DocumentBlockParam]
    ],
) -> Sequence[TextBlockParam]:
    """
    Reduces a group of Anthropic blocks by collating sequential text blocks.
    """
    text_blocks: list[TextBlockParam] = []
    for batch in provider_blocks:
        if not batch:
            continue
        current_text_segments: list[str] = []
        for block in batch:
            if block["type"] == "text":
                current_text_segments.append(block["text"])
            else:
                raise ValueError(f"Unsupported block type: {block}")
        text_blocks.append(
            TextBlockParam(type="text", text="\n\n".join(current_text_segments))
        )
    return text_blocks


def reduce_anthropic_user_or_assistant_message(
    provider_blocks: Sequence[
        Sequence[
            TextBlockParam
            | ImageBlockParam
            | DocumentBlockParam
            | AnthropicToolUseBlockParam
            | AnthropicToolResultBlockParam
        ]
    ],
) -> Sequence[
    TextBlockParam
    | ImageBlockParam
    | DocumentBlockParam
    | AnthropicToolUseBlockParam
    | AnthropicToolResultBlockParam
]:
    """
    Reduces a group of Anthropic blocks for user or assistant messages.

    Rules:
    1. Neighboring text blocks are collapsed with a `\\n\\n` separator
    2. Non-text blocks are preserved as-is
    3. Any batch with multiple non-text blocks or a mix of text and non-text blocks is invalid

    Args:
        provider_blocks: List of batches of provider blocks

    Returns:
        A flattened list of reduced provider blocks

    Raises:
        ValueError: If a batch contains multiple non-text blocks or a mix of text and non-text blocks
    """
    return reduce_anthropic_document_block_group(provider_blocks)


# -------------------- Main Reducer Function -------------------- #


@overload
def reduce_document_blocks(
    provider: Literal[Provider.ANTHROPIC],
    role: Literal[MessageRole.SYSTEM],
    provider_block_groups: AnthropicSystemContentBlockParamSequence,
) -> Sequence[TextBlockParam]: ...


@overload
def reduce_document_blocks(
    provider: Literal[Provider.ANTHROPIC],
    role: Literal[MessageRole.USER, MessageRole.ASSISTANT],
    provider_block_groups: AnthropicContentBlockParamSequence,
) -> Sequence[AnthropicContentBlockParam]: ...


@overload
def reduce_document_blocks(
    provider: Literal[Provider.OPENAI_CHAT],
    role: MessageRole,
    provider_block_groups: OpenAIChatContentBlockSequence,
) -> Sequence[OpenAIChatContentBlock]: ...


@overload
def reduce_document_blocks(
    provider: Literal[Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX],
    role: Literal[MessageRole.SYSTEM],
    provider_block_groups: GoogleContentBlockSequence,
) -> Sequence[GoogleSystemContentBlock]: ...


@overload
def reduce_document_blocks(
    provider: Literal[Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX],
    role: Literal[MessageRole.TOOL_CALL],
    provider_block_groups: GoogleContentBlockSequence,
) -> Sequence[google_types.FunctionCall]: ...


@overload
def reduce_document_blocks(
    provider: Literal[Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX],
    role: MessageRole,
    provider_block_groups: GoogleContentBlockSequence,
) -> Sequence[GoogleContentBlock]: ...


def reduce_document_blocks(
    provider: Provider,
    role: MessageRole,
    provider_block_groups: AnthropicContentBlockParamSequence
    | AnthropicSystemContentBlockParamSequence
    | OpenAIChatContentBlockSequence
    | GoogleContentBlockSequence,
) -> (
    Sequence[AnthropicContentBlockParam]
    | Sequence[OpenAIChatContentBlock]
    | Sequence[GoogleContentBlock]
    | Sequence[TextBlockParam]
):
    """
    Reduces document blocks by provider type and role, producing flat lists
    suitable for sending to LLM providers.

    Args:
        provider: The provider to format for
        role: The message role (system, user, assistant)
        provider_block_groups: The provider-specific blocks

    Returns:
        A flattened list of reduced provider-specific blocks
    """
    if provider == Provider.ANTHROPIC:
        if role == MessageRole.SYSTEM:
            provider_block_groups = cast(
                AnthropicSystemContentBlockParamSequence,
                provider_block_groups,
            )
            return reduce_anthropic_system_message(provider_block_groups)
        else:
            provider_block_groups = cast(
                AnthropicContentBlockParamSequence,
                provider_block_groups,
            )
            return reduce_anthropic_user_or_assistant_message(provider_block_groups)
    elif provider == Provider.OPENAI_CHAT:
        provider_block_groups = cast(
            OpenAIChatContentBlockSequence,
            provider_block_groups,
        )
        return reduce_openai_chat_document_block_group(provider_block_groups)
    elif provider in (Provider.GOOGLE_GEMINI, Provider.GOOGLE_VERTEX):
        provider_block_groups = cast(
            GoogleContentBlockSequence,
            provider_block_groups,
        )
        return reduce_google_document_block_group(provider_block_groups)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _shape_google_content_blocks_system_message(
    provider_blocks: Sequence[
        google_types.Part
        | google_types.File
        | google_types.FunctionCall
        | google_types.FunctionResponse
    ],
) -> str:
    """
    Shapes Google content blocks for a system message.
    """
    text = []
    for block in provider_blocks:
        if isinstance(block, google_types.Part) and block.text is not None:
            text.append(block.text) if block.text is not None else ""
        else:
            raise ValueError(f"Unsupported block type: {block} for system message")
    return "\n\n".join(text)


@overload
def shape_google_content_blocks(
    provider_blocks: Sequence[GoogleContentBlock],
    role: Literal[MessageRole.SYSTEM],
) -> str: ...


@overload
def shape_google_content_blocks(
    provider_blocks: Sequence[GoogleContentBlock],
    role: GOOGLE_GEMINI_CONTENT_MESSAGE_ROLES | GOOGLE_VERTEX_CONTENT_MESSAGE_ROLES,
) -> Sequence[google_types.Content | google_types.File]: ...


def shape_google_content_blocks(
    provider_blocks: Sequence[GoogleContentBlock],
    role: GOOGLE_GEMINI_MESSAGE_ROLES | GOOGLE_VERTEX_MESSAGE_ROLES,
) -> Sequence[google_types.Content | google_types.File] | str:
    """
    Shapes Google content blocks for a system message.
    """
    if role == MessageRole.SYSTEM:
        return _shape_google_content_blocks_system_message(provider_blocks)
    elif role in (
        MessageRole.USER,
        MessageRole.MODEL,
        MessageRole.TOOL_CALL,
        MessageRole.TOOL_RESULT,
    ):
        content: list[google_types.Content | google_types.File] = []
        current_part: list[google_types.Part] = []
        for block in provider_blocks:
            if isinstance(block, google_types.FunctionCall):
                current_part.append(
                    google_types.Part.from_function_call(
                        name=block.name or "",
                        args=block.args or {},
                    )
                )
            elif isinstance(block, google_types.FunctionResponse):
                current_part.append(
                    google_types.Part.from_function_response(
                        name=block.name or "",
                        response=block.response or {},
                    )
                )
            elif isinstance(block, google_types.Part):
                current_part.append(block)
            elif isinstance(block, google_types.File):
                if current_part:
                    content.append(
                        google_types.Content(
                            role=role.value.lower(), parts=current_part
                        )
                    )
                content.append(block)
                current_part = []
            else:
                raise ValueError(f"Unsupported block type: {block} for system message")
        if current_part:
            content.append(
                google_types.Content(role=role.value.lower(), parts=current_part)
            )
        return content
    else:
        raise ValueError(f"Unsupported role: {role}")

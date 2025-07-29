from typing import Sequence

from pydantic import TypeAdapter

from moxn.base_models.blocks.document import PDFContentFromSource
from moxn.base_models.blocks.image import ImageContentFromSource
from moxn.base_models.blocks.signed import (
    SignedURLContent,
    SignedURLImageContent,
    SignedURLPDFContent,
)
from moxn.base_models.blocks.text import TextContent
from moxn.base_models.blocks.tool import ToolCall, ToolResult
from moxn.base_models.blocks.variable import Variable

ContentBlock = (
    TextContent
    | ImageContentFromSource
    | PDFContentFromSource
    | SignedURLContent
    | SignedURLImageContent
    | SignedURLPDFContent
    | Variable
    | ToolCall
    | ToolResult
)

ContentBlockList = Sequence[ContentBlock]
ContentBlockDocument = Sequence[Sequence[ContentBlock]]

ContentBlockAdapter: TypeAdapter[ContentBlock] = TypeAdapter(ContentBlock)

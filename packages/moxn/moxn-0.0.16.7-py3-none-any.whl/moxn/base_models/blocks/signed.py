from datetime import datetime, timedelta, timezone

from moxn.base_models.blocks.base import ToProviderContentBlockMixin
from moxn.base_models.blocks.context import MessageContext
from moxn.base_models.blocks.document import MediaDataPDFFromURL
from moxn.base_models.blocks.image import (
    MediaImageFromURL,
)
from moxn_types.blocks.signed import (
    SignedURLContentModel,
    SignedURLImageContentModel,
    SignedURLPDFContentModel,
)
from moxn_types.type_aliases.anthropic import (
    AnthropicDocumentBlockParam,
    AnthropicImageBlockParam,
)
from moxn_types.type_aliases.google import GooglePart
from moxn_types.type_aliases.openai_chat import (
    OpenAIChatCompletionContentPartImageParam,
    OpenAIChatFile,
)


class SignedURLContent(SignedURLContentModel, ToProviderContentBlockMixin):
    @property
    def url(self) -> str:
        if self.signed_url:
            return self.signed_url
        raise ValueError("URL not set")

    def should_refresh(self) -> bool:
        if self.expiration is None:
            return True

        # Ensure expiration is timezone-aware
        expiration = self._ensure_timezone_aware(self.expiration)
        now = datetime.now(timezone.utc)

        return expiration < now + timedelta(seconds=self.buffer_seconds)

    def _ensure_timezone_aware(self, dt: datetime) -> datetime:
        """Ensure datetime is timezone-aware, converting to UTC if it's naive"""
        if dt.tzinfo is None:
            # Convert naive datetime to UTC
            return dt.replace(tzinfo=timezone.utc)
        return dt


class SignedURLImageContent(SignedURLImageContentModel, SignedURLContent):
    def _to_anthropic_content_block(
        self, context: MessageContext
    ) -> AnthropicImageBlockParam:
        return MediaImageFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_anthropic_content_block(context)

    def _to_openai_chat_content_block(
        self, context: MessageContext
    ) -> OpenAIChatCompletionContentPartImageParam:
        return MediaImageFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_openai_chat_content_block(context)

    def _to_google_gemini_content_block(self, context: MessageContext) -> GooglePart:
        return MediaImageFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_google_gemini_content_block(context)

    def _to_google_vertex_content_block(self, context: MessageContext) -> GooglePart:
        return MediaImageFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_google_vertex_content_block(context)


class SignedURLPDFContent(SignedURLPDFContentModel, SignedURLContent):
    def _to_anthropic_content_block(
        self, context: MessageContext
    ) -> AnthropicDocumentBlockParam:
        return MediaDataPDFFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_anthropic_content_block(context)

    def _to_openai_chat_content_block(self, context: MessageContext) -> OpenAIChatFile:
        return MediaDataPDFFromURL(
            url=self.url,
            media_type=self.media_type,
            filename=self.filename,
        )._to_openai_chat_content_block(context)

    def _to_google_gemini_content_block(self, context: MessageContext) -> GooglePart:
        return MediaDataPDFFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_google_gemini_content_block(context)

    def _to_google_vertex_content_block(self, context: MessageContext) -> GooglePart:
        return MediaDataPDFFromURL(
            url=self.url,
            media_type=self.media_type,
        )._to_google_vertex_content_block(context)

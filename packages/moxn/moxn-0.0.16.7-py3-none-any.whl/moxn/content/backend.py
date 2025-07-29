from __future__ import annotations

import logging
from typing import Protocol

import httpx
from pydantic import BaseModel, HttpUrl, PrivateAttr, SecretStr

from moxn.settings import MoxnSettings, get_moxn_settings
from moxn_types.content import (
    SignedURLContentRequest,
    SignedURLContentResponse,
)

logger = logging.getLogger(__name__)


class ContentBackend(Protocol):
    """Protocol for the backend that handles content API requests"""

    async def get_signed_content_url(
        self, request: SignedURLContentRequest
    ) -> SignedURLContentResponse: ...

    async def get_signed_content_url_batch(
        self, requests: list[SignedURLContentRequest]
    ) -> list[SignedURLContentResponse]: ...

    async def aclose(self) -> None: ...


class HttpContentBackend(BaseModel):
    """
    Concrete implementation that talks to the Moxn API over HTTP
    for content-related operations such as retrieving signed URLs.
    """

    user_id: str
    org_id: str | None = None
    api_key: SecretStr
    base_url: HttpUrl

    timeout: float = get_moxn_settings().timeout

    # HTTP client is not part of the pydantic model, just a PrivateAttr
    _client: httpx.AsyncClient = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        # Create client with base_url and auth headers baked in
        self._client = httpx.AsyncClient(
            base_url=str(self.base_url),
            timeout=self.timeout,
            headers=self.get_headers(),
        )

    @classmethod
    def from_settings(cls, settings: MoxnSettings) -> "HttpContentBackend":
        return cls(
            user_id=settings.user_id,
            org_id=settings.org_id,
            base_url=settings.base_api_route,
            api_key=settings.api_key,
            timeout=settings.timeout,
        )

    def get_headers(self) -> dict[str, str]:
        headers = {
            "x-api-key": self.api_key.get_secret_value(),
            "x-requested-user-id": self.user_id,
        }
        if self.org_id:
            headers["x-requested-org-id"] = self.org_id
        return headers

    # Content API methods

    async def get_signed_content_url(
        self, request: SignedURLContentRequest
    ) -> SignedURLContentResponse:
        """
        Get a signed URL for a content item.

        Args:
            request: The request containing content key and TTL

        Returns:
            Response containing signed URL and expiration time
        """
        try:
            response = await self._client.post(
                "/content/signed-url",
                json=request.model_dump(exclude_none=True, mode="json"),
            )
            response.raise_for_status()
            return SignedURLContentResponse.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting signed content URL: {e}", exc_info=True)
            raise

    async def get_signed_content_url_batch(
        self, requests: list[SignedURLContentRequest]
    ) -> list[SignedURLContentResponse]:
        """
        Get signed URLs for a batch of content items.

        Args:
            requests: List of requests containing content key and TTL

        Returns:
            List of responses containing signed URL and expiration time
        """
        try:
            response = await self._client.post(
                "/content/signed-url-batch",
                json=[
                    item.model_dump(exclude_none=True, mode="json") for item in requests
                ],
            )
            response.raise_for_status()
            return [
                SignedURLContentResponse.model_validate(item)
                for item in response.json()
            ]
        except Exception as e:
            logger.error(f"Error getting signed content URL: {e}", exc_info=True)
            raise

    async def aclose(self) -> None:
        """Properly close the underlying HTTPX client."""
        await self._client.aclose()

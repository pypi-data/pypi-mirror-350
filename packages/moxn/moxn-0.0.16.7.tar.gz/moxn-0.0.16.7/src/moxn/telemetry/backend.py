from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Protocol
from uuid import uuid4

import httpx
from pydantic import BaseModel, HttpUrl, PrivateAttr, SecretStr

from moxn.settings import MoxnSettings, get_moxn_settings
from moxn_types.telemetry import (
    MAX_INLINE_ATTRIBUTES_SIZE,
    SignedURLRequest,
    SignedURLResponse,
    SpanEventLogRequest,
    SpanLogRequest,
    TelemetryLogResponse,
)


class TelemetryTransportBackend(Protocol):
    """Protocol for the backend that handles actual sending of telemetry data"""

    async def send_telemetry_log(
        self, log_request: SpanLogRequest | SpanEventLogRequest
    ) -> TelemetryLogResponse: ...

    async def aclose(self) -> None: ...


class HttpTelemetryBackend(BaseModel):
    """
    Concrete implementation that talks to the Moxn API over HTTP,
    reusing a single AsyncClient for all telemetry posts and
    a second anonymous client for external-attributes PUTs.
    """

    user_id: str
    org_id: str | None = None
    api_key: SecretStr
    base_url: HttpUrl

    timeout: float = get_moxn_settings().telemetry_timeout

    # these clients are not part of the pydantic model, just PrivateAttrs
    _client: httpx.AsyncClient = PrivateAttr()
    _anon_client: httpx.AsyncClient = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        # 1) main client with base_url and auth headers baked in
        self._client = httpx.AsyncClient(
            base_url=str(self.base_url),
            timeout=self.timeout,
            headers=self.get_headers(),
        )
        # 2) anonymous client for external uploads (no base_url, no auth headers)
        self._anon_client = httpx.AsyncClient(timeout=self.timeout)

    @classmethod
    def from_settings(cls, settings: MoxnSettings) -> "HttpTelemetryBackend":
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

    # ---------- public-protocol methods --------------------------------------

    async def send_telemetry_log(
        self, log_request: SpanLogRequest | SpanEventLogRequest
    ) -> TelemetryLogResponse:
        if isinstance(
            log_request, SpanEventLogRequest
        ) and self._should_use_external_storage(log_request.attributes):
            return await self._send_telemetry_log_with_external_attributes(log_request)

        # inline case: use the persistent client with base_url
        resp = await self._client.post(
            "/telemetry/log-event",
            json=log_request.model_dump(exclude_none=True, mode="json", by_alias=True),
        )
        resp.raise_for_status()
        return TelemetryLogResponse.model_validate(resp.json())

    async def _send_telemetry_log_and_get_signed_url(
        self, req: SignedURLRequest
    ) -> SignedURLResponse:
        resp = await self._client.post(
            "/telemetry/log-event-and-get-signed-url",
            json=req.model_dump(exclude_none=True, mode="json", by_alias=True),
        )
        resp.raise_for_status()
        return SignedURLResponse.model_validate(resp.json())

    # ---------- internal helpers ---------------------------------------------

    @staticmethod
    def _should_use_external_storage(attributes: dict) -> bool:
        try:
            return len(json.dumps(attributes)) > MAX_INLINE_ATTRIBUTES_SIZE
        except (TypeError, ValueError):
            return True

    async def _send_telemetry_log_with_external_attributes(
        self, log_request: SpanEventLogRequest
    ) -> TelemetryLogResponse:
        original_attrs = log_request.attributes
        log_request.attributes = {}

        prefix = self.org_id or self.user_id
        file_path = f"{prefix}/{log_request.span_id}/{log_request.span_event_id}.json"

        signed_req = SignedURLRequest(
            file_path=file_path,
            media_type="application/json",
            log_request=log_request,
        )
        signed_resp = await self._send_telemetry_log_and_get_signed_url(signed_req)

        # upload the payload anonymously
        put_resp = await self._anon_client.put(
            signed_resp.url,
            content=json.dumps(original_attrs),
            headers={"Content-Type": "application/json"},
        )
        put_resp.raise_for_status()

        return TelemetryLogResponse(
            id=signed_resp.id or uuid4(),
            message="Successfully logged with external attributes",
            timestamp=datetime.now(timezone.utc),
        )

    async def aclose(self) -> None:
        """Properly close all underlying HTTPX clients."""
        await self._client.aclose()
        await self._anon_client.aclose()

import json
from datetime import datetime
from typing import Protocol
from uuid import uuid4

import httpx

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

    async def send_telemetry_log_and_get_signed_url(
        self, signed_url_request: SignedURLRequest
    ) -> SignedURLResponse: ...


class APITelemetryTransport:
    """Transport that sends telemetry data to the Moxn API, handling large payloads."""

    def __init__(
        self,
        backend: TelemetryTransportBackend,
        user_id: str,
        org_id: str | None = None,
    ):
        self.backend = backend
        self.user_id = user_id
        self.org_id = org_id

    async def send_log(
        self, log_request: SpanLogRequest | SpanEventLogRequest
    ) -> TelemetryLogResponse:
        # Only handle external storage for event logs with large attributes
        if isinstance(
            log_request, SpanEventLogRequest
        ) and self._should_use_external_storage(log_request.attributes):
            return await self._send_log_with_external_attributes(log_request)

        # Standard flow for smaller payloads
        return await self.backend.send_telemetry_log(log_request)

    def _should_use_external_storage(self, attributes: dict) -> bool:
        """Determine if attributes should be stored externally based on size"""
        try:
            serialized = json.dumps(attributes)
            return len(serialized) > MAX_INLINE_ATTRIBUTES_SIZE
        except (TypeError, ValueError):
            # If we can't serialize, assume it's complex/large
            return True

    async def _send_log_with_external_attributes(
        self,
        log_request: SpanEventLogRequest,
    ) -> TelemetryLogResponse:
        """
        Handle a large event log by:
        1) Getting a signed URL (this also creates the DB record),
        2) Uploading the raw attributes to the signed URL.

        The DB record creation happens when getting the signed URL,
        so we don't need a separate call to log an empty event.
        """
        # Store the original attributes
        original_attributes = log_request.attributes
        log_request.attributes = {}

        # Build a file-path prefix using org_id or user_id
        prefix = self.org_id if self.org_id else self.user_id
        file_path = f"{prefix}/{log_request.span_id}/{log_request.span_event_id}.json"

        # Get a signed URL (this also creates the DB record)
        signed_url_request = SignedURLRequest(
            file_path=file_path,
            media_type="application/json",
            log_request=log_request,
        )
        signed_url_response = await self.backend.send_telemetry_log_and_get_signed_url(
            signed_url_request
        )

        # Upload the attributes to the signed URL
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                signed_url_response.url,
                content=json.dumps(original_attributes),
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()

        # Return the response from the signed URL request
        return TelemetryLogResponse(
            id=(
                signed_url_response.id
                if getattr(signed_url_response, "id", None)
                else uuid4()
            ),
            message="Successfully logged with external attributes",
            timestamp=datetime.now(),
        )

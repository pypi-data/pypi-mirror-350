from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from moxn.telemetry.dispatcher import TelemetryDispatcher
from moxn_types.telemetry import (
    SpanEventLogRequest,
    SpanEventLogType,
    SpanKind,
)

# Global context variable to track current span
current_span: ContextVar[Optional["SpanContext"]] = ContextVar(
    "current_span", default=None
)


@dataclass
class SpanContext:
    """Thread-safe context for span management"""

    span_id: UUID
    root_span_id: UUID
    parent_span_id: UUID | None
    name: str
    kind: SpanKind
    prompt_id: UUID
    prompt_version_id: UUID
    start_time: datetime
    attributes: dict[str, Any]
    _transport: TelemetryDispatcher

    @classmethod
    def create_root(
        cls,
        name: str,
        kind: SpanKind,
        prompt_id: UUID,
        prompt_version_id: UUID,
        transport: TelemetryDispatcher,
        attributes: dict[str, Any] | None = None,
    ) -> "SpanContext":
        span_id = uuid4()
        return cls(
            span_id=span_id,
            root_span_id=span_id,
            parent_span_id=None,
            name=name,
            kind=kind,
            prompt_id=prompt_id,
            prompt_version_id=prompt_version_id,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
            _transport=transport,
        )

    def create_child(
        self,
        name: str,
        kind: SpanKind,
        attributes: Optional[dict[str, Any]] = None,
    ) -> "SpanContext":
        return SpanContext(
            span_id=uuid4(),
            root_span_id=self.root_span_id,
            parent_span_id=self.span_id,
            name=name,
            kind=kind,
            prompt_id=self.prompt_id,
            prompt_version_id=self.prompt_version_id,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
            _transport=self._transport,
        )

    async def log_event(
        self,
        message: str,
        metadata: dict[str, Any] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Log a generic event within this span"""
        await self._transport.enqueue(
            SpanEventLogRequest(
                id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                span_id=self.span_id,
                span_event_id=uuid4(),
                event_type=SpanEventLogType.EVENT,
                prompt_id=self.prompt_id,
                prompt_version_id=self.prompt_version_id,
                attributes=attributes or {},
                message=message,
                log_metadata=metadata or {},
            )
        )

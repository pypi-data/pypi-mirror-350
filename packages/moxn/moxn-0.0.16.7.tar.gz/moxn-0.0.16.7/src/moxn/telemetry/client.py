from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from contextvars import Token
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Literal, Optional
from uuid import UUID, uuid4

from moxn.models.prompt import PromptSession
from moxn.models.response import LLMEvent
from moxn.settings import MoxnSettings, get_moxn_settings
from moxn.telemetry.backend import HttpTelemetryBackend, TelemetryTransportBackend
from moxn.telemetry.dispatcher import TelemetryDispatcher
from moxn_types.telemetry import (
    SpanKind,
    SpanLogRequest,
    SpanLogType,
)

from .context import SpanContext, current_span


class TelemetryClient:
    """
    Higher-level façade that tracks spans and delegates *sending* to a backend.
    """

    def __init__(self, backend: TelemetryTransportBackend) -> None:
        self._backend = backend
        # Create the dispatcher, but don't start it yet
        self._dispatcher = TelemetryDispatcher(backend)
        self._started = False

    @classmethod
    def from_settings(cls, settings: MoxnSettings) -> "TelemetryClient":
        backend = HttpTelemetryBackend.from_settings(settings)
        return cls(backend)

    # ------------------------------------------------------------------ #
    # lifecycle helpers (called by top-level client)
    # ------------------------------------------------------------------ #
    async def start(self) -> None:
        """Start the telemetry system with background workers."""
        if not self._started:
            # Start the dispatcher with non-blocking background workers
            await self._dispatcher.start()
            self._started = True

    async def stop(self) -> None:
        """Stop the telemetry system, flush pending items, and clean up resources."""
        if self._started:
            # Try to flush with a timeout first
            try:
                await self._dispatcher.flush(timeout=get_moxn_settings().timeout)
            except asyncio.TimeoutError:
                # Continue with shutdown even if flush times out
                pass

            await self._dispatcher.stop()
            self._started = False

        if hasattr(self._backend, "aclose"):
            await self._backend.aclose()

    # optional sugar so **you** can still do
    #    async with TelemetryClient(…) as tc:
    async def __aenter__(self):  # pragma: no cover
        await self.start()
        return self

    async def __aexit__(self, *_):  # pragma: no cover
        await self.stop()

    # --------------------------------------------------------------------- #
    # Span helpers (unchanged except for backend wiring)
    # --------------------------------------------------------------------- #

    @asynccontextmanager
    async def span(
        self,
        prompt_session: PromptSession,
        name: str | None = None,
        kind: Literal["llm", "tool", "agent"] | SpanKind = "llm",
        attributes: Optional[dict[str, Any]] = None,
    ) -> AsyncGenerator[SpanContext, None]:
        # Make sure telemetry is started if used directly
        if not self._started:
            await self.start()

        if isinstance(kind, str):
            kind = SpanKind(kind)

        parent_context = current_span.get()

        _name: str = prompt_session.prompt.name if name is None else name

        context = (
            parent_context.create_child(_name, kind, attributes)
            if parent_context
            else SpanContext.create_root(
                name=_name,
                kind=kind,
                prompt_id=prompt_session.prompt_id,
                prompt_version_id=prompt_session.prompt_version_id,
                transport=self._dispatcher,
                attributes=attributes,
            )
        )

        await self._log_span_start(context)
        token: Token = current_span.set(context)

        try:
            yield context
        except Exception as exc:
            await self._log_span_error(context, str(exc))
            raise
        finally:
            current_span.reset(token)
            await self._log_span_end(context)

    async def log_event(self, event: LLMEvent, span_id: Optional[UUID] = None) -> None:
        # Make sure telemetry is started if used directly
        if not self._started:
            await self.start()

        context = current_span.get() if span_id is None else None
        if context is None:
            raise RuntimeError(
                f"No active span context found (span_id={span_id!s})"
            )  # pragma: no cover

        await context.log_event(
            message="LLM response received",
            metadata={"event_type": "llm_response"},
            attributes=event.model_dump(mode="json", by_alias=True),
        )

    # ------------------------------------------------------------------ #
    # Internal logging helpers (backend-aware)
    # ------------------------------------------------------------------ #

    async def _log_span_start(self, ctx: SpanContext) -> None:
        attrs = {"span.name": ctx.name, "span.kind": ctx.kind.value, **ctx.attributes}
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=ctx.start_time,
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.START,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=attrs,
                message=f"Started span: {ctx.name}",
            )
        )

    async def _log_span_error(self, ctx: SpanContext, error_msg: str) -> None:
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.ERROR,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=ctx.attributes,
                message=f"Error in span {ctx.name}: {error_msg}",
            )
        )

    async def _log_span_end(self, ctx: SpanContext) -> None:
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.END,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=ctx.attributes,
                message=f"Completed span: {ctx.name}",
            )
        )

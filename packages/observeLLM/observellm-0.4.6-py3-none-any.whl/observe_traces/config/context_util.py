from contextvars import ContextVar

from fastapi import Request
from langfuse.client import StatefulTraceClient

request_context: ContextVar[Request] = ContextVar(
    "request_context", default=None
)
tracer_context: ContextVar[StatefulTraceClient] = ContextVar(
    "tracer_context", default=None
)
request_metadata_context: ContextVar[dict] = ContextVar(
    "request_metadata_context", default={}
)

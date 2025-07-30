import functools
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from observe_traces.config.context_util import request_context
from observe_traces.config.langfuse_service import _LangfuseService


# Price calculators for different vector DB providers
def calculate_pinecone_price(
    operation_type: str, units: int
) -> Dict[str, float]:
    pricing = {
        "read": 16.0,  # $16 per million read units
        "write": 4.0,  # $4 per million write units
    }

    price = (units / 1000000) * pricing[operation_type]

    return {"units": units, "price": price}


# Provider-specific response parsers
def parse_pinecone_write_response(
    response_data: Dict[str, Any],
) -> Dict[str, int]:
    return {
        "operation_type": "write",
        "units": response_data.get("upsertedCount", 0),
    }


def parse_pinecone_read_response(
    response_data: Dict[str, Any],
) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {"operation_type": "read", "units": usage.get("readUnits", 0)}


# Provider configurations
PROVIDER_CONFIGS = {
    "pinecone": {
        "write_parser": parse_pinecone_write_response,
        "read_parser": parse_pinecone_read_response,
        "price_calculator": calculate_pinecone_price,
        "response_extractor": lambda data: [
            {
                "score": match["score"],
                "text": match.get("metadata", {}).get(
                    "text", ""
                ),  # Fallback to empty string if text is not present
                "namespace": data.get("namespace", ""),
            }
            for match in data.get("matches", [])
        ],
    }
    # Add other vector DB providers here as needed
}


def vectordb_tracing(provider: str, operation_type: str):
    """
    Decorator for tracing Vector DB API calls

    Args:
        provider: Name of the vector DB provider (e.g., "pinecone")
        operation_type: Type of operation ("read" or "write")
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Get trace ID from request context
            id = request_context.get()
            trace_id = id

            # Get provider config
            provider_config = PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                return await func(*args, **kwargs)

            start_time = time.perf_counter()

            try:
                result = await func(*args, **kwargs)

                end_time = time.perf_counter()
                response_time = end_time - start_time

                if operation_type == "write":
                    operation_data = provider_config["write_parser"](result)
                else:  # read
                    operation_data = provider_config["read_parser"](result)

                price_data = provider_config["price_calculator"](
                    operation_data["operation_type"], operation_data["units"]
                )

                ist = timezone(timedelta(hours=5, minutes=30))
                pinecone_response = None

                query = None
                namespace = kwargs.get(
                    "project_namespace", kwargs.get("namespace", "")
                )
                index_host = kwargs.get("index_host", "")

                # Extract relevant function arguments for the trace
                # For Pinecone upsert
                if operation_type == "write":
                    index_host = index_host
                    namespace = namespace
                    vectors_count = result.get("upsertedCount", 0)
                    total_vectors = len(kwargs.get("vectors", []))
                    pinecone_response = result
                    operation_details = {
                        "index_host": index_host,
                        "namespace": namespace,
                        "upserted_vectors": vectors_count,
                        "total_vectors": total_vectors,
                    }
                # For Pinecone queries
                elif operation_type == "read":
                    top_k = kwargs.get("max_results", 0)
                    pinecone_response = result.get(
                        "matches", result.get("results", [])
                    )
                    query = kwargs.get("query", "")
                    operation_details = {
                        "index_host": index_host,
                        "namespace": namespace,
                        "top_k": top_k,
                    }
                else:
                    operation_details = {}

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY BELOW ###
                try:
                    span_data = {
                        "service_provider": provider,
                        "operation_type": operation_type,
                        "response": pinecone_response or "",
                        "operation_details": operation_details,
                        "units": operation_data["units"],
                        "price": price_data["price"],
                        "query": query,
                        "start_time": start_time,
                        "end_time": end_time,
                        "response_time": response_time,
                        "timestamp": datetime.now(ist).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }

                    await _LangfuseService.create_span_for_vectorDB(
                        trace_id=trace_id,
                        span_data=span_data,
                        name=f"{provider.capitalize()} {operation_type.capitalize()}",
                    )

                except Exception as e:
                    raise e

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY ABOVE ###
                return result

            except Exception as e:
                raise e

        return wrapper

    return decorator

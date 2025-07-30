import functools
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

from observe_traces.config.context_util import request_context
from observe_traces.config.langfuse_service import _LangfuseService


def calculate_pinecone_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "pinecone-rerank-v0": 0.10,  # Example: $0.10 per 1k rerank units
    }
    rerank_units = tokens_data.get("rerank_units", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (rerank_units / 1000) * model_price
    return {
        "rerank_units": rerank_units,
        "price_per_1K": model_price,
        "total": total_price,
    }


def calculate_cohere_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "rerank-english-v3.0": 0.15,  # Example: $0.15 per search unit
    }
    search_units = tokens_data.get("search_units", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = search_units * model_price
    return {
        "search_units": search_units,
        "price_per_unit": model_price,
        "total": total_price,
    }


def calculate_jina_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "jina-rerank-v1-tiny-en": 0.08,  # Example: $0.08 per 1M tokens
    }
    tokens = tokens_data.get("tokens", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (tokens / 1000000) * model_price
    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


def calculate_voyage_rerank_price(
    model_name: str, tokens_data: Dict[str, int]
) -> Dict[str, float]:
    pricing = {
        "voyage-rerank-v1": 0.12,  # Example: $0.12 per 1M tokens
    }
    tokens = tokens_data.get("tokens", 0)
    model_price = pricing.get(model_name, 0.0)
    total_price = (tokens / 1000000) * model_price
    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


# Token parsers for different reranking providers
def parse_pinecone_rerank_tokens(
    response_data: Dict[str, Any],
) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {"rerank_units": usage.get("rerank_units", 0)}


def parse_cohere_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from cohere response
    meta = response_data.get("meta", {})
    billed_units = meta.get("billed_units", {})
    return {
        "search_units": billed_units.get("search_units", 0),
    }


def parse_jina_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from jina response
    usage = response_data.get("usage", {})
    return {
        "tokens": usage.get("total_tokens", 0),
    }


def parse_voyage_rerank_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from voyage response
    usage = response_data.get("usage", {})
    return {
        "tokens": usage.get("total_tokens", 0),
    }


RERANKING_PROVIDER_CONFIGS = {
    "pinecone": {
        "token_parser": parse_pinecone_rerank_tokens,
        "price_calculator": calculate_pinecone_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "cohere": {
        "token_parser": parse_cohere_rerank_tokens,
        "price_calculator": calculate_cohere_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "jina": {
        "token_parser": parse_jina_rerank_tokens,
        "price_calculator": calculate_jina_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
    "voyage": {
        "token_parser": parse_voyage_rerank_tokens,
        "price_calculator": calculate_voyage_rerank_price,
        "rerank_results_extractor": lambda data: data.get("results", []),
    },
}


def register_reranking_provider(
    provider_name: str,
    token_parser: Callable,
    price_calculator: Callable,
    rerank_results_extractor: Callable,
):
    # Register a new reranking provider with configurations
    RERANKING_PROVIDER_CONFIGS[provider_name] = {
        "token_parser": token_parser,
        "price_calculator": price_calculator,
        "rerank_results_extractor": rerank_results_extractor,
    }


def reranking_tracing(provider: str):
    """
    Decorator for tracing reranking API calls with provider-specific handling

    Args:
        provider: Name of the reranking provider (e.g., "pinecone", "cohere", "jina", "voyage")
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract model_name, query, and documents from args and kwargs
            model_name = kwargs.get("model_name", "")
            if not model_name and len(args) > 1:
                model_name = args[1]  # Assuming model_name is second argument

            query = kwargs.get("query", "")
            if not query and len(args) > 2:
                query = args[2]  # Assuming query is third argument

            documents = kwargs.get("documents", [])
            if not documents and len(args) > 3:
                documents = args[3]  # Assuming documents is fourth argument

            top_n = kwargs.get("top_n", 0)
            if not top_n and len(args) > 4:
                top_n = args[4]

            # Get request ID from context
            id = request_context.get()
            trace_id = id

            # Get provider config
            provider_config = RERANKING_PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                return await func(*args, **kwargs)

            start_time = time.perf_counter()
            ist = timezone(timedelta(hours=5, minutes=30))

            try:
                # Call the original function
                result = await func(*args, **kwargs)

                end_time = time.perf_counter()
                response_time = end_time - start_time

                # Process the response based on provider
                tokens_data = {}
                if isinstance(result, tuple):
                    rerank_results = result[0] if len(result) > 0 else []
                    raw_response = result[1] if len(result) > 1 else None
                    if raw_response:
                        tokens_data = provider_config["token_parser"](
                            raw_response
                        )
                else:
                    # case when function returns entire json response
                    raw_response = result
                    rerank_results = provider_config[
                        "rerank_results_extractor"
                    ](raw_response)
                    tokens_data = provider_config["token_parser"](raw_response)

                rerank_results = []
                for doc in result["data"]:
                    rerank_results.append(documents[doc["index"]])

                # Calculate price if token data is available
                price_data = {}
                if tokens_data and "tokens" in tokens_data:
                    price_data = provider_config["price_calculator"](
                        model_name, tokens_data.get("tokens", 0)
                    )

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY BELOW ###
                try:
                    span_data = {
                        "service_provider": provider,
                        "model_name": model_name,
                        "tokens": tokens_data,
                        "price": price_data,
                        "query": query,
                        "documents": documents,
                        "document_count": len(documents),
                        "top_n": top_n,
                        "rerank_results": rerank_results,
                        "response_time": response_time,
                        "start_time": start_time,
                        "end_time": end_time,
                        "timestamp": datetime.now(ist).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }

                    await _LangfuseService.create_span_for_reranking(
                        trace_id=trace_id,
                        span_data=span_data,
                        name=f"{provider.capitalize()} Reranking",
                    )

                except Exception as e:
                    raise e

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY ABOVE ###

                return result

            except Exception as e:
                raise e

        return wrapper

    return decorator

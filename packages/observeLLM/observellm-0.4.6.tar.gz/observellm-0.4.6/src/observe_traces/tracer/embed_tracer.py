import functools
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

from observe_traces.config.context_util import request_context
from observe_traces.config.langfuse_service import _LangfuseService


def calculate_pinecone_price(model_name: str, tokens: int) -> Dict[str, float]:
    pricing = {
        "llama-text-embed-v2": 0.16,
        "multilingual-e5-large": 0.08,
        "pinecone-sparse-english-v0": 0.08,
        # Add more models as needed
    }

    model_price = pricing.get(model_name, 0.0)  # Default fallback
    total_price = (tokens / 1000000) * model_price

    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


def calculate_cohere_price(model_name: str, tokens: int) -> Dict[str, float]:
    pricing = {
        "embed-english-v3.0": 0.1,
        "embed-multilingual-v3.0": 0.1,
        # Add more models as needed
    }

    model_price = pricing.get(model_name, 0.0)  # Default fallback
    total_price = (tokens / 1000000) * model_price

    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


def calculate_jina_price(model_name: str, tokens: int) -> Dict[str, float]:
    pricing = {
        "jina-embeddings-v2-base-en": 0.05,
        "jina-embeddings-v3": 0.12,
        "jina-embeddings-v2-base-code": 0.05,
        # Add more models as needed
    }

    model_price = pricing.get(model_name, 0.0)  # Default fallback
    total_price = (tokens / 1000000) * model_price

    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


def calculate_voyageai_price(model_name: str, tokens: int) -> Dict[str, float]:
    pricing = {
        "voyage-3": 0.06,
        "voyage-3-lite": 0.02,
        "voyage-finance-2": 0.12,
        "voyage-law-2": 0.12,
        "voyage-code-2": 0.12,
        "voyage-code-3": 0.18,
        "voyage-3-large": 0.18,
        # Add more models as needed
    }

    model_price = pricing.get(model_name, 0.0)  # Default fallback
    total_price = (tokens / 1000000) * model_price

    return {"tokens": tokens, "price_per_1M": model_price, "total": total_price}


# Token parsers for different embedding providers
def parse_pinecone_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from pinecone response
    if "usage" in response_data:
        usage = response_data.get("usage", {})
        return {
            "tokens": usage.get("total_tokens", 0),
        }
    return {"tokens": 0}


def parse_cohere_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from cohere response
    meta = response_data.get("meta", {})
    billed_units = meta.get("billed_units", {})
    return {
        "tokens": billed_units.get("input_tokens", 0),
    }


def parse_jina_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from jina response
    usage = response_data.get("usage", {})
    return {
        "tokens": usage.get("total_tokens", 0),
    }


def parse_voyageai_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    # Extract usage data from voyage response
    usage = response_data.get("usage", {})

    return {
        "tokens": usage.get("total_tokens", 0),
    }


EMBEDDING_PROVIDER_CONFIGS = {
    "pinecone": {
        "token_parser": parse_pinecone_tokens,
        "price_calculator": calculate_pinecone_price,
        "embeddings_extractor": lambda data: [
            item["values"] for item in data.get("data", [])
        ],
    },
    "cohere": {
        "token_parser": parse_cohere_tokens,
        "price_calculator": calculate_cohere_price,
        "embeddings_extractor": lambda data: data.get("embeddings", {}).get(
            "float", []
        ),
    },
    "jina": {
        "token_parser": parse_jina_tokens,
        "price_calculator": calculate_jina_price,
        "embeddings_extractor": lambda data: [
            item["embedding"] for item in data.get("data", [])
        ],
    },
    "voyageai": {
        "token_parser": parse_voyageai_tokens,
        "price_calculator": calculate_voyageai_price,
        "embeddings_extractor": lambda data: [
            item["embedding"] for item in data.get("data", [])
        ],
    },
}


def register_embedding_provider(
    provider_name: str,
    token_parser: Callable,
    price_calculator: Callable,
    embeddings_extractor: Callable,
):
    # Register a new embedding provider with configurations
    EMBEDDING_PROVIDER_CONFIGS[provider_name] = {
        "token_parser": token_parser,
        "price_calculator": price_calculator,
        # "embeddings_extractor": embeddings_extractor
    }


def embedding_tracing(provider: str):
    """
    Decorator for tracing embedding API calls with provider-specific handling

    Args:
        provider: Name of the embedding provider (e.g., "pinecone", "cohere", "jina")
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract model_name and inputs from args and kwargs
            model_name = kwargs.get("model_name", "")
            if not model_name and len(args) > 1:
                model_name = args[1]  # Assuming model_name is second argument

            inputs = kwargs.get("inputs", kwargs.get("texts", []))
            if not inputs and len(args) > 2:
                inputs = args[2]  # Assuming inputs/texts is third argument

            # Get request ID from context
            id = request_context.get()
            trace_id = id

            # Get provider config
            provider_config = EMBEDDING_PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                raise ValueError(
                    f"No configuration found for embedding provider: {provider}"
                )

            start_time = time.perf_counter()

            try:
                # Call the original function
                result = await func(*args, **kwargs)

                end_time = time.perf_counter()
                response_time = end_time - start_time

                # Process the response based on provider
                tokens_data = {}
                if isinstance(result, tuple):
                    embeddings = result[0] if len(result) > 0 else []
                    raw_response = result[1] if len(result) > 1 else None
                    if raw_response:
                        tokens_data = provider_config["token_parser"](
                            raw_response
                        )
                else:
                    # case when function returns entire json response
                    raw_response = result
                    embeddings = provider_config["embeddings_extractor"](
                        raw_response
                    )
                    tokens_data = provider_config["token_parser"](raw_response)

                # Calculate price if token data is available
                price_data = {}
                if tokens_data and "tokens" in tokens_data:
                    price_data = provider_config["price_calculator"](
                        model_name, tokens_data.get("tokens", 0)
                    )

                # Set timezone to IST
                ist = timezone(timedelta(hours=5, minutes=30))

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY BELOW ###
                try:
                    span_data = {
                        "service_provider": provider,
                        "model_name": model_name,
                        "input": (
                            inputs if isinstance(inputs, list) else [inputs]
                        ),
                        "tokens": tokens_data,
                        "price": price_data,
                        "input_count": (
                            len(inputs) if isinstance(inputs, list) else 1
                        ),
                        "response_time": response_time,
                        "start_time": start_time,
                        "end_time": end_time,
                        "timestamp": datetime.now(ist).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "embedding_dimensions": (
                            len(embeddings[0])
                            if embeddings and len(embeddings) > 0
                            else 0
                        ),
                    }

                    await _LangfuseService.create_span_for_embedding(
                        trace_id=trace_id,
                        span_data=span_data,
                        name=f"{provider.capitalize()} Embeddings Generation",
                    )

                except Exception as e:
                    raise e

                ### ADD YOUR CUSTOM LOGIC FOR OBSERVABILITY ABOVE ###

                return result

            except Exception as e:
                raise e

        return wrapper

    return decorator

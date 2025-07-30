import functools
import json
import time
from datetime import datetime
from typing import Any, Callable, Dict

from observe_traces.config.context_util import request_context
from observe_traces.config.langfuse_service import _LangfuseService
from observe_traces.utils.token_costs import get_token_costs


# Token parsers for different providers
def parse_openai_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }


def parse_groq_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    return {
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }


def parse_anthropic_tokens(response_data: Dict[str, Any]) -> Dict[str, int]:
    usage = response_data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    return {
        "prompt_tokens": input_tokens,
        "completion_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def get_completion_start_time(
    response_data: Dict[str, Any], provider: str
) -> float:
    """Extract completion start time from response data based on provider."""
    if provider == "openai":
        # OpenAI includes created timestamp in the response
        return response_data.get("created", time.time())
    elif provider == "anthropic":
        # Anthropic includes started_at timestamp in the response
        return response_data.get("started_at", time.time())
    elif provider == "groq":
        # Groq includes created timestamp in the response
        return response_data.get("created", time.time())
    return time.time()  # Default to current time if not available


PROVIDER_CONFIGS = {
    "openai": {
        "token_parser": parse_openai_tokens,
        "response_extractor": lambda data: (
            data["choices"][0]["message"]["content"]
            if "choices" in data and data["choices"]
            else ""
        ),
    },
    "groq": {
        "token_parser": parse_groq_tokens,
        "response_extractor": lambda data: (
            data["choices"][0]["message"]["content"]
            if "choices" in data and data["choices"]
            else ""
        ),
    },
    "anthropic": {
        "token_parser": parse_anthropic_tokens,
        "response_extractor": lambda data: (
            data["content"][0]["text"]
            if "content" in data and data["content"]
            else ""
        ),
    },
    # Add other providers here
}


def register_provider(
    provider_name: str,
    token_parser: Callable,
    response_extractor: Callable,
):
    # Register a new LLM provider with configurations here
    PROVIDER_CONFIGS[provider_name] = {
        "token_parser": token_parser,
        "response_extractor": response_extractor,
    }


def llm_tracing(provider: str):
    """
    Decorator for tracing LLM API calls with provider-specific handling

    Args:
        provider: Name of the LLM provider (e.g., "openai", "groq")
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, **params):
            # Generate trace ID if not provided
            trace_id = request_context.get()

            # Get provider config
            provider_config = PROVIDER_CONFIGS.get(provider, {})
            if not provider_config:
                return await func(self, **params)

            start_time = time.perf_counter()
            completion_start_time = None

            try:
                result = await func(self, **params)

                end_time = time.perf_counter()
                response_time = end_time - start_time

                if isinstance(result, tuple):
                    response_data = result[0] if len(result) > 0 else None
                    raw_response = result[1] if len(result) > 1 else None
                    llm_response = response_data
                    tokens_data = (
                        provider_config["token_parser"](raw_response)
                        if raw_response
                        else {}
                    )
                    # Get completion start time from raw response
                    if raw_response:
                        completion_start_time = get_completion_start_time(
                            raw_response, provider
                        )
                else:
                    raw_response = result
                    llm_response = provider_config["response_extractor"](
                        raw_response
                    )
                    tokens_data = provider_config["token_parser"](raw_response)
                    # Get completion start time from raw response
                    completion_start_time = get_completion_start_time(
                        raw_response, provider
                    )

                # Calculate price using token_costs utility
                cost_details = {}
                if tokens_data:
                    try:
                        model_pricing = get_token_costs(
                            params.get("model"), provider
                        )
                        prompt_tokens = tokens_data.get("prompt_tokens", 0)
                        completion_tokens = tokens_data.get(
                            "completion_tokens", 0
                        )

                        input_price = (
                            prompt_tokens
                            * model_pricing["input_cost_per_token"]
                        )
                        output_price = (
                            completion_tokens
                            * model_pricing["output_cost_per_token"]
                        )
                        total_price = input_price + output_price

                        cost_details = {
                            "input": input_price,
                            "output": output_price,
                            "total": total_price,
                        }
                    except ValueError as e:
                        raise e

                try:
                    generation_data = {
                        "model_name": params.get("model"),
                        "service_provider": provider,
                        "input": {
                            "user": params.get("chat_messages"),
                            "system": params.get("system_prompt"),
                        },
                        "output": llm_response,
                        "usage": tokens_data,  # Using OpenAI-style usage format for better Langfuse compatibility
                        "cost_details": cost_details,
                        "start_time": datetime.fromtimestamp(start_time),
                        "end_time": datetime.fromtimestamp(end_time),
                    }

                    await _LangfuseService.create_generation_for_LLM(
                        trace_id,
                        generation_data,
                        (
                            params.get("operation_name", "")
                            .replace("_", " ")
                            .title()
                            if params.get("operation_name")
                            else f"{provider.capitalize()} Generation"
                        ),
                    )

                except Exception as e:
                    raise e

                return result

            except Exception as e:
                raise e

        return wrapper

    return decorator


def llm_streaming_tracing(provider: str):
    """
    Decorator for tracing streaming LLM API calls with provider-specific handling.
    Currently only supports Anthropic provider.

    Args:
        provider: Name of the LLM provider (must be "anthropic")
    """
    if provider != "anthropic":
        raise ValueError(
            "Streaming tracing currently only supports Anthropic provider"
        )

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, **params):
            # Generate trace ID if not provided
            trace_id = request_context.get()

            start_time = time.perf_counter()
            total_input_tokens = 0
            total_output_tokens = 0
            collected_response = ""

            try:
                async for response_line in func(self, **params):
                    if response_line.startswith("data: "):
                        response_data = json.loads(response_line[6:])

                        # Handle different event types
                        if response_data["type"] == "message_start":
                            # Get initial input tokens
                            total_input_tokens = response_data["message"][
                                "usage"
                            ]["input_tokens"]
                            total_output_tokens = response_data["message"][
                                "usage"
                            ]["output_tokens"]
                        elif response_data["type"] == "content_block_delta":
                            # Collect response text
                            collected_response += response_data["delta"]["text"]
                        elif response_data["type"] == "message_delta":
                            # Update output tokens
                            total_output_tokens += response_data["usage"][
                                "output_tokens"
                            ]

                        yield response_line
                    else:
                        yield response_line

                end_time = time.perf_counter()
                response_time = end_time - start_time

                # Calculate token usage
                tokens_data = {
                    "prompt_tokens": total_input_tokens,
                    "completion_tokens": total_output_tokens,
                    "total_tokens": total_input_tokens + total_output_tokens,
                }

                # Calculate price using token_costs utility
                cost_details = {}
                if tokens_data:
                    try:
                        model_pricing = get_token_costs(
                            params.get("model"), provider
                        )
                        prompt_tokens = tokens_data.get("prompt_tokens", 0)
                        completion_tokens = tokens_data.get(
                            "completion_tokens", 0
                        )

                        input_price = (
                            prompt_tokens
                            * model_pricing["input_cost_per_token"]
                        )
                        output_price = (
                            completion_tokens
                            * model_pricing["output_cost_per_token"]
                        )
                        total_price = input_price + output_price

                        cost_details = {
                            "input": input_price,
                            "output": output_price,
                            "total": total_price,
                        }
                    except ValueError as e:
                        raise e

                try:
                    generation_data = {
                        "model_name": params.get("model"),
                        "service_provider": provider,
                        "input": {
                            "user": params.get("chat_messages"),
                            "system": params.get("system_prompt"),
                        },
                        "output": collected_response,
                        "usage": tokens_data,
                        "cost_details": cost_details,
                        "start_time": datetime.fromtimestamp(start_time),
                        "end_time": datetime.fromtimestamp(end_time),
                    }

                    await _LangfuseService.create_generation_for_LLM(
                        trace_id,
                        generation_data,
                        (
                            params.get("operation_name", "")
                            .replace("_", " ")
                            .title()
                            if params.get("operation_name")
                            else f"{provider.capitalize()} Generation"
                        ),
                    )

                except Exception as e:
                    raise e

            except Exception as e:
                raise e

        return wrapper

    return decorator

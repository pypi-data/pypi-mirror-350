from typing import Any, Dict, Optional

from langfuse import Langfuse

from observe_traces.config.context_util import tracer_context


class LangfuseClient:
    def __init__(
        self,
        langfuse_public_key: str,
        langfuse_secret_key: str,
        langfuse_host: str,
        release: str,
        environment: str,
    ):
        self.langfuse_public_key = langfuse_public_key
        self.langfuse_secret_key = langfuse_secret_key
        self.langfuse_host = langfuse_host
        self.release = release
        self.environment = environment
        self.langfuse_client = None

    def initialize_langfuse_client(self):
        self.langfuse_client = Langfuse(
            public_key=self.langfuse_public_key,
            secret_key=self.langfuse_secret_key,
            host=self.langfuse_host,
            release=self.release,
            environment=self.environment,
        )

    def close_langfuse_client(self):
        pass


class _LangfuseService:
    _instance = None

    @classmethod
    def initialize(
        cls,
        langfuse_public_key: str,
        langfuse_secret_key: str,
        langfuse_host: str,
        release: str,
        environment: str,
    ) -> None:
        """Initialize the Langfuse client singleton."""
        if cls._instance is None:
            cls._instance = LangfuseClient(
                langfuse_public_key=langfuse_public_key,
                langfuse_secret_key=langfuse_secret_key,
                langfuse_host=langfuse_host,
                release=release,
                environment=environment,
            )
            cls._instance.initialize_langfuse_client()

    @classmethod
    def get_instance(cls) -> Optional[LangfuseClient]:
        """Get the Langfuse client instance."""
        return cls._instance

    @classmethod
    def close(cls) -> None:
        """Close the Langfuse client instance."""
        if cls._instance is not None:
            cls._instance.close_langfuse_client()
            cls._instance = None

    @staticmethod
    async def create_generation_for_LLM(
        trace_id: str, generation_data: Dict[str, Any], name: str
    ) -> Optional[str]:

        try:
            trace = tracer_context.get()

            trace.update(
                output=generation_data["output"],
            )
        except Exception as e:
            return None

        langfuse_client = _LangfuseService.get_instance().langfuse_client
        generation_object = langfuse_client.generation(
            trace_id=trace_id,
            name=name,
        )

        generation_object.end(
            model=generation_data["model_name"],
            # start_time=generation_data["start_time"],
            # end_time=generation_data["end_time"],
            input=generation_data["input"],
            output=generation_data["output"],
            usage_details={
                "input": generation_data["usage"]["prompt_tokens"],
                "output": generation_data["usage"]["completion_tokens"],
                # "total_token": generation_data["usage"]["total_tokens"],
            },
            cost_details={
                "input": generation_data["cost_details"]["input"],
                "output": generation_data["cost_details"]["output"],
                # "total_cost": generation_data["cost_details"]["total"],
            },
            metadata={
                "model": generation_data["model_name"],
                "provider": generation_data["service_provider"],
                "start_time": generation_data["start_time"],
                "end_time": generation_data["end_time"],
                "time_taken": (
                    generation_data["end_time"] - generation_data["start_time"]
                ).total_seconds(),
                "input_token": generation_data["usage"]["prompt_tokens"],
                "output_token": generation_data["usage"]["completion_tokens"],
                "input_cost": generation_data["cost_details"]["input"],
                "output_cost": generation_data["cost_details"]["output"],
                "total_cost": generation_data["cost_details"]["total"],
            },
        )

        return generation_object.id

    @staticmethod
    async def create_span_for_vectorDB(
        trace_id: str, span_data: Dict[str, Any], name: str
    ) -> Optional[str]:

        langfuse_client = _LangfuseService.get_instance().langfuse_client
        span_object = langfuse_client.span(
            trace_id=trace_id,
            name=name,
        )

        span_object.end(
            input=span_data["query"],
            output=span_data["response"],
            start_time=span_data["start_time"],
            end_time=span_data["end_time"],
            metadata={
                **span_data["operation_details"],
                "operation_type": span_data["operation_type"],
                "provider": span_data["service_provider"],
                "cost": span_data["price"],
                "read_units": span_data["units"],
            },
        )

        return span_object.id

    @staticmethod
    async def create_span_for_embedding(
        trace_id: str, span_data: Dict[str, Any], name: str
    ) -> Optional[str]:

        try:
            trace = tracer_context.get()

            trace.update(
                input=span_data["input"],
            )
        except Exception as e:
            return None

        langfuse_client = _LangfuseService.get_instance().langfuse_client
        span_object = langfuse_client.span(
            trace_id=trace_id,
            name=name,
        )

        span_object.end(
            input=span_data["input"],
            start_time=span_data["start_time"],
            end_time=span_data["end_time"],
            metadata={
                "provider": span_data["service_provider"],
                "model_name": span_data["model_name"],
                "input count": span_data["input_count"],
                "cost": span_data["price"]["total"],
                "token usage": span_data["tokens"],
                "price": span_data["price"],
                "embedding_dimensions": span_data["embedding_dimensions"],
                "response_time": span_data["response_time"],
                "timestamp": span_data["timestamp"],
            },
        )

        return span_object.id

    @staticmethod
    async def create_span_for_reranking(
        trace_id: str, span_data: Dict[str, Any], name: str
    ) -> Optional[str]:

        langfuse_client = _LangfuseService.get_instance().langfuse_client
        span_object = langfuse_client.span(
            trace_id=trace_id,
            name=name,
        )

        span_object.end(
            input={
                "query": span_data["query"],
                "documents": span_data["documents"],
            },
            output=span_data["rerank_results"],
            start_time=span_data["start_time"],
            end_time=span_data["end_time"],
            metadata={
                "provider": span_data["service_provider"],
                "model_name": span_data["model_name"],
                "output_count": span_data["document_count"],
                "cost": span_data["price"],
                "token usage": span_data["tokens"]["rerank_units"],
                "response_time": span_data["response_time"],
                "timestamp": span_data["timestamp"],
                "top_n": span_data["top_n"],
            },
        )

        return span_object.id

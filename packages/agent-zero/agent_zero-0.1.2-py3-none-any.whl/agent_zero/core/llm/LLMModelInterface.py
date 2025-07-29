from abc import ABC, abstractmethod
from typing import Generator, AsyncGenerator

from openai import Stream, AsyncStream
from openai.types.chat import ChatCompletionChunk

from pipecat.services.llm_service import LLMService as PipecatLLMService
from pipecat.frames.frames import TextFrame, EndFrame

class LLMModelInterface(ABC):
    def __init__(self, model, original_name):
        self.model = model
        self.original_name = original_name

    @abstractmethod
    def initialize_async_client(self, *args):
        pass

    @abstractmethod
    def prepare_messages(self, *args) -> list:
        pass

    @abstractmethod
    async def ainvoke_model(self, client, messages, temperature, max_tokens, top_p, response_type, tools, tool_choice, parallel_tool_calls) -> dict:
        pass

    @abstractmethod
    async def ainvoke_model_stream(self, client, messages, temperature, max_tokens, top_p, tools, tool_choice, parallel_tool_calls) -> AsyncStream[ChatCompletionChunk]:
        pass

    @abstractmethod
    async def async_call_llm_stream(self, messages, temperature=None, max_tokens=None, top_p=None, tools=None, tool_choice=None, parallel_tool_calls=False) -> AsyncGenerator[ChatCompletionChunk, None]:
        pass

    @abstractmethod
    async def async_call_llm(self, messages, temperature=None, max_tokens=None, top_p=None, response_type=None, response_schema=None, tools=None, tool_choice=None, parallel_tool_calls=False) -> dict:
        pass

def as_pipecat_service(llm_cls):
    """
    Decorator that wraps any ``LLMModelInterface`` subclass so it can also be
    used in a Pipecat pipeline *without removing its original methods*.
    """
    class _PipecatAdapter(llm_cls, PipecatLLMService):
        def __init__(self, *args, **kwargs):
            llm_cls.__init__(self, *args, **kwargs)
            PipecatLLMService.__init__(self)

        async def call_llm(self, messages, **params):
            return await self.async_call_llm(
                messages,
                temperature=params.get("temperature"),
                max_tokens=params.get("max_tokens"),
                top_p=params.get("top_p"),
                response_type=params.get("response_type"),
                response_schema=params.get("response_schema"),
                tools=params.get("tools"),
                tool_choice=params.get("tool_choice"),
                parallel_tool_calls=params.get("parallel_tool_calls", False),
            )

        async def stream_llm(self, messages, **params):
            async for chunk in self.async_call_llm_stream(
                messages,
                temperature=params.get("temperature"),
                max_tokens=params.get("max_tokens"),
                top_p=params.get("top_p"),
                tools=params.get("tools"),
                tool_choice=params.get("tool_choice"),
                parallel_tool_calls=params.get("parallel_tool_calls", False),
            ):
                token = chunk.choices[0].delta.get("content")
                if token:
                    yield TextFrame(token)
            yield EndFrame()

    _PipecatAdapter.__name__ = f"{llm_cls.__name__}PipecatAdapter"
    return _PipecatAdapter

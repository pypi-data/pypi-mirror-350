import copy
import json

from typing import AsyncGenerator, Optional, List, Dict, AsyncIterable
from google.oauth2 import service_account
from vertexai.generative_models import FunctionCall, Candidate
from vertexai.preview.generative_models import (
    GenerativeModel,
    ChatSession,
    GenerationConfig,
    Tool,
    Content,
    FunctionDeclaration,
    Part,
    GenerationResponse,
)
from vertexai import init
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function as ChatCompletionMessageToolCallFunction
import time

from agent_zero.data.consts import GOOGLE_CREDENTIALS
from .LLMModelInterface import LLMModelInterface
from .helpers.async_retry_llm_call_decorator import async_retry_with_pause

FINISH_REASON_MAP = {
    0: None,
    1: "stop",
    2: "length",
    3: "function_call"
}

def safe_function_arguments(raw_args):
    if not raw_args or not isinstance(raw_args, dict):
        return "{}"
    cleaned = {
        str(k): v for k, v in raw_args.items()
        if k and v not in [None, "", [], {}]
    }
    return json.dumps(cleaned) if cleaned else "{}"

class Usage:
    def __init__(self, prompt, completion, total):
        self.prompt_tokens = prompt
        self.completion_tokens = completion
        self.total_tokens = total

    def to_dict(self):
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


class Delta:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls

    def to_dict(self):
        data = {}
        if self.content is not None:
            data["content"] = self.content
        if self.tool_calls:
            data["tool_calls"] = self.tool_calls
        return data

    def __repr__(self):
        return (
            f"Delta(content={repr(self.content)}, tool_calls={repr(self.tool_calls)})"
        )


class DeltaChoice:
    def __init__(self, delta, finish_reason=None, index=0):
        self.delta = Delta(
            content=delta.get("content"),
            tool_calls=delta.get("tool_calls"),
        )
        self.finish_reason = finish_reason
        self.index = index

    def to_dict(self):
        return {
            "delta": self.delta.to_dict(),
            "finish_reason": self.finish_reason,
            "index": self.index,
        }


class OpenAIStyleChunk:
    def __init__(self, choices, usage_metadata=None):
        self.choices = choices
        if usage_metadata:
            self.usage = Usage(
                prompt=usage_metadata.prompt_token_count,
                completion=usage_metadata.candidates_token_count,
                total=usage_metadata.total_token_count,
            )
        else:
            self.usage = None

    def to_dict(self):
        base = {
            "choices": [choice.to_dict() for choice in self.choices],
        }
        if self.usage:
            base["usage"] = self.usage.to_dict()
        return base

    def encode(self, encoding='utf-8'):
        return (f"data: {json.dumps(self.to_dict(), ensure_ascii=False, default=lambda o: o.model_dump() if hasattr(o, 'model_dump') else str(o))}\n\n").encode(encoding)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"

class GeminiBaseModel(LLMModelInterface):

    def __init__(
        self,
        model: str,
        project: str = "956319252358",
        location: str = "europe-central2",
        credentials: Optional[service_account.Credentials] = None,
    ):
        original_name = f"Gemini/{model}"
        super().__init__(model, original_name)

        if credentials is None and GOOGLE_CREDENTIALS:
            init(project=project, location=location, credentials=GOOGLE_CREDENTIALS)
        else:
            raise ValueError(
                "No credentials found in environment. Set GOOGLE_CREDENTIALS_JSON or pass credentials explicitly into GeminiBaseModel.")

        self.model = model
        self.client = None

    def prepare_messages(
        self, messages
    ) -> tuple[str | None, list[Content], str | None]:
        role_map = {"user": "user", "assistant": "model"}
        history = []
        system_instruction = None

        for m in messages:
            if m["role"] == "system" and system_instruction is None:
                system_instruction = m["content"]

            elif m["role"] in role_map:
                if "tool_calls" in m and m["tool_calls"]:
                    for tool_call in m["tool_calls"]:
                        history.append(Content(
                            role="model",
                            parts=[
                                Part.from_dict({
                                    "functionCall": {
                                        "name": tool_call["function"]["name"],
                                        "args": tool_call["function"]["arguments"]
                                    }
                                })
                            ]
                        ))
                else:
                    history.append(Content(
                        role=role_map[m["role"]],
                        parts=[Part.from_text(m["content"])]
                    ))

            elif m["role"] == "tool":
                response_data = m["content"]
                if isinstance(response_data, str):
                    try:
                        response_data = json.loads(response_data)
                    except json.JSONDecodeError:
                        response_data = {"_": response_data}
                if not isinstance(response_data, dict):
                    response_data = {"output": response_data}

                history.append(Content(
                    parts=[
                        Part.from_dict({
                            "functionResponse": {
                                "name": m.get("name", "unknown_function"),
                                "response": response_data
                            }
                        })
                    ]
                ))

        # Extract last user message as query
        query = None
        for m in reversed(messages):
            if m["role"] == "user":
                query = m["content"]
                break

        return system_instruction, history, query

    def initialize_async_client(self, messages, tools):
        return self.initialize_client(messages)

    def initialize_client(self, messages):
        system_instruction, history, query = self.prepare_messages(messages)
        self.generative_model = GenerativeModel(
            model_name=self.model, system_instruction=system_instruction
        )

        return self.generative_model.start_chat(history=history), query

    def transform_stream_chunk_to_openai_format(self, chunk) -> OpenAIStyleChunk | None:
        if hasattr(chunk, "candidates") and chunk.candidates:
            candidate: Candidate = chunk.candidates[0]
            parts: list[Part] = candidate.content.parts
            delta_dict = {}
            raw_finish_reason = getattr(candidate, "finish_reason", 0)
            finish_reason = FINISH_REASON_MAP.get(raw_finish_reason, None)

            for part in parts:
                if hasattr(part, "function_call") and isinstance(
                    part.function_call, FunctionCall
                ):
                    from types import SimpleNamespace
                    delta_dict["tool_calls"] = [
                        ChatCompletionMessageToolCall(
                            id="call_0",
                            index=0,
                            type="function",
                            function=ChatCompletionMessageToolCallFunction(
                                name=part.function_call.name,
                                arguments=safe_function_arguments(part.function_call.args),
                            ),
                        )
                    ]
                elif hasattr(part, "text") and part.text:
                    delta_dict["content"] = part.text

            if delta_dict:
                params = {"delta":delta_dict}
                if finish_reason:
                    params["finish_reason"] = finish_reason
                return OpenAIStyleChunk(
                    choices=[DeltaChoice(**params)]
                )

        return None

    def transform_full_response_to_openai_format(self, gemini_response) -> ChatCompletion:
        # Map Gemini tool calls to OpenAI format
        tool_calls = []
        if getattr(gemini_response, "tool_calls", None):
            for i, tool_call in enumerate(gemini_response.tool_calls):
                tool_calls.append(
                    ChatCompletionMessageToolCall(
                        id="call_{i}",
                        index=i,
                        type="function",
                        function=ChatCompletionMessageToolCallFunction(
                            name=tool_call.name,
                            arguments=safe_function_arguments(tool_call.args),
                        ),
                    )
                )

        # Construct OpenAI-style message
        message = ChatCompletionMessage(
            role="assistant",
            content=gemini_response.text,
            tool_calls=tool_calls or None
        )

        return ChatCompletion(
            id="call_0",
            object="chat.completion",
            created=int(time.time()),
            model=self.model,
            choices=[
                Choice(
                    index=0,
                    message=message,
                    finish_reason="tool_calls" if tool_calls else "stop"
                )
            ]
        )

    def map_openai_tools_to_gemini(
        self, tools: Optional[List[Dict]]
    ) -> Optional[List[Tool]]:
        if not tools:
            return None

        function_declarations = []

        for tool in tools:
            if tool["type"] == "function":
                fn = tool["function"]
                parameters = fn.get("parameters", {})

                if parameters.get("type") == "object" and not parameters.get(
                    "properties"
                ):
                    parameters["properties"] = {
                        "_": {
                            "type": "string",
                            "description": "Placeholder required by Gemini.",
                        }
                    }

                function_declarations.append(
                    FunctionDeclaration(
                        name=fn["name"],
                        description=fn.get("description", ""),
                        parameters=parameters,
                    )
                )

        return [Tool(function_declarations=function_declarations)]

    @async_retry_with_pause
    async def ainvoke_model(
        self,
        client: ChatSession,
        user_query: str,
        temperature,
        max_tokens,
        top_p,
        *_args,
        tools=None,
        **_kwargs,
    ) -> ChatCompletion:
        params = {
            "content": user_query,
            "generation_config": GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=top_p,
            ),
        }

        if tools:
            gemini_tools = self.map_openai_tools_to_gemini(tools)
            params["tools"] = gemini_tools

        response = await client.send_message_async(**params)

        return self.transform_full_response_to_openai_format(response)

    async def ainvoke_model_stream(
        self,
        client: ChatSession,
        user_query: str,
        temperature,
        max_tokens,
        top_p,
        *_args,
        tools=None,
        **_kwargs,
    ) -> AsyncIterable[GenerationResponse]:
        params = {
            "content": user_query,
            "stream": True,
        }

        config_kwargs = {}
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if max_tokens is not None:
            config_kwargs["max_output_tokens"] = max_tokens
        if top_p is not None:
            config_kwargs["top_p"] = top_p
        if temperature or top_p or max_tokens:
            params["generation_config"]: GenerationConfig(**config_kwargs)

        if tools:
            gemini_tools = self.map_openai_tools_to_gemini(tools)
            params["tools"] = gemini_tools

        stream = await client.send_message_async(**params)

        async for chunk in stream:
            response_chunk = self.transform_stream_chunk_to_openai_format(chunk)
            if response_chunk:
               yield response_chunk

        # yield OpenAIStyleChunk(choices=[DeltaChoice(delta={}, finish_reason="stop")])

    async def async_call_llm_stream(
        self,
        messages,
        temperature=None,
        max_tokens=None,
        top_p=None,
        tools=None,
        **_kwargs,
    ) -> AsyncGenerator[dict, None]:
        messages = copy.deepcopy(messages)

        client, query = self.initialize_client(messages)

        async for r in self.ainvoke_model_stream(
            client, query, temperature, max_tokens, top_p, tools=tools
        ):
            yield r

    async def async_call_llm(
        self,
        messages,
        temperature=None,
        max_tokens=None,
        top_p=None,
        tools=None,
        **_kwargs,
    ) -> dict:
        messages = copy.deepcopy(messages)
        client, query = self.initialize_client(messages)

        response = await self.ainvoke_model(
            client, query, temperature, max_tokens, top_p, tools=tools
        )
        return {
            "role": "assistant",
            "content": response.choices[0].message.content.strip()
        }

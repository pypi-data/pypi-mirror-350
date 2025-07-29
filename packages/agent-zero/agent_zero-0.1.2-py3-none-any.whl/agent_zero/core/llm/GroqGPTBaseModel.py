import copy
import json
from typing import AsyncGenerator

from openai.types.chat import ChatCompletionChunk

from .LLMModelInterface import LLMModelInterface
from openai import AsyncClient, AsyncStream
from groq import AsyncGroq

from .helpers.async_retry_llm_call_decorator import async_retry_with_pause

class GroqGPTBaseModel(LLMModelInterface):

    def __init__(self, model: str, api_key: str, client_class, async_client_class, response_format_class, base_url=None):
        original_name = f"{client_class.__name__}/{model}"
        super().__init__(model, original_name)
        self.api_key = api_key
        self.client_class = client_class
        self.async_client_class = async_client_class
        self.response_format_class = response_format_class
        self.base_url = base_url

    def initialize_async_client(self):
        if self.base_url:
            return self.async_client_class(api_key=self.api_key, base_url=self.base_url)
        return self.async_client_class(api_key=self.api_key)

    def prepare_messages(self, messages) -> list:

        for message in messages:
            if tool_calls := message.get("tool_calls"):
                for tool_call in tool_calls:
                    if type(tool_call['function']['arguments']) is dict:
                        tool_call['function']['arguments'] = json.dumps(tool_call['function']['arguments'])

        return messages

    def prepare_response(self, response):

        if "refusal" in list(response.keys()):
            del response['refusal']
        if tool_calls := response.get("tool_calls"):
            for tool_call in tool_calls:
                tool_call['function']['arguments'] = json.loads(tool_call['function']['arguments'])

        return response

    @async_retry_with_pause
    async def ainvoke_model(self, client: AsyncClient | AsyncGroq, messages, temperature, max_tokens, top_p, response_type, tools, tool_choice, parallel_tool_calls) -> dict:
        params = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
        }
        if tools:
            params['tools'] = tools
            params['parallel_tool_calls'] = parallel_tool_calls
            params['tool_choice'] = tool_choice
        if response_type:
            params['response_format'] = self.response_format_class(type=response_type)
        response = await client.chat.completions.create(**params)
        return response.choices[0].message.to_dict()

    @async_retry_with_pause
    async def ainvoke_model_stream(self, client: AsyncClient | AsyncGroq, messages, temperature, max_tokens, top_p, tools, tool_choice, parallel_tool_calls) -> AsyncStream[ChatCompletionChunk]:
        params = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'stream': True
        }
        if tools:
            params['tools'] = tools
            params['parallel_tool_calls'] = parallel_tool_calls
            params['tool_choice'] = tool_choice

        response = await client.chat.completions.create(**params)
        return response

    async def async_call_llm_stream(self, messages, temperature=None, max_tokens=None, top_p=None, tools=None, tool_choice='none', parallel_tool_calls=False) -> AsyncGenerator[ChatCompletionChunk, None]:
        client = self.initialize_async_client()

        messages = copy.deepcopy(messages)
        messages = self.prepare_messages(messages)

        response = await self.ainvoke_model_stream(client, messages, temperature, max_tokens, top_p, tools, tool_choice, parallel_tool_calls)
        async for r in response:
            yield r

    async def async_call_llm(self, messages, temperature=None, max_tokens=None, top_p=None, response_type=None, response_schema=None, tools=None, tool_choice=None, parallel_tool_calls=False) -> dict:
        try:
            client = self.initialize_async_client()

            messages = copy.deepcopy(messages)
            messages = self.prepare_messages(messages)

            response = await self.ainvoke_model(client, messages, temperature, max_tokens, top_p, response_type, tools, tool_choice, parallel_tool_calls)
            response = self.prepare_response(response)
            return response
        except Exception as e:
            print(f"Error in async_call_llm func: {type(e)}\n\n{str(e)}")

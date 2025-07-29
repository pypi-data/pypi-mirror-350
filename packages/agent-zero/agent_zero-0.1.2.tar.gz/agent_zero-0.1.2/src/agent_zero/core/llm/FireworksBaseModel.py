import copy
import json
from typing import AsyncGenerator
from fireworks.client import AsyncFireworks
from openai.types.chat import ChatCompletionChunk

from .LLMModelInterface import LLMModelInterface
from .helpers.async_retry_llm_call_decorator import async_retry_with_pause
from .models.llm_types import IntentSchema

class FireworksLlamaBaseModel(LLMModelInterface):

    def __init__(self, model: str, api_key: str, client_class, async_client_class, response_format_class, base_url=None):
        original_name = model
        super().__init__(model, original_name)
        self.api_key = api_key
        self.client_class = client_class
        self.async_client_class = async_client_class
        self.response_format_class = response_format_class
        self.base_url = base_url or "https://api.fireworks.ai/inference/v1"


    def initialize_async_client(self):
        if self.base_url:
            return self.async_client_class(api_key=self.api_key, base_url=self.base_url)
        return self.async_client_class(api_key=self.api_key)

    def prepare_messages(self, messages) -> list:
        for message in messages:
            if tool_calls := message.get("tool_calls"):
                for tool_call in tool_calls:
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
    async def ainvoke_model(self, client: AsyncFireworks, messages, temperature, max_tokens, top_p, response_type, tools, tool_choice, parallel_tool_calls, response_schema=None) -> dict:
        params = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'top_k': 40,
            'stream': False
        }

        if tools:
            params['tools'] = tools
            params['parallel_tool_calls'] = parallel_tool_calls
            params['tool_choice'] = tool_choice
        if response_type == "json_object":
            params['response_format'] = {
                "type": "json_object"
            }
            if response_schema:
                params['response_format']["schema"] = response_schema.model_json_schema()
            else:
                params['response_format']["schema"] = IntentSchema.model_json_schema()


        response = await client.chat.completions.acreate(**params)
        message = response.choices[0].message
        return {
            'role': message.role,
            'content': message.content,
            'tool_calls': message.tool_calls if hasattr(message, 'tool_calls') else None
        }

    @async_retry_with_pause
    async def ainvoke_model_stream(self, client: AsyncFireworks, messages, temperature, max_tokens, top_p, tools, tool_choice, parallel_tool_calls):
        params = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'top_k': 40,
            'stream': True
        }

        if tools:
            params['tools'] = tools
            params['parallel_tool_calls'] = parallel_tool_calls
            params['tool_choice'] = tool_choice

        return client.chat.completions.acreate(**params)

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

            response = await self.ainvoke_model(client, messages, temperature, max_tokens, top_p, response_type, tools, tool_choice, parallel_tool_calls, response_schema)
            response = self.prepare_response(response)
            return response
        except Exception as e:
            print(f"Error in async_call_llm func: {type(e)}\n\n{str(e)}")
            return {}

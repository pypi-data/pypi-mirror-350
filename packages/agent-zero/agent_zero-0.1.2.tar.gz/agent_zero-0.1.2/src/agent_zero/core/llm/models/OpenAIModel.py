import openai
from openai.types.chat.completion_create_params import ResponseFormat
from agent_zero.data.consts import OPENAI_API_KEY
from agent_zero.core.llm.GroqGPTBaseModel import GroqGPTBaseModel


class ChatGptModel(GroqGPTBaseModel):

    def __init__(self, model: str, openai_key=None):
        super().__init__(model, openai_key if openai_key else OPENAI_API_KEY, openai.Client, openai.AsyncClient, ResponseFormat)

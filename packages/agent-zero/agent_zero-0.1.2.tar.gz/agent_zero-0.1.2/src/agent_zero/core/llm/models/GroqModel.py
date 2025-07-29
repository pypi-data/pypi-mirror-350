from groq import Groq, AsyncGroq
from groq.types.chat.completion_create_params import ResponseFormat
from agent_zero.data.consts import GROQ_API_KEY
from agent_zero.core.llm.GroqGPTBaseModel import GroqGPTBaseModel


class GroqModel(GroqGPTBaseModel):

    def __init__(self, model: str, groq_api_key=None):
        super().__init__(model, groq_api_key if groq_api_key else GROQ_API_KEY, Groq, AsyncGroq, ResponseFormat)

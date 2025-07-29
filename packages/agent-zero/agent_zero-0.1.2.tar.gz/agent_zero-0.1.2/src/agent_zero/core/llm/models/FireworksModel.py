from agent_zero.data.consts import FIREWORKS_API_KEY
from agent_zero.core.llm.FireworksBaseModel import FireworksLlamaBaseModel
from fireworks.client import AsyncFireworks, Fireworks
from agent_zero.core.llm.models.llm_types import ResponseFormat


class FireworksModel(FireworksLlamaBaseModel):
    def __init__(self, model: str, fireworks_api_key=None):
        super().__init__(
            model, fireworks_api_key if fireworks_api_key else FIREWORKS_API_KEY, Fireworks, AsyncFireworks, ResponseFormat)
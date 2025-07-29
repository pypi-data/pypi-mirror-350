from agent_zero.core.llm.VertexAIGeminiBaseModel import GeminiBaseModel

class GeminiModel(GeminiBaseModel):
    def __init__(self, model: str, project: str=None, location: str=None):
        super().__init__(model, project, location)

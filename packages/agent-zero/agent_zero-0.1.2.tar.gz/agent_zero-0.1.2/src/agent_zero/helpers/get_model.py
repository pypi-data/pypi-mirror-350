from typing import Type, Dict
import inspect

from agent_zero.core.llm.LLMModelInterface import LLMModelInterface
from agent_zero.core.llm.models.VertexAIGeminiModel import GeminiModel
from agent_zero.core.llm.models.OpenAIModel import ChatGptModel
from agent_zero.core.llm.models.GroqModel import GroqModel
from agent_zero.core.llm.models.FireworksModel import FireworksModel


class ModelFactory:
    """
    Factory for creating LLM model instances based on a given vendor name.
    """

    _registry: Dict[str, Type[LLMModelInterface]] = {
        "openai": ChatGptModel,
        "google": GeminiModel,
        "groq": GroqModel,
        "fireworks": FireworksModel,
    }

    @classmethod
    def register_vendor(cls, vendor: str, model_cls: Type[LLMModelInterface]) -> None:
        """
        Register a new vendor-model class mapping.

        Args:
            vendor (str): Name of the vendor (e.g. 'openai').
            model_cls (Type[LLMModelInterface]): Corresponding model class.
        """
        cls._registry[vendor.strip().lower()] = model_cls

    @classmethod
    def get_model(
        cls,
        vendor: str,
        model_name: str,
        **init_kwargs
    ) -> LLMModelInterface:
        """
        Instantiate an LLM model by vendor and model name.

        Args:
            vendor (str): Name of the vendor.
            model_name (str): Identifier of the model.
            **init_kwargs: Additional keyword arguments for model instantiation.

        Returns:
            LLMModelInterface: Instantiated model object.
        """
        key = vendor.strip().lower()
        if key not in cls._registry:
            valid = ", ".join(cls._registry.keys())
            raise ValueError(f"Unknown vendor '{vendor}'. Expected one of: {valid}")

        model_cls = cls._registry[key]

        # Filter kwargs to only those accepted by the constructor
        sig = inspect.signature(model_cls.__init__)
        accepted = {
            name for name in sig.parameters if name not in ("self", "model")
        }
        filtered_kwargs = {k: v for k, v in init_kwargs.items() if k in accepted}

        return model_cls(model_name, **filtered_kwargs)


# Convenience alias
get_model = ModelFactory.get_model

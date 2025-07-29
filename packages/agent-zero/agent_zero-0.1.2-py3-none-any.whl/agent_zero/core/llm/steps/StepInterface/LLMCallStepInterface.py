from agent_zero.data.consts import BASE_TEMPERATURE, BASE_MAX_TOKENS, BASE_TOP_P
from agent_zero.core.llm.steps.InferenceStepDebugObjects import Argument
from agent_zero.core.llm.steps.StepInterface.InferenceStepInterface import InferenceStepInterface
from abc import abstractmethod

from agent_zero.core.llm.LLMModelInterface import LLMModelInterface


class LLMCallStepInterface(InferenceStepInterface):

    def __init__(self, step_name: str,
                 stage_name: str,
                 llm: LLMModelInterface,
                 temperature=BASE_TEMPERATURE,
                 max_tokens=BASE_MAX_TOKENS,
                 top_p=BASE_TOP_P,
                 messages: list = [],
                 response_type=None,
                 tools=None,
                 tool_choice='none',
                 parallel_tool_calls=False):
        """
        response_type can be only text or json_object
        """
        super().__init__(step_name, stage_name, step_type='LLM')
        self.system_message = None
        self.history = None
        self.messages = messages
        self.llm = llm
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        if response_type not in ['text', 'json_object', None]:
            raise ValueError('invalid response type')
        self.response_type = response_type
        self.tools = tools
        self.tool_choice = tool_choice
        if tool_choice != 'none' and tool_choice != 'auto' and tool_choice != 'required' and not isinstance(tool_choice, dict):
            raise Exception('Invalid tool_choice value')
        self.parallel_tool_calls = parallel_tool_calls

    @abstractmethod
    def process(self, current_input, *args, **kwargs):
        pass

    def get_attributes(self) -> list:
        self.attributes.append(Argument("model", self.llm.original_name).to_dict())
        self.attributes.append(Argument("max_tokens", self.max_tokens).to_dict())
        self.attributes.append(Argument("temperature", self.temperature).to_dict())
        self.attributes.append(Argument('top_p', self.top_p).to_dict())
        self.attributes.append(Argument("response_type", self.response_type).to_dict())
        return self.attributes

    def collect_metrics(self, tokens, costs):
        self.metrics.append(Argument("tokens", tokens).to_dict())
        self.metrics.append(Argument("costs", costs).to_dict())

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, create_model

from agent_zero.data.consts import StateEnum, languages
from agent_zero.core.config import get_config

class ConversationFlow(BaseModel):
    active_agent: StateEnum = StateEnum.MAIN_AGENT_FLOW
    arguments: dict = Field(default_factory=dict)


class PostCallAnalysisSchema(BaseModel):
    callback_time: Optional[datetime]  # Null if no appointment was set
    call_status: str  # One of the predefined status strings
    call_summary: str  # A brief 1-2 sentence natural-language summary

class AgentSettings(BaseModel):
    voice_provider: str
    voice_url: Optional[str]
    voice_id: Optional[str]
    start_message: Optional[str] = None
    speak_first: Optional[bool] = False


class RequestBodyForVoiceAI(BaseModel):
    inference_url: Optional[str]
    prompt: str
    inputs: Optional[dict]
    from_number: Optional[str]
    to_number: Optional[str]
    agent_settings: Optional[AgentSettings]
    end_call_seconds: Optional[int] = None
    background_noise: Optional[bool] = False
    language: Optional[str] = 'en'
    play_audio_url: Optional[str] = None


class Metadata(BaseModel):
    history: list[dict]

    generated_messages_per_turn: list[dict] = Field(default_factory=list)
    active_flow: ConversationFlow = Field(default_factory=ConversationFlow)
    finalize_action: Optional[Literal["__end__", "__transfer__"]] = None
    finalize_action_kwargs: Optional[dict] = Field(default_factory=dict)


class PlatformMetadata(BaseModel):
    platform: Optional[Literal["retell", "elevenlabs"]] = None
    response_id: Optional[int] = None
    turn_taking: Optional[Literal["agent_turn", "user_turn"]] = None
    tools: Optional[List] = None


class RequestBody(BaseModel):
    conversation_id: str
    query: Optional[str] = None
    agent_inputs: BaseModel = Field(default_factory=lambda: create_agent_inputs())
    metadata: Metadata = None
    stream: bool = False
    history: Optional[List[Dict[str, Any]]] = None
    platform_metadata: Optional[PlatformMetadata] = None


class RelevantResponseRequest(BaseModel):
    conversation_id: str
    platform_metadata: PlatformMetadata


class CallMonitor(BaseModel):
    listenUrl: str
    controlUrl: str


class Transport(BaseModel):
    assistantVideoEnabled: bool


class AssistantOverrides(BaseModel):
    clientMessages: List[str]


class Call(BaseModel):
    id: str
    orgId: str
    createdAt: str
    updatedAt: str
    type: str
    monitor: CallMonitor
    transport: Transport
    webCallUrl: str
    status: str
    assistantId: str
    assistantOverrides: AssistantOverrides


class Message(BaseModel):
    role: str
    content: str


class VapiRequestBody(BaseModel):
    model: str
    messages: List[Message]
    temperature: float
    stream: bool
    max_tokens: int
    call: Call
    metadata: Dict[str, Any]
    credentials: List[Any]


class ElevenlabsRequestBody(BaseModel):
    messages: List
    model: str
    max_tokens: int
    stream: bool
    temperature: float
    tools: Optional[List[Dict]]
    elevenlabs_extra_body: Optional[dict] = None


class ContentResponse(BaseModel):
    response_type: Literal["response"] = "response"
    content: str


class ToolCallInvocationResponse(BaseModel):
    response_type: Literal["tool_call_invocation"] = "tool_call_invocation"
    tool_call_id: str
    name: str
    arguments: str


class ToolCallResultResponse(BaseModel):
    response_type: Literal["tool_call_result"] = "tool_call_result"
    tool_call_id: str
    content: str


InferenceEvent = Union[
    ContentResponse | ToolCallInvocationResponse | ToolCallResultResponse
]


_TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "dict": dict,
    "list": list,
}

_AGENT_INPUTS_MODEL: type[BaseModel] | None = None


def _build_agent_inputs_model() -> type[BaseModel]:
    global _AGENT_INPUTS_MODEL
    if _AGENT_INPUTS_MODEL is not None:
        return _AGENT_INPUTS_MODEL

    cfg_defaults = get_config()["agent_inputs"]
    fields = {}

    for key, raw in cfg_defaults.items():
        if isinstance(raw, dict) and "value" in raw:
            val = raw["value"]
            typ = _TYPE_MAP.get(raw.get("type"), type(val))
        else:
            val = raw
            typ = type(val)
        fields[key] = (typ, val)

    model_cls = create_model(
        f"{get_config()['agent_inputs']['project_name'].capitalize()}AgentInputs",
        __base__=BaseModel,
        **fields,
    )
    _AGENT_INPUTS_MODEL = model_cls
    return model_cls


def create_agent_inputs() -> BaseModel:
    """
    Create a Pydantic model instance for agent inputs using only
    the default values from the project config.
    """
    model_cls = _build_agent_inputs_model()

    cfg_defaults = get_config()["agent_inputs"]

    # Extract default values, skipping keys with None
    defaults: dict[str, Any] = {}
    for key, raw in cfg_defaults.items():
        if raw is None:
            continue
        if isinstance(raw, dict) and "value" in raw:
            defaults[key] = raw["value"]
        else:
            defaults[key] = raw

    return model_cls(**defaults)

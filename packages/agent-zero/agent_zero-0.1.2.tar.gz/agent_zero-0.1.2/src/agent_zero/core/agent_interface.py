"""Defines base and specialized agent interfaces for managing conversation flows and metadata."""

import json
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Literal, Optional, Union, Tuple

from pydantic import BaseModel, Field

from agent_zero.core.llm.steps.StepInterface.LLMCallStepInterface import LLMCallStepInterface
from agent_zero.core.llm.steps.Steps.PhantomStep import PhantomStep

from agent_zero.helpers import add_debug_data
from agent_zero.data.schemas import InferenceEvent


class MetadataBaseModel(BaseModel):
    """Base metadata model for agent finalization actions."""

    finalize_action: Optional[
        Literal["__end__", "__start_transfer__", "__transfer__"]
    ] = None
    finalize_action_kwargs: dict = Field(default_factory=dict)


class SubFlowParameters(BaseModel):
    """Parameters for initiating a sub-flow."""

    name: str
    arguments: dict


class MainAgentMetadata(MetadataBaseModel):
    """Metadata specific to the main agent."""

    start_sub_flow: bool = False
    sub_flow_data: Optional[SubFlowParameters] = None


class SubAgentMetadata(MetadataBaseModel):
    """Metadata specific to sub-agents."""

    finalize_success_status: bool = False
    exit_sub_flow: bool = False


class BaseAgentInterface(ABC):
    """Abstract base class defining the interface for an agent."""

    def __init__(
        self,
        history: List[Dict[str, str]],
        metadata: MetadataBaseModel,
        name: str,
        call_id: str,
        is_sub_agent: bool = False,
    ) -> None:
        """
        Initialize the base agent interface.

        Args:
            history: List of message dictionaries representing conversation history.
            metadata: Metadata model instance associated with the agent.
            name: Name identifier for the agent.
            call_id: Unique identifier for the call/session.
            is_sub_agent: Flag indicating whether this is a sub-agent.
        """
        self.metadata = metadata
        self.name = name
        self.is_sub_agent = is_sub_agent
        self.history = history
        self.generated_messages: List[Dict] = []
        self.generated_messages_per_step: List[Dict] = []
        self._debug_data_list: List[Dict] = []
        self.call_id = call_id

    @abstractmethod
    async def run_stream(
        self,
    ) -> AsyncGenerator[Tuple[InferenceEvent, None], Tuple[None, list]]:
        """
        Run the agent's main processing loop as an asynchronous stream.

        Yields:
            Tuples of InferenceEvent and None for outputs,
            and None and list for inputs.
        """
        pass

    @abstractmethod
    async def run_openai_stream(self) -> AsyncGenerator:
        """
        Run the agent's OpenAI streaming interface asynchronously.

        Yields:
            Streaming data from OpenAI API.
        """
        pass

    @abstractmethod
    async def run_voice_stream(
        self, websocket_client: object, stream_sid: str, call_info: dict
    ) -> AsyncGenerator:
        """
        Run a voice call pipeline over the given websocket client.

        Args:
            websocket_client: The websocket client to send/receive audio frames.
            stream_sid: Stream session identifier.
            call_info: Dictionary containing call metadata.

        Yields:
            Streaming audio frames or processing results.
        """
        pass

    def step_messages_collector(
        self,
        llm_step: Optional[Union[LLMCallStepInterface, PhantomStep]],
        to_supplement_history: bool = True,
    ) -> None:
        """
        Collect messages generated during a step and update history accordingly.

        Args:
            llm_step: The current LLM call or phantom step instance.
            to_supplement_history: Whether to append collected messages to overall history.
        """
        step_all_messages: List[Dict] = []

        if llm_step:
            if self.generated_messages_per_step:
                llm_step.add_output(self.generated_messages_per_step)
                self.generated_messages_per_step.clear()

            step_debug_data = llm_step.collect_debug_info()
            add_debug_data(step_debug_data, self._debug_data_list)

            step_all_messages = step_debug_data["outputs"]["value"]
        else:
            if self.generated_messages_per_step:
                step_all_messages = self.generated_messages_per_step.copy()
                self.generated_messages_per_step.clear()

        if to_supplement_history:
            self.generated_messages.extend(step_all_messages)

        # Debug output of generated data
        print("--------------------------------------------------------------")
        print("Generated data (outputs):\n", json.dumps(step_all_messages, indent=4))
        print("--------------------------------------------------------------")


class MainAgentInterface(BaseAgentInterface, ABC):
    """Interface for the main agent handling primary conversation flows."""

    def __init__(
        self,
        history: List[Dict[str, str]],
        name: str,
        call_id: str,
    ) -> None:
        """
        Initialize the main agent interface.

        Args:
            history: List of message dictionaries representing conversation history.
            name: Name identifier for the agent.
            call_id: Unique identifier for the call/session.
        """
        metadata = MainAgentMetadata()
        super().__init__(history, metadata, name, call_id, is_sub_agent=False)


class SubAgentInterface(BaseAgentInterface, ABC):
    """Interface for sub-agents managing sub-flows within a conversation."""

    def __init__(self, history: List[Dict[str, str]], name: str, call_id: str) -> None:
        """
        Initialize the sub-agent interface.

        Args:
            history: List of message dictionaries representing conversation history.
            name: Name identifier for the sub-agent.
            call_id: Unique identifier for the call/session.
        """
        metadata = SubAgentMetadata()
        super().__init__(history, metadata, name, call_id, is_sub_agent=True)

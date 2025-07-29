"""
This module handles inference and routing logic for ElevenLabs and general LLM-based agents,
including post-call analytics and platform-specific streaming behavior.
"""

import inspect
import json
import time
from datetime import datetime
from typing import List, AsyncGenerator, Optional, Any

from pipecat.frames.frames import TextFrame, EndFrame
from pipecat.processors.frame_processor import FrameProcessor

from agent_zero.api.helpers.generate_grouped_calendar import generate_grouped_calendar
from agent_zero.api.helpers.get_available_time_slots import get_available_time_slots
from agent_zero.api.helpers.next_business_dates import next_business_dates
from agent_zero.core.agent import Agent
from agent_zero.data.cache import (
    cache,
    init_cache,
    update_response_id,
    update_cache_retell_platform,
)
from agent_zero.data.consts import finalize_actions_phrases
from agent_zero.data.schemas import create_agent_inputs, ContentResponse
from agent_zero.helpers import add_debug_data


async def run_pipeline(pipeline: List[FrameProcessor]) -> AsyncGenerator[str, None]:
    """
    Runs a sequence of processing steps and yields text output from TextFrame instances.

    Args:
        pipeline (List[FrameProcessor]): List of processing steps.

    Yields:
        str: Text content from processed frames, each followed by a newline.
    """
    state: dict = {}

    for step in pipeline:
        iterator = step.process(None, state)  # May be coroutine or async generator

        if inspect.isasyncgen(iterator):
            async for frame in iterator:
                if isinstance(frame, TextFrame):
                    text = (
                        frame.text
                        if isinstance(frame.text, str)
                        else json.dumps(frame.text)
                    )
                    yield text + "\n"
                elif isinstance(frame, EndFrame):
                    break
        else:
            await iterator


async def frame_stream(pipeline: List[FrameProcessor]) -> AsyncGenerator[str, None]:
    """
    Streams frames from the pipeline as Server-Sent Events (SSE).

    Yields:
        str: Lines already starting with ``data: `` or encoded as JSON and
             terminated by ``\n\n`` so Starlette/StreamingResponse can push
             them verbatim.
    """
    state: dict = {}

    for step in pipeline:
        iterator = step.process(None, state)

        # coroutine → just await it
        if not inspect.isasyncgen(iterator):
            await iterator
            continue

        # async-generator → forward its yields
        async for frame in iterator:
            # Processor already produced a ready-to-send string
            if isinstance(frame, str):
                # Ensure proper SSE format with 'data:' prefix
                text = frame.rstrip("\n")
                if not text.startswith("data:"):
                    yield f"data: {text}\n\n"
                else:
                    yield f"{text}\n\n"

            # Classic TextFrame → wrap into OpenAI-style SSE
            elif isinstance(frame, TextFrame):
                payload = (
                    frame.text
                    if isinstance(frame.text, dict)
                    else {"content": frame.text}
                )
                yield f"data: {json.dumps(payload)}\n\n"

            # EndFrame → close the stream
            elif isinstance(frame, EndFrame):
                yield "data: [DONE]\n\n"


class AgentInputsProcessor(FrameProcessor):
    """
    Processes and normalizes agent input data in the pipeline state.
    """

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Normalizes agent inputs by replacing None or empty strings with "Unknown".

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state containing 'agent_inputs'.
        """
        agent_inputs_dict = {
            k: (
                "Unknown"
                if (v is None or (isinstance(v, str) and v.strip() == ""))
                else v
            )
            for k, v in state["agent_inputs"].model_dump().items()
        }
        state["agent_inputs"] = create_agent_inputs()


class SharedKnowledgeProcessor(FrameProcessor):
    """
    Adds current date and time information to shared knowledge in the pipeline state.
    """

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Updates shared knowledge with the current date and time string.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state containing 'agent_inputs'.
        """
        shared_knowledge = state["agent_inputs"].model_dump()
        shared_knowledge["current_date"] = datetime.now().strftime(
            "%Y-%m-%d, %A. Time: %H:%M."
        )
        state["shared_knowledge"] = shared_knowledge

class TL_SharedKnowledgeProcessor(FrameProcessor):
    """
    Adds current date and time information to shared knowledge in the pipeline state.
    """

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Updates shared knowledge with the current date and time string.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state containing 'agent_inputs'.
        """
        next_5_business_days = next_business_dates()
        slots = await get_available_time_slots(next_5_business_days)

        shared_knowledge = state["agent_inputs"].model_dump()
        shared_knowledge["current_date"] = datetime.now().strftime(
            "%Y-%m-%d, %A. Time: %H:%M."
        )
        shared_knowledge["slots_data"] = json.dumps(slots, indent=4)
        shared_knowledge["calendar"] = generate_grouped_calendar(datetime.now())
        state["shared_knowledge"] = shared_knowledge

class TransportInputProcessorElevenlabs(FrameProcessor):
    """
    Initializes pipeline state with ElevenLabs-specific request data.
    """

    def __init__(
        self, request_body: Any, call_id: str, conversation_history: List[Any]
    ) -> None:
        super().__init__()
        self.request_body = request_body
        self.call_id = call_id
        self.conversation_history = conversation_history

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Sets initial ElevenLabs-specific data in the pipeline state.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state to update.
        """
        state["request_body"] = self.request_body
        state["call_id"] = self.call_id
        state["conversation_history"] = self.conversation_history


class InitCacheProcessorElevenlabs(FrameProcessor):
    """
    Initializes cache state for ElevenLabs platform, treating all requests as retell platform.
    """

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Updates cache and pipeline state for ElevenLabs retell platform.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with 'call_id', 'request_body', and 'conversation_history'.
        """
        update_cache_retell_platform(
            call_id=state["call_id"],
            agent_inputs=state["request_body"].agent_inputs,
            conversation_history=state["conversation_history"],
        )
        state["metadata"] = cache[state["call_id"]]["metadata"]
        state["agent_inputs"] = cache[state["call_id"]]["agent_inputs"]


class TransportInputProcessorInference(FrameProcessor):
    """
    Initializes pipeline state with general inference request data.
    """

    def __init__(
        self,
        request_body: Any,
        call_id: str,
        platform_metadata: Optional[Any],
        conversation_history: List[Any],
        active_flow: Any,
    ) -> None:
        super().__init__()
        self.request_body = request_body
        self.call_id = call_id
        self.platform_metadata = platform_metadata
        self.conversation_history = conversation_history
        self.active_flow = active_flow

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Sets inference-related data in the pipeline state.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state to update.
        """
        state["request_body"] = self.request_body
        state["call_id"] = self.call_id
        state["platform_metadata"] = self.platform_metadata
        state["conversation_history"] = self.conversation_history
        state["active_flow"] = self.active_flow


class InitCacheProcessorInference(FrameProcessor):
    """
    Initializes or updates cache state based on platform metadata for inference requests.
    """

    async def process(self, frame: Optional[Any], state: dict) -> None:
        """
        Updates cache based on platform metadata, handling retell platform specially.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with keys 'platform_metadata', 'call_id', 'request_body', etc.
        """
        init_cache(
            query=state["request_body"].query,
            call_id=state["call_id"],
            metadata=state["request_body"].metadata,
            agent_inputs=state["request_body"].agent_inputs,
            conversation_history=state["conversation_history"],
            active_flow=state["active_flow"],
        )
        state["metadata"] = cache[state["call_id"]]["metadata"]
        state["agent_inputs"] = cache[state["call_id"]]["agent_inputs"]


class AgentPlainStreamingProcessor(FrameProcessor):
    """
    Processes LLM stream output and aggregates chunks into a full text message.
    """

    def __init__(self, model: Any) -> None:
        super().__init__()
        self.model = model

    async def process(
        self, frame: Optional[Any], state: dict
    ) -> AsyncGenerator[Any, None]:
        """
        Collects streaming chunks from the Agent and yields a single TextFrame followed by EndFrame.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with conversation and agent info.

        Yields:
            TextFrame: Aggregated full message.
            EndFrame: Indicates end of processing.
        """
        chunks: List[str] = []
        agent = Agent(
            model=self.model,
            history=state["conversation_history"],
            name=state["agent_inputs"].project_name,
            call_id=state["call_id"],
            conversation_knowledge=state["shared_knowledge"],
        )

        async for chunk_event, _ in agent.run_stream():
            if chunk_event:
                chunks.append(str(chunk_event.content))

        full_message = " ".join(chunks).strip()
        yield TextFrame(full_message)
        yield EndFrame()


class AgentPlatformStreamingProcessor(FrameProcessor):
    """
    Processes LLM stream output with optional streaming, collects debug data,
    and yields frames formatted for platform consumption.
    """

    def __init__(self, model: Any, stream: bool) -> None:
        super().__init__()
        self.model = model
        self.stream = stream

    async def process(
        self, frame: Optional[Any], state: dict
    ) -> AsyncGenerator[Any, None]:
        """
        Processes streaming output from Agent, yields JSON frames if streaming,
        otherwise aggregates and yields a single JSON text frame.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with conversation and agent info.

        Yields:
            str or TextFrame: Streaming JSON frames or aggregated JSON text frame.
            EndFrame: Indicates end of processing.
        """
        all_debug_data: List[dict] = []

        agent = Agent(
            model=self.model,
            history=state["conversation_history"],
            name=state["agent_inputs"].project_name,
            call_id=state["call_id"],
            conversation_knowledge=state["shared_knowledge"],
        )

        async for chunk_event, debug_data in agent.run_stream():
            if debug_data:
                add_debug_data(debug_data, all_debug_data)
            if chunk_event and self.stream:
                yield f"{json.dumps(chunk_event.model_dump(), indent=4)}\n\n"

        cache[state["call_id"]]["metadata"].history.extend(agent.generated_messages)
        cache[state["call_id"]]["metadata"].generated_messages_per_turn.extend(
            agent.generated_messages
        )

        if finalize_action := agent.metadata.finalize_action:
            cache[state["call_id"]]["metadata"].finalize_action = finalize_action
            cache[state["call_id"]][
                "metadata"
            ].finalize_action_kwargs = agent.metadata.finalize_action_kwargs
            print(
                f"Finalizing action: {cache[state['call_id']]['metadata'].finalize_action}"
            )

        if cache[state["call_id"]]["metadata"].finalize_action and self.stream:
            chunk = ContentResponse(
                content=cache[state["call_id"]]["metadata"].finalize_action
            ).model_dump()
            yield f"data: {json.dumps(chunk, indent=4)}\n\n"

        if not self.stream:
            generated_content: List[str] = []
            for data in all_debug_data:
                if data["title"] != "Generate intent":
                    if data["type"] == "LLM":
                        messages = data["outputs"]["value"]
                        for message in messages:
                            if message["role"] == "assistant":
                                generated_content.append(message["content"])
                    if data["type"] == "phantom step":
                        output = data["outputs"]["value"]
                        generated_content.append(output)

            if action := cache[state["call_id"]]["metadata"].finalize_action:
                generated_content.extend(
                    [
                        finalize_actions_phrases[
                            state["shared_knowledge"]["language_code"]
                        ][action]
                    ]
                )

            yield TextFrame(
                json.dumps(
                    {
                        "model": self.model.original_name,
                        "message": '\n\n'.join([item for item in generated_content if item != "none"]),
                        "steps": all_debug_data,
                        "error": None,
                        "metadata": cache[state["call_id"]]["metadata"].model_dump(),
                    }
                )
            )

        yield EndFrame()


class AgentPlatformStreamingProcessorElevenlabs(FrameProcessor):
    """
    Processes LLM stream output with optional streaming, collects debug data,
    and yields frames formatted for platform consumption.
    """

    def __init__(self, model: Any, stream: bool) -> None:
        super().__init__()
        self.model = model
        self.stream = stream

    async def process(
        self, frame: Optional[Any], state: dict
    ) -> AsyncGenerator[Any, None]:
        """
        Processes streaming output from Agent, yields JSON frames if streaming,
        otherwise aggregates and yields a single JSON text frame.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with conversation and agent info.

        Yields:
            str or TextFrame: Streaming JSON frames or aggregated JSON text frame.
            EndFrame: Indicates end of processing.
        """
        chunks: List[str] = []
        all_debug_data: List[dict] = []

        agent = Agent(
            model=self.model,
            history=state["conversation_history"],
            name=state["agent_inputs"].project_name,
            call_id=state["call_id"],
            conversation_knowledge=state["shared_knowledge"],
        )

        async for chunk_event, debug_data in agent.run_stream():
            if debug_data:
                add_debug_data(debug_data, all_debug_data)
            if chunk_event and self.stream:
                text = str(chunk_event.content)
                chunk = {
                    "id": state["call_id"],
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": getattr(self.model, "original_name", ""),
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": text},
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(chunk)}\n\n"

        if self.stream:
            # Stream termination signal for SSE
            yield "data: [DONE]\n\n"
            return

        cache[state["call_id"]]["metadata"].history.extend(agent.generated_messages)
        cache[state["call_id"]]["metadata"].generated_messages_per_turn.extend(
            agent.generated_messages
        )

        if finalize_action := agent.metadata.finalize_action:
            cache[state["call_id"]]["metadata"].finalize_action = finalize_action
            cache[state["call_id"]][
                "metadata"
            ].finalize_action_kwargs = agent.metadata.finalize_action_kwargs
            print(
                f"Finalizing action: {cache[state['call_id']]['metadata'].finalize_action}"
            )

        if cache[state["call_id"]]["metadata"].finalize_action and self.stream:
            chunk = ContentResponse(
                content=cache[state["call_id"]]["metadata"].finalize_action
            ).model_dump()
            yield f"data: {json.dumps(chunk, indent=4)}\n\n"

        if not self.stream:
            generated_content: List[str] = []
            for data in all_debug_data:
                print(f"generated_content in iterator: {generated_content}")
                if data["title"] != "Generate intent":
                    if data["type"] == "LLM":
                        messages = data["outputs"]["value"]
                        for message in messages:
                            if message["content"] and message["role"] == "assistant":
                                generated_content.append(message["content"])
                    elif data["type"] == "phantom step":
                        output = data["outputs"]["value"]
                        if output:
                            generated_content.append(output)

            if action := cache[state["call_id"]]["metadata"].finalize_action:
                generated_content.extend(
                    [
                        finalize_actions_phrases[
                            state["shared_knowledge"]["language_code"]
                        ][action]
                    ]
                )

            yield TextFrame(
                json.dumps(
                    {
                        "model": self.model.original_name,
                        "message": " ".join(
                            item
                            for item in generated_content
                            if item not in [None, "none"]
                        ).strip(),
                        "steps": all_debug_data,
                        "error": None,
                        "metadata": cache[state["call_id"]]["metadata"].model_dump(),
                    }
                )
            )

        yield EndFrame()


class AgentVoiceProcessor(FrameProcessor):
    """
    Processes LLM output for voice call pipelines, emitting audio frames via websocket.

    Args:
        call_id (str): Identifier for the call.
        model (Any): Model instance used for inference.
        websocket_client (Any): Websocket client to send audio frames.
        stream_sid (Any): Stream session identifier.
        call_info (dict): Optional additional call information.
    """

    def __init__(
        self,
        call_id: str,
        model: Any,
        websocket_client: Any,
        stream_sid: Any,
        call_info: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.call_id = call_id
        self.model = model
        self.websocket_client = websocket_client
        self.stream_sid = stream_sid
        self.call_info = call_info or {}

    async def process(
        self, frame: Optional[Any], state: dict
    ) -> AsyncGenerator[Any, None]:
        """
        Runs the Agent voice stream and yields audio frames.

        Args:
            frame: Input frame (not used).
            state (dict): Pipeline state with metadata and agent inputs.

        Yields:
            Audio frames streamed from the Agent.
            EndFrame: Indicates end of processing.
        """
        agent = Agent(
            model=self.model,
            history=state["metadata"].history,
            name=state["agent_inputs"].project_name,
            call_id=self.call_id,
            conversation_knowledge=state["shared_knowledge"],
        )

        async for audio_frame in agent.run_voice_stream(
            self.websocket_client, self.stream_sid, self.call_info
        ):
            yield audio_frame
        yield EndFrame()

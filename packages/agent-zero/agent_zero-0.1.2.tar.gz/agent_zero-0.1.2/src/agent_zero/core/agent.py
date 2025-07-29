"""Inference module for voice agent pipeline.

This module provides the core Agent and AgentLLMService classes for orchestrating
voice-based LLM interactions, including streaming, tool-calling, and context aggregation.
"""

import asyncio
import json
import os
import re
import time
from typing import AsyncGenerator, Tuple, Optional, Any

# Third-party imports
from deepgram import LiveOptions

from pipecat.frames.frames import (
    TextFrame,
    LLMFullResponseStartFrame,
    LLMFullResponseEndFrame,
    LLMMessagesFrame,
    TTSSpeakFrame,
)
from pipecat.processors.frame_processor import FrameDirection
from pipecat.services.llm_service import LLMService
from pipecat.services.openai.llm import (
    OpenAIContextAggregatorPair,
    OpenAIUserContextAggregator,
    OpenAIAssistantContextAggregator,
)
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams,
)
from pipecat.audio.mixers.soundfile_mixer import SoundfileMixer
from pipecat.serializers.twilio import TwilioFrameSerializer
from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContext,
    OpenAILLMContextFrame,
)
from connexity.metrics.pipecat import ConnexityTwilioObserver

# Application-specific imports
from agent_zero.core.llm.GroqGPTBaseModel import GroqGPTBaseModel
from agent_zero.core.llm.steps.Steps.PhantomStep import PhantomStep
from agent_zero.core.llm.steps.Steps.AsyncLLMCallStepBase import AsyncLLMCallStepBase
from agent_zero.core.llm.steps.Steps.AsyncLLMCallStepBaseStream import AsyncLLMCallStepBaseStream
from agent_zero.core.tools import get_function_handlers, get_functions_meta
from agent_zero.helpers.get_model import get_model
from agent_zero.core.config import get_config
from agent_zero.helpers import create_openai_chunk
from agent_zero.data.schemas import (
    ToolCallInvocationResponse,
    ToolCallResultResponse,
    ContentResponse,
)
from agent_zero.core.agent_interface import MainAgentInterface
from agent_zero.core.prompts import get_prompt, PromptType
from agent_zero.data.consts import (
    OPENAI_API_KEY,
    BACKGROUND_AUDIO_DICT,
    CONNEXITY_API_KEY, TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_ID
)
from agent_zero.core.pipecat_w_twillio.get_tts_service import (
    get_tts_service,
)
from agent_zero.core.pipecat_w_twillio.EndCallProcessor import (
    EndCallProcessor,
)
from agent_zero.core.pipecat_w_twillio.initiate_vad_params import (
    initiate_vad_params,
)
from agent_zero.data.cache import set_call_status


class Agent(MainAgentInterface):
    """
    Main conversational agent for orchestrating LLM-driven voice interactions.

    Handles prompt construction, streaming LLM responses, tool invocation, and
    context aggregation for the voice agent pipeline.
    """

    def __init__(
        self,
        model: GroqGPTBaseModel,
        history: list[dict[str, str]],
        name: str,
        call_id: str,
        conversation_knowledge: dict,
    ) -> None:
        """
        Initialize the Agent.

        Args:
            model (GroqGPTBaseModel): The LLM model to use.
            history (list[dict[str, str]]): Conversation history.
            name (str): Name of the agent.
            call_id (str): Unique call identifier.
            conversation_knowledge (dict): Project and session knowledge.
        """
        if len(history) and "role" in history[0] and history[0]["role"] == "system":
            self.system_prompt = history.pop(0)["content"]

        super().__init__(history, name, call_id)
        self.llm = model
        self.technical_llm = get_model(
            get_config()["llm"]["utils"]["vendor"],
            get_config()["llm"]["utils"]["model"],
            openai_key=OPENAI_API_KEY,
        )
        self.conversation_knowledge = conversation_knowledge

        # Mapping of tool names to internal functions
        self._internal_tools_mapping = get_function_handlers(get_config()["tools"])

        # Buffers and state for streaming and tool-calling
        self.collected_chunks: list = []
        self.previous_content: str = ""
        self.current_content: str = ""
        self.task_done: bool = False

        self.special_token_started: bool = False
        self.special_token: Optional[str] = None

        self.parentheses_phrase_started: bool = False

        self.assistant_message_content: str = ""
        self.first_sentence_generated: bool = False

        # Buffers to collect tool call information during streaming
        self.function_calls_buffer: list = []
        self.current_function_call: Optional[dict] = None
        self.has_tool_calls: bool = False
        self.tools_configuration = get_functions_meta(get_config()["tools"])
        print(f"TOOLS: {self.tools_configuration}")

    def _create_messages(self) -> list[dict[str, str]]:
        """
        Construct messages for the LLM call, including system prompt and conversation history.

        Returns:
            list[dict[str, str]]: List of message dicts for LLM input.
        """
        if self.conversation_knowledge["translate_prompt"]:
            prompt_str = get_prompt(
                PromptType.AGENT,
                self.conversation_knowledge["language_code"],
            )
            prompt = prompt_str.format(**self.conversation_knowledge)
        else:
            prompt_str = get_prompt(PromptType.AGENT)
            prompt = prompt_str.format(**self.conversation_knowledge)

        return [
            {
                "role": "system",
                "content": (
                    self.system_prompt
                    if hasattr(self, "system_prompt") and self.system_prompt
                    else prompt
                ),
            },
            *self.history,
            *self.generated_messages,
        ]

    def _create_quick_response_messages(self) -> list[dict[str, str]]:
        """
        Construct messages for generating a quick response.

        Returns:
            list[dict[str, str]]: List of message dicts for quick response.
        """
        prompt_str = get_prompt(
            PromptType.QUICK_RESPONSE,
            self.conversation_knowledge["language_code"],
        )
        prompt = prompt_str.format(
            message=self.history[-1]["content"],
            assistant_message=(
                self.history[-2]["content"] if len(self.history) >= 2 else ""
            ),
        )

        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "..."},
        ]

    async def get_quick_response(
        self,
    ) -> Tuple[Optional[str], PhantomStep | None]:
        """
        Generates a quick response (fallback or filler) using a technical LLM.

        Returns:
            Tuple[Optional[str], PhantomStep]: The quick response string (or None) and a PhantomStep for message collection.
        """
        messages = self._create_quick_response_messages()

        technical_llm_call_step = AsyncLLMCallStepBase(
            stage_name=self.name,
            step_name="Generate quick response",
            llm=self.technical_llm,
            top_p=0.05,
            temperature=1,
            messages=messages,
        )

        replica, _ = await technical_llm_call_step.process()
        normalized_replica = replica.strip().strip('"').strip("'")
        if replica and normalized_replica.lower() in ["none", "...", ".", "''", '""', None]:
            quick_response = None
        else:
            quick_response = normalized_replica

        self.step_messages_collector(
            technical_llm_call_step, to_supplement_history=False
        )

        return quick_response, None

    async def run_and_collect_functions_from_llm_step(
        self, llm_call_step: AsyncLLMCallStepBaseStream
    ) -> None:
        """
        Runs the LLM call step as a stream, collecting output chunks and any tool/function calls.

        Args:
            llm_call_step (AsyncLLMCallStepBaseStream): The LLM streaming step to process.
        """
        # Ensure tool call buffer is initialized for this run
        if not hasattr(self, "function_calls_buffer"):
            self.function_calls_buffer = []

        async for chunk in llm_call_step.process():
            self.collected_chunks.append(chunk)
            delta = chunk.choices[0].delta
            print(delta, flush=True)

            if content := delta.content:
                self.assistant_message_content += content
                self.current_content += content

            # Detect when the first full sentence is generated for early streaming
            if not self.first_sentence_generated and re.search(
                r"[.!?](?:\s|$)", self.current_content
            ):
                print(f"Sentence generated: {self.current_content}", flush=True)
                self.first_sentence_generated = True

            # Collect tool/function calls as they arrive
            if tool_calls := getattr(delta, "tool_calls", None):
                self.has_tool_calls = True
                for tool_call in tool_calls:
                    if tool_call.index is not None:
                        if len(self.function_calls_buffer) <= tool_call.index:
                            self.function_calls_buffer.append(
                                {
                                    "function": {"name": "", "arguments": ""},
                                    "id": tool_call.id,
                                }
                            )
                        self.current_function_call = self.function_calls_buffer[
                            tool_call.index
                        ]

                        if hasattr(tool_call, "function"):
                            if tool_call.function.name:
                                self.current_function_call["function"][
                                    "name"
                                ] = tool_call.function.name
                            if tool_call.function.arguments:
                                self.current_function_call["function"][
                                    "arguments"
                                ] += tool_call.function.arguments

                        elif "function" in tool_call:
                            if tool_call["function"].get("name"):
                                self.current_function_call["function"]["name"] = (
                                    tool_call["function"].get("name")
                                )
                            if tool_call["function"].get("arguments"):
                                self.current_function_call["function"][
                                    "arguments"
                                ] += tool_call["function"].get("arguments")

    async def run_openai_stream(self) -> AsyncGenerator[Tuple[Any, Any], None]:
        """
        Streams OpenAI LLM responses as output chunks, optionally yielding a quick response first.

        Yields:
            Tuple[Any, Any]: Each yielded tuple contains (chunk, None) or (None, debug_data).
        """
        messages = self._create_messages()

        llm_call_step = AsyncLLMCallStepBaseStream(
            stage_name=self.name,
            step_name="LLM Call Step",
            llm=self.llm,
            top_p=0.15,
            temperature=1,
            messages=messages,
            tools=self.tools_configuration,
            tool_choice="auto",
            parallel_tool_calls=True,
        )

        self.collected_chunks = []
        last_yielded_chunk_idx = 0

        # Start quick response and main LLM stream in parallel
        quick_response_task = asyncio.create_task(self.get_quick_response())
        main_agent_task = asyncio.create_task(
            self.run_and_collect_functions_from_llm_step(llm_call_step)
        )
        quick_response_task_done = False

        while not main_agent_task.done():
            if not quick_response_task_done and quick_response_task.done():
                quick_response_task_done = True
                quick_response, phantom_step = quick_response_task.result()
                # Yield quick response if main sentence not yet generated
                if not self.first_sentence_generated and quick_response:
                    print("Yielding quick response....", flush=True)
                    self.step_messages_collector(
                        phantom_step, to_supplement_history=False
                    )
                    quick_response_chunk = create_openai_chunk(quick_response)
                    yield quick_response_chunk, None

            # Yield new chunks as they become available after first sentence
            if (
                last_yielded_chunk_idx < len(self.collected_chunks)
                and self.first_sentence_generated
            ):
                for chunk in self.collected_chunks[last_yielded_chunk_idx:]:
                    yield chunk, None
                last_yielded_chunk_idx = len(self.collected_chunks)
            await asyncio.sleep(0.005)

        if last_yielded_chunk_idx < len(self.collected_chunks):
            for chunk in self.collected_chunks[last_yielded_chunk_idx:]:
                yield chunk, None

        yield None, self._debug_data_list

    async def run_stream(self) -> AsyncGenerator[
        Tuple[Any, Any],
        None,
    ]:
        """
        Main streaming coroutine for the agent, yielding content or tool call responses as events.

        Yields:
            Tuple[Any, Any]: Each yielded tuple contains (event, None) or (None, debug_data).
        """
        if self.history and self.history[-1]["role"] == "user":
            first_run = True
        else:
            first_run = False

        while True:
            background_tasks = []
            background_tools_ids = []

            self.assistant_message_content = ""

            # Re-initialize tool call buffers and flags for each run
            self.function_calls_buffer = []
            self.current_function_call = None
            self.has_tool_calls = False
            mapped_tools_called = False
            messages = self._create_messages()

            llm_call_step = AsyncLLMCallStepBaseStream(
                stage_name=self.name,
                step_name="LLM Call Step",
                llm=self.llm,
                top_p=0.15,
                temperature=1,
                messages=messages,
                tools=self.tools_configuration,
                tool_choice="auto",
            )

            if first_run:
                quick_response_task = asyncio.create_task(self.get_quick_response())
                main_agent_task = asyncio.create_task(
                    self.run_and_collect_functions_from_llm_step(llm_call_step)
                )

                quick_response_task_done = False

                while not main_agent_task.done():
                    if not quick_response_task_done and quick_response_task.done():
                        quick_response_task_done = True
                        quick_response, phantom_step = quick_response_task.result()

                        if not self.first_sentence_generated and quick_response:
                            print(f"Yielding quick response....")
                            self.step_messages_collector(
                                phantom_step, to_supplement_history=False
                            )
                            yield ContentResponse(content=quick_response), None

                    if self.previous_content != self.current_content:
                        difference = self.current_content[len(self.previous_content) :]
                        yield ContentResponse(content=difference), None

                        self.previous_content = self.current_content
                    await asyncio.sleep(0.005)

                if self.previous_content != self.current_content:
                    difference = self.current_content[len(self.previous_content) :]

                    yield ContentResponse(content=difference), None
            else:
                async for chunk in llm_call_step.process():
                    delta = chunk.choices[0].delta

                    if content := delta.content:
                        self.assistant_message_content += content
                        self.current_content += content
                        yield ContentResponse(content=content), None

                    if tool_calls := getattr(delta, "tool_calls", None):
                        self.has_tool_calls = True
                        for tool_call in tool_calls:
                            if tool_call.index is not None:
                                if len(self.function_calls_buffer) <= tool_call.index:
                                    self.function_calls_buffer.append(
                                        {
                                            "function": {
                                                "name": tool_call.function.name,
                                                "arguments": tool_call.function.arguments,
                                            },
                                            "id": tool_call.id,
                                        }
                                    )
                                self.current_function_call = self.function_calls_buffer[
                                    tool_call.index
                                ]

                                if hasattr(tool_call, "function"):
                                    if tool_call.function.name:
                                        self.current_function_call["function"][
                                            "name"
                                        ] = tool_call.function.name
                                    if tool_call.function.arguments:
                                        self.current_function_call["function"][
                                            "arguments"
                                        ] += tool_call.function.arguments

                                elif "function" in tool_call:
                                    if tool_call["function"].get("name"):
                                        self.current_function_call["function"][
                                            "name"
                                        ] = tool_call["function"].get("name")
                                    if tool_call["function"].get("arguments"):
                                        self.current_function_call["function"][
                                            "arguments"
                                        ] += tool_call["function"].get("arguments")

            assistant_message = {
                "role": "assistant",
                "content": self.assistant_message_content,
            }

            if self.has_tool_calls:
                tool_calls = []
                background_tasks = []
                background_tools_ids = []

                for function_call in self.function_calls_buffer:
                    tool_name = function_call["function"]["name"]
                    fn_arguments = function_call["function"]["arguments"]
                    tool_id = function_call["id"]

                    try:
                        arguments = json.loads(fn_arguments or "{}")
                    except (json.JSONDecodeError, TypeError):
                        arguments = {}

                    if tool_name == "end_call":
                        self.metadata.finalize_action = "__end__"
                        self.metadata.finalize_action_kwargs["call_concluded"] = True

                    elif tool_name in self._internal_tools_mapping:
                        if tool_name == "transfer_call":
                            self.metadata.finalize_action_kwargs["call_concluded"] = (
                                True
                            )

                        mapped_tools_called = True
                        tool_call_event = ToolCallInvocationResponse(
                            tool_call_id=tool_id,
                            name=tool_name,
                            arguments=json.dumps(arguments, indent=4),
                        )
                        yield tool_call_event, None

                        tool_calls.append(
                            {
                                "id": tool_id,
                                "type": "function",
                                "function": {"name": tool_name, "arguments": arguments},
                            }
                        )

                        function_to_call = self._internal_tools_mapping[tool_name]
                        background_tasks.append(
                            asyncio.create_task(function_to_call(**arguments))
                        )
                        background_tools_ids.append(tool_id)

                if tool_calls:
                    assistant_message["tool_calls"] = tool_calls

                self.generated_messages_per_step.append(assistant_message)

                if background_tasks:
                    completed_tool_results, _ = await asyncio.wait(background_tasks)
                    tool_results = [
                        await tool_result for tool_result in completed_tool_results
                    ]

                    finished_background_tools = [
                        {
                            "role": "tool",
                            "content": (
                                json.dumps(tool_result, indent=4)
                                if type(tool_result) in [dict, list]
                                else tool_result
                            ),
                            "tool_call_id": tool_id,
                        }
                        for tool_id, tool_result in zip(
                            background_tools_ids, tool_results
                        )
                    ]

                    for tool in finished_background_tools:
                        tool_call_result_event = ToolCallResultResponse(
                            tool_call_id=tool["tool_call_id"], content=tool["content"]
                        )
                        yield tool_call_result_event, None
                    self.generated_messages_per_step.extend(finished_background_tools)
            else:
                self.generated_messages_per_step.append(assistant_message)

            self.step_messages_collector(llm_call_step)

            first_run = False

            if not mapped_tools_called:
                break

        yield None, self._debug_data_list

    async def run_voice_stream(
        self,
        websocket_client: Any,
        stream_sid: str,
        call_info: dict = {},
    ) -> None:
        """
        Runs the full voice agent pipeline for a websocket client and audio stream.

        Args:
            websocket_client (Any): The websocket client connection.
            stream_sid (str): The stream session ID.
            call_info (dict): Call metadata and configuration.
        """
        start_time = time.time()
        set_call_status(call_info.get("sid"), "in-progress")

        selected_sound = call_info.get("background_noise")

        default_sound = (
            selected_sound if selected_sound in BACKGROUND_AUDIO_DICT.keys() else "test"
        )

        soundfile_mixer = SoundfileMixer(
            sound_files=BACKGROUND_AUDIO_DICT,
            default_sound=default_sound,
            volume=0.5,
        )

        vad_params = initiate_vad_params()

        transport = FastAPIWebsocketTransport(
            websocket=websocket_client,
            params=FastAPIWebsocketParams(
                audio_out_enabled=True,
                audio_out_mixer=(
                    soundfile_mixer if call_info.get("background_noise") else None
                ),
                add_wav_header=False,
                audio_in_enabled=True,
                vad_analyzer=SileroVADAnalyzer(params=vad_params),
                audio_in_passthrough=True,
                serializer=TwilioFrameSerializer(stream_sid),
            ),
        )

        print(self.conversation_knowledge)
        # Use appropriate Deepgram model for language (TODO: update when multi-language supported)
        if self.conversation_knowledge["language_code"] != "en":
            live_options = LiveOptions(
                model="nova-2-general",
                language=self.conversation_knowledge["language_code"],
            )
        else:
            live_options = None

        stt = DeepgramSTTService(
            api_key=os.getenv("DEEPGRAM_API_KEY"), live_options=live_options
        )

        tts = get_tts_service(call_info)

        agent_llm_service = AgentLLMService(self)

        context = OpenAILLMContext(self.history)
        context_aggregator = agent_llm_service.create_context_aggregator(context)

        # EndCallProcessor with static seconds (should be made dynamic if needed)
        end_call = EndCallProcessor(
            start_time=start_time, sid=call_info.get("sid"), seconds=300
        )

        pipeline = Pipeline(
            [
                transport.input(),
                stt,
                context_aggregator.user(),
                agent_llm_service,
                end_call,
                tts,
                transport.output(),
                context_aggregator.assistant(),
            ]
        )

        connexity_metrics_observer = ConnexityTwilioObserver()
        await connexity_metrics_observer.initialize(sid=self.call_id,
                             api_key=CONNEXITY_API_KEY,
                             agent_id=get_config()["agent_id"],
                             agent_phone_number=call_info.get("to"),
                             user_phone_number=call_info.get("from"),
                             phone_call_provider='twilio',
                             twilio_account_sid=TWILIO_ACCOUNT_ID,
                             twilio_auth_token=TWILIO_AUTH_TOKEN,
                             voice_provider='11labs',
                             llm_model=get_config()["llm"]["utils"]["model"],
                             llm_provider=get_config()["llm"]["utils"]["vendor"],
                             call_type=call_info.get('call_type'),
                             transcriber='deepgram')

        task = PipelineTask(
            pipeline,
            params=PipelineParams(audio_in_sample_rate=8000, allow_interruptions=True),
            observers=[connexity_metrics_observer]
        )

        @transport.event_handler("on_client_connected")
        async def on_client_connected(transport, client):
            """
            Sends a greeting or initial message when the client connects.
            """
            if get_config()["start_message"]:
                await task.queue_frames([TTSSpeakFrame(get_config()["start_message"])])
            else:
                await task.queue_frames([LLMMessagesFrame(self.history)])

        @transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, client):
            """
            Cancels the task and marks call as completed on disconnect.
            """
            await task.cancel()
            set_call_status(call_info.get("sid"), "completed")

        runner = PipelineRunner(handle_sigint=False, force_gc=True)

        await runner.run(task)


class AgentLLMService(LLMService):
    """
    Pipecat processor that calls Agent.run_stream() and streams each content chunk as a TextFrame.
    Mirrors InferenceCall logic to preserve LLMService metrics and start/end frames.
    """

    def __init__(self, agent: "Agent") -> None:
        """
        Args:
            agent (Agent): The conversational agent instance.
        """
        super().__init__()
        self.agent = agent

    async def _stream_llm(self, context: OpenAILLMContext) -> None:
        """
        Iterate over the agent's async generator (run_stream) which yields
        (chunk_event, debug_data) tuples. Only forwards textual ContentResponse as TextFrame.

        Args:
            context (OpenAILLMContext): The LLM context for the session.
        """
        await self.start_ttfb_metrics()

        async for chunk_event, _ in self.agent.run_stream():
            if chunk_event is None:
                continue

            # Only forward ContentResponse as TextFrame
            if isinstance(chunk_event, ContentResponse):
                content = chunk_event.content
                if content:
                    await self.stop_ttfb_metrics()
                    await self.push_frame(TextFrame(content))

        # Ensure TTFT metrics are stopped even if no content arrived
        await self.stop_ttfb_metrics()

    async def process_frame(self, frame: Any, direction: FrameDirection) -> None:
        """
        Orchestrates frame processing: identifies context, wraps with LLMFullResponseStart/End frames,
        and propagates all other frames unchanged.

        Args:
            frame (Any): The frame to process.
            direction (FrameDirection): The direction of frame flow.
        """
        await super().process_frame(frame, direction)

        context = None
        if isinstance(frame, OpenAILLMContextFrame):
            context = frame.context
        elif isinstance(frame, LLMMessagesFrame):
            context = OpenAILLMContext.from_messages(frame.messages)
        else:
            await self.push_frame(frame, direction)

        if context:
            await self.push_frame(LLMFullResponseStartFrame())
            await self.start_processing_metrics()
            await self._stream_llm(context)
            await self.stop_processing_metrics()
            await self.push_frame(LLMFullResponseEndFrame())

    def can_generate_metrics(self) -> bool:
        """
        Indicates that this service can generate metrics.

        Returns:
            bool: True if metrics can be generated.
        """
        return True

    @staticmethod
    def create_context_aggregator(
            context: OpenAILLMContext, *, assistant_expect_stripped_words: bool = True
    ) -> OpenAIContextAggregatorPair:
        user = OpenAIUserContextAggregator(context)
        assistant = OpenAIAssistantContextAggregator(
            context, expect_stripped_words=assistant_expect_stripped_words
        )
        return OpenAIContextAggregatorPair(_user=user, _assistant=assistant)

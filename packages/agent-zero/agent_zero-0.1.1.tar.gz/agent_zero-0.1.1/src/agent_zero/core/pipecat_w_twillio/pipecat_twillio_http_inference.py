import json
import typing
from copy import copy

import aiohttp
from loguru import logger
from pipecat.frames.frames import (
    TextFrame,
    Frame,
    LLMFullResponseEndFrame,
    LLMFullResponseStartFrame,
    VisionImageRawFrame,
)
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContextFrame
from pipecat.processors.frame_processor import FrameDirection
from pipecat.services.llm_service import LLMService
from pipecat.services.openai.llm import (
    OpenAIContextAggregatorPair,
    OpenAIUserContextAggregator,
    OpenAIAssistantContextAggregator,
)

import os
import time

from deepgram import LiveOptions
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMMessagesFrame, TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams,
)
from pipecat.audio.mixers.soundfile_mixer import SoundfileMixer
from pipecat.serializers.twilio import TwilioFrameSerializer
from dotenv import load_dotenv

from agent_zero.core.pipecat_w_twillio.EndCallProcessor import (
    EndCallProcessor,
)
from agent_zero.core.pipecat_w_twillio.get_tts_service import (
    get_tts_service,
)
from agent_zero.core.pipecat_w_twillio.initiate_vad_params import (
    initiate_vad_params,
)
from agent_zero.data.consts import BACKGROUND_AUDIO_DICT, INFERENCE_URL

load_dotenv(override=True)


from agent_zero.core.pipecat_w_twillio.accumulate_last_assistant_user_messages import (
    accumulate_last_assistant_user_messages,
)


class InferenceCall(LLMService):
    """This is the base for all services that use the AsyncOpenAI client.

    This service consumes OpenAILLMContextFrame frames, which contain a reference
    to an OpenAILLMContext frame. The OpenAILLMContext object defines the context
    sent to the LLM for a completion. This includes user, assistant and system messages
    as well as tool choices and the tool, which is used if requesting function
    calls from the LLM.
    """

    def __init__(
        self, model: str, inference_url: str, prompt: str, inputs: dict, sid: str
    ):
        super().__init__()
        self._model: str = model
        self.inputs = inputs
        self.inference_url = inference_url
        self.sid = sid
        self.prompt = prompt

    async def _stream_chat_completions(
        self, context: OpenAILLMContext
    ) -> typing.AsyncGenerator:
        # messages: List[ChatCompletionMessageParam] = context.get_messages()
        logger.debug(f"Generating chat: {context.get_messages_json()}")

        headers = {"Content-Type": "application/json"}
        body = copy(self.inputs)
        body["model"] = self._model
        body["history"] = context.messages
        body["conversation_id"] = self.sid
        body["stream"] = True
        user_content, assistant_content = accumulate_last_assistant_user_messages(
            context.messages
        )
        body["query"] = user_content
        body["last_assistant_message"] = assistant_content
        body["prompt"] = self.prompt
        body["inputs"] = self.inputs

        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.post(
                self.inference_url, headers=headers, data=json.dumps(body)
            ) as response:
                response.raise_for_status()
                first_chunk_time = None
                async for chunk in response.content.iter_any():
                    if chunk:
                        if first_chunk_time is None:
                            first_chunk_time = time.time()
                            latency = first_chunk_time - start_time
                            logger.debug(f"Inference latency: {latency} seconds")
                        yield chunk.decode("utf-8")

    async def _process_context(self, context: OpenAILLMContext):
        await self.start_ttfb_metrics()

        # chunk_stream: AsyncStreamIterator[bytes] = (
        #     await self._stream_chat_completions(context)
        # )

        async for chunk in self._stream_chat_completions(context):
            if len(chunk) == 0:
                continue

            await self.stop_ttfb_metrics()
            await self.push_frame(TextFrame(chunk))

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        context = None
        if isinstance(frame, OpenAILLMContextFrame):
            context: OpenAILLMContext = frame.context
        elif isinstance(frame, LLMMessagesFrame):
            context = OpenAILLMContext.from_messages(frame.messages)
        elif isinstance(frame, VisionImageRawFrame):
            pass
        else:
            await self.push_frame(frame, direction)

        if context:
            await self.push_frame(LLMFullResponseStartFrame())
            await self.start_processing_metrics()
            await self._process_context(context)
            await self.stop_processing_metrics()
            await self.push_frame(LLMFullResponseEndFrame())

    def can_generate_metrics(self) -> bool:
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


async def run_bot(
    websocket_client: typing.Any,
    stream_sid: str,
    call_status_storage: dict,
    call_info: dict = {},
    speak_first: bool = False,
    *args,
) -> None:
    """
    Run the voice agent bot using a real-time WebSocket pipeline.

    Args:
        websocket_client (Any): WebSocket interface to stream audio and messages.
        stream_sid (str): Session identifier for Twilio stream.
        call_status_storage (dict): Shared dict for tracking call state.
        call_info (dict, optional): Call-specific settings and metadata.
        speak_first (bool, optional): If True, the bot speaks a predefined start message first.
        *args: Additional arguments passed to pipeline execution.

    Returns:
        None
    """
    start_time = time.time()
    call_status_storage[call_info.get("sid")] = "in-progress"
    start_message = call_info.get("agent_settings", {}).get("start_message")

    if start_message:
        messages = []
    else:
        messages = [
            {"role": "system", "content": ""},
        ]

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

    inference = InferenceCall(
        model="OpenAI/gpt-4.1-mini-2025-04-14",
        inference_url=INFERENCE_URL,
        prompt=call_info.get("prompt"),
        inputs=call_info.get("inputs") if call_info.get("inputs") else {},
        sid=call_info.get("sid"),
    )

    # TODO change to nova 3 when they will add multi-language support
    if call_info.get("language") != "en":
        live_options = LiveOptions(
            model="nova-2-general",
            language=call_info.get("language"),
        )
    else:
        live_options = None

    stt = DeepgramSTTService(
        api_key=os.getenv("DEEPGRAM_API_KEY"), live_options=live_options
    )

    tts = get_tts_service(call_info)

    context = OpenAILLMContext(messages)
    context_aggregator = inference.create_context_aggregator(context)

    # TODO REMOVE STATIC SECONDS
    # end_call = EndCallProcessor(start_time=start_time, sid=call_info.get('sid'), seconds=call_info.get('end_call_seconds'))
    end_call = EndCallProcessor(
        start_time=start_time, sid=call_info.get("sid"), seconds=300
    )

    pipeline = Pipeline(
        [
            transport.input(),  # Websocket input from client
            stt,  # Speech-To-Text
            context_aggregator.user(),
            inference,  # LLM
            end_call,
            tts,  # Text-To-Speech,
            transport.output(),  # Websocket output to client
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(audio_in_sample_rate=8000, allow_interruptions=True),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        if speak_first:
            if start_message:
                await task.queue_frames([TTSSpeakFrame(start_message)])
            else:
                await task.queue_frames([LLMMessagesFrame(messages)])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        await task.cancel()
        call_status_storage[call_info.get("sid")] = "completed"

    runner = PipelineRunner(handle_sigint=False, force_gc=True)

    await runner.run(task)

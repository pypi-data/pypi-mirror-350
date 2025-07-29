import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union

from fastapi import WebSocket, Request, Query
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.websockets import WebSocketDisconnect

from loguru import logger

from agent_zero.core.agent import Agent
from agent_zero.helpers.get_model import get_model
from agent_zero.core.pipecat_w_twillio.pipecat_twillio_http_inference import (
    run_bot,
)
from agent_zero.core.config import get_config
from agent_zero.core.pipecat_w_twillio.twilio_service import TwilioClient
from agent_zero.core.pipecat_w_twillio.templates import (
    twiml_template_outbound,
    twiml_template_inbound,
    twiml_template_outbound_with_play,
)
from agent_zero.data.consts import (
    SERVER_ADDRESS,
    OPENAI_API_KEY,
    INFERENCE_URL,
)
from agent_zero.data.validators import (
    is_valid_iso_language,
    is_valid_voice_settings,
    is_valid_end_call_time,
)
from agent_zero.data.cache import (
    set_call_status,
    get_call_status,
    delete_call_status,
    update_response_id,
)
from agent_zero.api.helpers.processors import (
    TransportInputProcessorInference,
    InitCacheProcessorInference,
    AgentInputsProcessor,
    SharedKnowledgeProcessor,
    frame_stream,
    TransportInputProcessorElevenlabs,
    InitCacheProcessorElevenlabs,
    run_pipeline,
    AgentPlainStreamingProcessor,
    AgentPlatformStreamingProcessor, TL_SharedKnowledgeProcessor, AgentPlatformStreamingProcessorElevenlabs,
)
from agent_zero.helpers import process_elevenlabs_transcript
from agent_zero.api.helpers.next_business_dates import next_business_dates
from agent_zero.api.helpers.get_available_time_slots import get_available_time_slots
from agent_zero.api.helpers.generate_grouped_calendar import generate_grouped_calendar
from agent_zero.core.tools.functions import transfer_call, get_weekday
from agent_zero.data.schemas import (
    ElevenlabsRequestBody,
    RequestBody,
    PlatformMetadata,
    RelevantResponseRequest,
    RequestBodyForVoiceAI,
    create_agent_inputs,
)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

twilio_client = TwilioClient()
data_storage: Dict[str, Dict[str, Any]] = {}



async def agent_inference(
    request_body: RequestBody
) -> StreamingResponse:
    """
    Process a standard inference request and return a streaming response.

    Args:
        request_body (RequestBody): The request payload.

    Returns:
        StreamingResponse: The processed response as a JSON event stream.
    """
    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id
    platform_metadata = request_body.platform_metadata
    conversation_history = request_body.history
    conversation_history.append({"role": "user", "content": request_body.query})
    active_flow = getattr(request_body, "active_flow", None)

    pipeline = [
        TransportInputProcessorInference(
            request_body,
            call_id,
            platform_metadata,
            conversation_history,
            active_flow,
        ),
        InitCacheProcessorInference(),
        AgentInputsProcessor(),
        SharedKnowledgeProcessor(),
        AgentPlatformStreamingProcessor(model, request_body.stream),
    ]

    return StreamingResponse(run_pipeline(pipeline), media_type="application/json")


async def plain_agent_inference(
    request_body: RequestBody
) -> StreamingResponse:
    """
    Process a standard inference request without streaming.

    Args:
        request_body (RequestBody): The request payload.

    Returns:
        StreamingResponse: The processed response.
    """

    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id
    platform_metadata = request_body.platform_metadata
    conversation_history = request_body.history
    active_flow = getattr(request_body, "active_flow", None)

    pipeline = [
        TransportInputProcessorInference(
            request_body,
            call_id,
            platform_metadata,
            conversation_history,
            active_flow,
        ),
        InitCacheProcessorInference(),
        AgentInputsProcessor(),
        SharedKnowledgeProcessor(),
        AgentPlainStreamingProcessor(model),
    ]

    return StreamingResponse(run_pipeline(pipeline), media_type="application/json")


async def agent_elevenlabs_inference(
    request_body: ElevenlabsRequestBody
) -> StreamingResponse:
    """
    Process an ElevenLabs-specific inference request and return a streaming response.

    Args:
        request_body (ElevenlabsRequestBody): The ElevenLabs-specific request payload.

    Returns:
        StreamingResponse: The processed response.
    """
    # Prepare agent_inputs_dict for RequestBody construction

    messages = request_body.messages
    if messages:
        messages.pop(0)  # Remove the assistant's first greeting
    messages = process_elevenlabs_transcript(messages)

    tools = request_body.tools
    platform_metadata = PlatformMetadata(platform="elevenlabs", tools=tools)

    request_body = RequestBody(
        conversation_id="123",
        stream=True,
        history=messages,
        platform_metadata=platform_metadata,
        agent_inputs=create_agent_inputs()
    )

    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id

    pipeline = [
        TransportInputProcessorElevenlabs(request_body, call_id, messages),
        InitCacheProcessorElevenlabs(),
        AgentInputsProcessor(),
        SharedKnowledgeProcessor(),
        AgentPlatformStreamingProcessorElevenlabs(model, True),
    ]

    return StreamingResponse(frame_stream(pipeline), media_type="application/json")


async def receive_voice_updates(
    request: RelevantResponseRequest
) -> None:
    """
    Update the response ID for a given conversation ID and turn-taking status.

    Args:
        request (RelevantResponseRequest): The incoming update request.

    Returns:
        None
    """
    update_response_id(
        call_id=request.conversation_id,
        response_id=request.platform_metadata.response_id,
        turn_taking=request.platform_metadata.turn_taking,
    )


async def process_call_transfer() -> Dict[str, Any]:
    """
    Handle a call transfer process.

    Args:

    Returns:
        Dict[str, Any]: The response from the transfer handler.
    """
    return transfer_call()


async def process_get_weekday(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
) -> Dict[str, str]:
    """
    Get the name of the weekday for the given date.

    Args:
        date (str): Date string in YYYY-MM-DD format.

    Returns:
        Dict[str, str]: A dictionary with the weekday name.
    """
    return {"message": get_weekday(date)}


async def status_callback_get(sid: str) -> Dict[str, Optional[str]]:
    """
    Get the call status for a given SID.

    Args:
        sid (str): The call SID.

    Returns:
        Dict[str, Optional[str]]: The call status.
    """
    return {"status": get_call_status(sid)}


async def status_callback_post(request: Request) -> None:
    """
    Handle a POST request to update call status.

    Args:
        request (Request): The incoming POST request.

    Returns:
        None
    """
    post_data = await request.form()
    print(post_data, flush=True)
    call_sid = post_data.get("CallSid")

    if post_data.get("CallStatus") == "busy":
        set_call_status(call_sid, "completed")

    if post_data.get("CallStatus") == "completed":
        delete_call_status(call_sid)
        data_storage.pop(call_sid, None)


async def initiate_phone_call(
    request_body: RequestBodyForVoiceAI
) -> Any:
    """
    Initiate a phone call via Twilio and store call data.

    Args:
        request_body (RequestBodyForVoiceAI): The request payload for voice AI.

    Returns:
        Union[JSONResponse, Dict[str, str]]: JSONResponse on error or call details on success.
    """
    language = request_body.language
    if not is_valid_iso_language(language):
        return JSONResponse(
            status_code=403,
            content={"message": f"Invalid language {language}"},
        )

    if not is_valid_voice_settings(
        request_body.agent_settings.voice_id, request_body.agent_settings.voice_url
    ):
        return JSONResponse(
            status_code=403,
            content={"message": "Invalid voice settings, no voice_id and voice_url"},
        )

    if not is_valid_end_call_time(request_body.end_call_seconds):
        return JSONResponse(
            status_code=403,
            content={"message": "Invalid end_call_seconds, the value must be >=60"},
        )

    try:
        sid = twilio_client.create_phone_call(
            request_body.from_number, request_body.to_number
        )
        set_call_status(sid, "initiated")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Internal Server Error: {e}"},
        )

    data_storage[sid] = request_body.model_dump()
    data_storage[sid]["sid"] = sid
    data_storage[sid]["call_type"] = "outbound"

    return {
        "sid": sid,
        "from": request_body.from_number,
        "to": request_body.to_number,
    }


async def outbound_webhook(request: Request) -> HTMLResponse:
    """
    Handle outbound webhook and return TwiML response.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: The TwiML XML response.
    """
    print("POST TwiML")

    data = await request.form()
    sid = data.get("CallSid")
    call_info = data_storage.get(sid, {})
    audio_url = call_info.get("play_audio_url")

    if audio_url:
        formatted_xml = twiml_template_outbound_with_play.format(
            audio_url=audio_url,
            wss_url=SERVER_ADDRESS,
        )
    else:
        formatted_xml = twiml_template_outbound.format(
            wss_url=SERVER_ADDRESS,
        )

    return HTMLResponse(content=formatted_xml, media_type="application/xml")


async def outbound_websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle outbound websocket endpoint for streaming voice data.

    Args:
        websocket (WebSocket): The websocket connection.

    Returns:
        None
    """
    call_sid = None
    try:
        await websocket.accept()
        start_data = websocket.iter_text()
        await start_data.__anext__()  # Skip first message
        call = json.loads(await start_data.__anext__())
        print(call, flush=True)
        call_sid = call["start"]["callSid"]
        stream_sid = call["start"]["streamSid"]

        call_info = data_storage.get(call_sid)
        print("WebSocket connection accepted")

        history = call_info.get("history", [])
        agent_inputs = create_agent_inputs()

        shared_knowledge = agent_inputs.model_dump()
        shared_knowledge["current_date"] = datetime.now().strftime(
            "%Y-%m-%d, %A. Time: %H:%M."
        )

        agent = Agent(
            model=get_model(
                get_config()["llm"]["main"]["vendor"],
                get_config()["llm"]["main"]["model"],
                openai_key=OPENAI_API_KEY,
            ),
            history=history,
            name=agent_inputs.project_name,
            call_id=call_sid,
            conversation_knowledge=shared_knowledge,
        )

        await agent.run_voice_stream(websocket, stream_sid, call_info)
        await websocket.close()

    except WebSocketDisconnect:
            print(f"LLM WebSocket disconnected for {call_sid}")
    except Exception as e:
        print(f"Error in LLM WebSocket: {e} for {call_sid}")
        await websocket.close(1011, "Server error")


async def test(request: Request) -> None:
    """
    Test endpoint that prints an error message.

    Args:
        request (Request): The incoming request.

    Returns:
        None
    """
    print("ERROR")


async def inbound_webhook(
    request: Request
) -> HTMLResponse:
    """
    Handle inbound webhook and return TwiML response.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: The TwiML XML response.
    """
    content_type = request.headers.get("content-type", "")

    if content_type.startswith("application/json"):
        data: Dict[str, Any] = await request.json()
    else:
        # Twilio default: application/x-www-form-urlencoded
        raw = await request.form()
        data = dict(raw)

    call_to = data.get("To")
    call_from = data.get("From")
    print("POST TwiML")
    sid = data.get("CallSid")

    data_storage[sid] = {
        "to": call_to,
        "from": call_from,
        "sid": sid,
        "inputs": data.get("inputs", {}),
        "agent_settings": data.get("agent_settings", {}),
        "call_type": "inbound",
        "inference_url": INFERENCE_URL,
        "language": "en",
        "end_call_seconds": (
            data.get("end_call_seconds") if data.get("end_call_seconds") else True
        ),
        "prompt": "",
    }

    formatted_xml = twiml_template_inbound.format(
        status_callback=SERVER_ADDRESS,
        transcription_url=SERVER_ADDRESS,
        wss_url=SERVER_ADDRESS,
    )

    return HTMLResponse(content=formatted_xml, media_type="application/xml")


async def inbound_websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle inbound websocket endpoint for streaming voice data and run agent.

    Args:
        websocket (WebSocket): The websocket connection.

    Returns:
        None
    """
    call_sid = None
    try:
        await websocket.accept()
        start_data = websocket.iter_text()
        await start_data.__anext__()  # Skip first message
        call = json.loads(await start_data.__anext__())
        print(call, flush=True)
        call_sid = call["start"]["callSid"]
        stream_sid = call["start"]["streamSid"]
        call_info = data_storage.get(call_sid, {})
        print("WebSocket connection accepted")

        history = call_info.get("history", [])
        agent_inputs = create_agent_inputs()

        shared_knowledge = agent_inputs.model_dump()
        shared_knowledge["current_date"] = datetime.now().strftime(
            "%Y-%m-%d, %A. Time: %H:%M."
        )

        agent = Agent(
            model=get_model(
                get_config()["llm"]["main"]["vendor"],
                get_config()["llm"]["main"]["model"],
                openai_key=OPENAI_API_KEY,
            ),
            history=history,
            name=agent_inputs.project_name,
            call_id=call_sid,
            conversation_knowledge=shared_knowledge,
        )

        await agent.run_voice_stream(websocket, stream_sid, call_info)
        await websocket.close()

    except WebSocketDisconnect:
        print(f"LLM WebSocket disconnected for {call_sid}")
    except Exception as e:
        print(f"Error in LLM WebSocket: {e} for {call_sid}")
        await websocket.close(1011, "Server error")


async def tl_inbound_websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle inbound websocket endpoint for streaming voice data and run agent.

    Args:
        websocket (WebSocket): The websocket connection.

    Returns:
        None
    """
    call_sid = None
    try:
        await websocket.accept()
        start_data = websocket.iter_text()
        await start_data.__anext__()  # Skip first message
        call = json.loads(await start_data.__anext__())
        print(call, flush=True)
        call_sid = call["start"]["callSid"]
        stream_sid = call["start"]["streamSid"]
        call_info = data_storage.get(call_sid, {})
        print("WebSocket connection accepted")

        from agent_zero.core.agent import Agent

        history = call_info.get("history", [])
        agent_inputs = create_agent_inputs()

        shared_knowledge = agent_inputs.model_dump()
        shared_knowledge["current_date"] = datetime.now().strftime(
            "%Y-%m-%d, %A. Time: %H:%M."
        )
        # ---- Talent Lobby extras ----
        next_5_business_days = next_business_dates()
        slots = await get_available_time_slots(next_5_business_days)
        shared_knowledge["slots_data"] = json.dumps(slots, indent=4)
        shared_knowledge["calendar"] = generate_grouped_calendar(datetime.now())
        # -----------------------------

        agent = Agent(
            model=get_model(
                get_config()["llm"]["main"]["vendor"],
                get_config()["llm"]["main"]["model"],
                openai_key=OPENAI_API_KEY,
            ),
            history=history,
            name=agent_inputs.project_name,
            call_id=call_sid,
            conversation_knowledge=shared_knowledge,
        )

        await agent.run_voice_stream(websocket, stream_sid, call_info)
        try:
            await websocket.close()
        except RuntimeError:
            logger.debug(f"WebSocket already closed for {call_sid}")

    except WebSocketDisconnect:
        print(f"LLM WebSocket disconnected for {call_sid}")
    except Exception as e:
        print(f"Error in LLM WebSocket: {e} for {call_sid}")
        try:
            await websocket.close(1011, "Server error")
        except RuntimeError:
            logger.debug(f"WebSocket already closed when sending error close for {call_sid}")


async def inbound_websocket_endpoint_inference_url(
    websocket: WebSocket = "talent_lobby"
) -> None:
    """
    Handle inbound websocket endpoint with inference URL and run bot.

    Args:
        websocket (WebSocket): The websocket connection.

    Returns:
        None
    """
    call_sid = None
    try:
        await websocket.accept()
        start_data = websocket.iter_text()
        await start_data.__anext__()  # Skip first message
        call = json.loads(await start_data.__anext__())
        print(call, flush=True)
        call_sid = call["start"]["callSid"]
        stream_sid = call["start"]["streamSid"]

        call_info = data_storage.get(call_sid)
        print("WebSocket connection accepted")

        await run_bot(websocket, stream_sid, data_storage, call_info)

    except WebSocketDisconnect:
        print(f"LLM WebSocket disconnected for {call_sid}")
    except Exception as e:
        print(f"Error in LLM WebSocket: {e} for {call_sid}")
        await websocket.close(1011, "Server error")


# TALENT LOBBY
async def tl_plain_agent_inference(
    request_body: RequestBody
) -> StreamingResponse:
    """
    Process a standard inference request without streaming.

    Args:
        request_body (RequestBody): The request payload.

    Returns:
        StreamingResponse: The processed response.
    """
    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id
    platform_metadata = request_body.platform_metadata
    conversation_history = request_body.history
    active_flow = getattr(request_body, "active_flow", None)

    pipeline = [
        TransportInputProcessorInference(
            request_body,
            call_id,
            platform_metadata,
            conversation_history,
            active_flow,
        ),
        InitCacheProcessorInference(),
        AgentInputsProcessor(),
        TL_SharedKnowledgeProcessor(),
        AgentPlainStreamingProcessor(model),
    ]

    return StreamingResponse(run_pipeline(pipeline), media_type="application/json")

async def tl_agent_inference(
    request_body: RequestBody
) -> StreamingResponse:
    """
    Process a standard inference request and return a streaming response.

    Args:
        request_body (RequestBody): The request payload.

    Returns:
        StreamingResponse: The processed response as a JSON event stream.
    """
    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id
    platform_metadata = request_body.platform_metadata
    platform_metadata = request_body.platform_metadata
    conversation_history = request_body.history
    conversation_history.append({"role": "user", "content": request_body.query})
    active_flow = getattr(request_body, "active_flow", None)

    pipeline = [
        TransportInputProcessorInference(
            request_body,
            call_id,
            platform_metadata,
            conversation_history,
            active_flow,
        ),
        InitCacheProcessorInference(),
        AgentInputsProcessor(),
        TL_SharedKnowledgeProcessor(),
        AgentPlatformStreamingProcessor(model, request_body.stream),
    ]

    return StreamingResponse(run_pipeline(pipeline), media_type="application/json")

async def tl_agent_elevenlabs_inference(
    request_body: ElevenlabsRequestBody
) -> StreamingResponse:
    """
    Process an ElevenLabs-specific inference request and return a streaming response.

    Args:
        request_body (ElevenlabsRequestBody): The ElevenLabs-specific request payload.

    Returns:
        StreamingResponse: The processed response.
    """
    # Prepare agent_inputs_dict for RequestBody construction

    messages = request_body.messages
    if messages:
        messages.pop(0)  # Remove the assistant's first greeting
    messages = process_elevenlabs_transcript(messages)

    tools = request_body.tools
    platform_metadata = PlatformMetadata(platform="elevenlabs", tools=tools)

    request_body = RequestBody(
        conversation_id="123",
        stream=True,
        history=messages,
        platform_metadata=platform_metadata,
        agent_inputs=create_agent_inputs()
    )

    model = get_model(
        get_config()["llm"]["main"]["vendor"],
        get_config()["llm"]["main"]["model"],
        openai_key=OPENAI_API_KEY,
    )

    call_id = request_body.conversation_id

    pipeline = [
        TransportInputProcessorElevenlabs(request_body, call_id, messages),
        InitCacheProcessorElevenlabs(),
        AgentInputsProcessor(),
        TL_SharedKnowledgeProcessor(),
        AgentPlatformStreamingProcessorElevenlabs(model, True),
    ]

    return StreamingResponse(frame_stream(pipeline), media_type="application/json")
"""
This module provides a simple in-memory TTL cache for managing conversation state,
metadata, agent inputs, and call status for voice agent sessions. It includes
helper functions to initialize, update, and retrieve cached data associated with
individual call sessions.
"""

from typing import Any, Dict, List, Optional
from cachetools import TTLCache

from agent_zero.data.consts import StateEnum
from agent_zero.data.schemas import (
    ConversationFlow,
    Metadata,
    create_agent_inputs,
)

cache = TTLCache(maxsize=10000, ttl=3600)


def update_response_id(
    call_id: str, response_id: Optional[str], turn_taking: Optional[Any]
) -> None:
    """
    Update the response ID and turn-taking information for a given call in the platform_metadata section.

    Args:
        call_id: The unique identifier for the call session.
        response_id: The response ID to associate with this call.
        turn_taking: Turn-taking information to store for this call.
    """
    # Ensure the "platform_metadata" section exists in cache
    if "platform_metadata" not in cache or call_id not in cache["platform_metadata"]:
        cache["platform_metadata"] = {}
        cache["platform_metadata"][call_id] = {}
    # Store response_id and turn_taking if provided
    if response_id:
        cache["platform_metadata"][call_id]["relevant_response_id"] = response_id
    if turn_taking:
        cache["platform_metadata"][call_id]["turn_taking"] = turn_taking


def update_cache_retell_platform(
    call_id: str,
    conversation_history: Optional[List[Any]],
    agent_inputs: Optional[Any],
) -> None:
    """
    Update the cache for a given call with new conversation history and agent inputs.
    Initializes cache for the call if not already present.

    Args:
        call_id: The unique identifier for the call session.
        conversation_history: The conversation history to store.
        agent_inputs: Agent inputs to associate with the call.
    """
    # Initialize cache for new call_id
    if call_id not in cache:
        cache[call_id] = {}
        cache[call_id]["agent_inputs"] = create_agent_inputs()
        active_flow = ConversationFlow(active_agent=StateEnum.MAIN_AGENT_FLOW)
        metadata = Metadata(
            active_flow=active_flow,
            history=[],
        )
        cache[call_id]["metadata"] = metadata
    # Update agent_inputs if provided
    if agent_inputs:
        cache[call_id]["agent_inputs"] = agent_inputs
    # Update conversation history if provided
    if conversation_history:
        if "metadata" not in cache[call_id]:
            active_flow = ConversationFlow(active_agent=StateEnum.MAIN_AGENT_FLOW)
            metadata = Metadata(
                active_flow=active_flow,
                history=conversation_history if conversation_history else [],
            )
            cache[call_id]["metadata"] = metadata
        else:
            cache[call_id]["metadata"].history = conversation_history


def init_cache(
    call_id: str,
    metadata: Optional[Metadata],
    agent_inputs: Optional[Any],
    query: Optional[str],
    conversation_history: Optional[List[Any]],
    active_flow: Optional[ConversationFlow],
) -> None:
    """
    Initialize or update the cache entry for a call session, including metadata, agent inputs,
    conversation history, and active flow.

    Args:
        call_id: The unique identifier for the call session.
        metadata: Metadata object to store for the call.
        agent_inputs: Agent inputs to associate with the call.
        query: Latest user query to append to conversation history.
        conversation_history: Conversation history to initialize.
        active_flow: Active conversation flow for the session.
    """
    # Ensure cache entry exists for call_id
    if call_id not in cache:
        cache[call_id] = {}
    # Ensure flows_trace list exists for tracking flow changes
    if "flows_trace" not in cache[call_id]:
        cache[call_id]["flows_trace"] = []
    # Set agent_inputs, creating default if missing
    if agent_inputs:
        cache[call_id]["agent_inputs"] = agent_inputs
    else:
        if not cache[call_id].get("agent_inputs", None):
            cache[call_id]["agent_inputs"] = create_agent_inputs()
    # Set metadata, creating default if missing
    if metadata:
        cache[call_id]["metadata"] = metadata
    else:
        if not cache[call_id].get("metadata", None):
            _active_flow = (
                active_flow
                if active_flow
                else ConversationFlow(active_agent=StateEnum.MAIN_AGENT_FLOW)
            )
            _history = conversation_history if conversation_history else []
            metadata = Metadata(
                active_flow=_active_flow,
                history=_history,
            )
            cache[call_id]["metadata"] = metadata
    # Append the query to conversation history if provided
    if query:
        cache[call_id]["metadata"].history.append({"role": "user", "content": query})


# -------------------------------------------------
# Call-status helpers
# -------------------------------------------------
def set_call_status(call_id: str, status: str) -> None:
    """
    Store or update the status of a phone call.

    Args:
        call_id: The unique identifier for the call session.
        status: The status string to store.
    """
    if call_id not in cache:
        cache[call_id] = {}
    cache[call_id]["status"] = status


def get_call_status(call_id: str) -> Optional[str]:
    """
    Return the current status of a call, or ``None`` if not available.

    Args:
        call_id: The unique identifier for the call session.

    Returns:
        The status string if present, else None.
    """
    return cache.get(call_id, {}).get("status")


def delete_call_status(call_id: str) -> None:
    """
    Remove only the status info for ``call_id`` (leave other data intact).

    Args:
        call_id: The unique identifier for the call session.
    """
    if call_id in cache and "status" in cache[call_id]:
        del cache[call_id]["status"]

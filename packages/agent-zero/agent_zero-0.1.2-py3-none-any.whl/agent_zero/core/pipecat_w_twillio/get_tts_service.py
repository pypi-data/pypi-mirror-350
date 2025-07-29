import os

from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
from pipecat.services.playht.tts import PlayHTTTSService
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.lmnt.tts import LmntTTSService


def get_tts_service(call_info: dict) -> object:
    """
    Return the appropriate TTS service instance based on the voice provider specified in call_info.

    Args:
        call_info (dict): Dictionary containing agent settings, including voice provider and voice ID or URL.

    Returns:
        object: An instance of a TTS service class.
    """
    voice_provider = call_info.get("agent_settings", {}).get(
        "voice_provider", "elevenlabs"
    )

    if voice_provider not in ["elevenlabs", "playht", "cartesia", "lmnt"]:
        raise ValueError(
            f"Invalid voice_provider: {voice_provider}. It must be either 'elevenlabs', 'playht', 'lmnt', or 'cartesia'."
        )

    agent_settings = call_info.get("agent_settings", {})

    if voice_provider == "elevenlabs":
        return ElevenLabsTTSService(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id=agent_settings.get("voice_id", os.getenv("ELEVENLABS_VOICE_ID")),
        )
    elif voice_provider == "playht":
        return PlayHTTTSService(
            user_id=os.getenv("PLAYHT_USER_ID"),
            api_key=os.getenv("PLAYHT_API_KEY"),
            voice_url=agent_settings.get("voice_url"),
        )
    elif voice_provider == "cartesia":
        return CartesiaTTSService(
            api_key=os.getenv("CARTESIA_API_KEY"),
            voice_id=agent_settings.get("voice_id"),
        )
    elif voice_provider == "lmnt":
        return LmntTTSService(
            api_key=os.getenv("LMNT_API_KEY"),
            voice_id=agent_settings.get("voice_id"),
            sample_rate=16000,
        )

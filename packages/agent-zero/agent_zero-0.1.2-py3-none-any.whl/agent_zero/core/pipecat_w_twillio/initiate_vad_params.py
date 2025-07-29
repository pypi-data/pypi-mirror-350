from pipecat.audio.vad.vad_analyzer import VADParams

from agent_zero.core.config import get_config


def initiate_vad_params() -> VADParams:
    """
    Initialize VAD (Voice Activity Detection) parameters from the config.

    Returns:
        VADParams: An instance of VADParams with values from the configuration.

    Raises:
        ValueError: If required VAD parameters are missing in the configuration.
    """
    vad_params = get_config().get("vad_params")
    required_keys = {"confidence", "min_volume", "start_secs", "stop_secs"}

    # Check if any required key is missing in the vad_params
    if any(key not in vad_params for key in required_keys):
        raise ValueError("invalid vad_params config")

    # Initialize and return VADParams with the given configuration
    return VADParams(**vad_params)

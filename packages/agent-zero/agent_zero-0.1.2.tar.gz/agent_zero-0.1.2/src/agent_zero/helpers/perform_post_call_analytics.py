import json
from datetime import datetime

from agent_zero.core.llm.models.FireworksModel import FireworksModel
from agent_zero.core.prompts import get_prompt
from agent_zero.data.consts import FIREWORKS_API_KEY, PromptType
from agent_zero.data.schemas import PostCallAnalysisSchema

async def perform_post_call_analysis(
    messages: list[dict], llm: FireworksModel | None = None, language="en"
) -> dict:
    """
    Perform post-call analysis using the LLM.

    Args:
        messages (list[dict]): The list of conversation messages.
        llm (FireworksModel | None): Optional LLM instance to use.

    Returns:
        dict: The structured analysis result, including callback time, call status, and summary.
    """
    if not llm:
        llm = FireworksModel(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            fireworks_api_key=FIREWORKS_API_KEY,
        )

    prompt_str = get_prompt(PromptType.POST_ANALYSIS, language)
    prompt = prompt_str.format(
        messages=json.dumps(messages, indent=4),
        current_datetime=datetime.now().strftime("%Y-%m-%d, %A. Time: %H:%M."),
    )
    formatted_messages = [{"role": "system", "content": prompt}]

    response = await llm.async_call_llm(
        messages=formatted_messages,
        temperature=1,
        response_type="json_object",
        response_schema=PostCallAnalysisSchema,
    )

    if response := response.get("content"):
        response = json.loads(response)

    if isinstance(response.get("callback_time"), str):
        # Convert callback_time string to a datetime object for further processing
        response["callback_time"] = datetime.fromisoformat(response["callback_time"])

    return response
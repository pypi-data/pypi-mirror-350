import json
import uuid
from datetime import time


def create_openai_finish_chunk():
    chunk = {
        "id": str(uuid.uuid4()),
        "choices": [
            {
                "delta": {
                    "content": None,
                    "role": None,
                    "function_call": None,
                    "tool_calls": None
                },
                "finish_reason": 'stop',
            }
        ],
        "created": int(time.time()),
        "object": "chat.completion.chunk",
    }

    return f"data: {json.dumps(chunk)}\n\n"
import json
import uuid
from datetime import time


def create_openai_chunk(content):
    chunk = {
        "id": str(uuid.uuid4()),
        "choices": [
            {
                "delta": {
                    "content": content,
                    "role": 'assistant',
                    "function_call": None,
                    "tool_calls": None
                },
                "finish_reason": None,
            }
        ],
        "created": int(time.time()),
        "object": "chat.completion.chunk",
    }

    return f"data: {json.dumps(chunk)}\n\n"
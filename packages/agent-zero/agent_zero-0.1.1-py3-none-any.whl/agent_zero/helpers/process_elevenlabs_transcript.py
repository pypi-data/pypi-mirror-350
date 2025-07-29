def process_elevenlabs_transcript(messages):
    merged_messages = []
    i = 0

    while i < len(messages):
        msg = messages[i]

        # Check if it's an assistant message with content but no tool calls
        if (
            msg["role"] == "assistant" and
            "content" in msg and msg["content"] and
            "tool_calls" not in msg and
            i + 1 < len(messages) and
            messages[i + 1]["role"] == "assistant" and
            "tool_calls" in messages[i + 1] and not messages[i + 1].get("content")
        ):
            msg["tool_calls"] = messages[i + 1]["tool_calls"]

            # Skip the next message as it's now merged
            i += 1

        merged_messages.append(msg)

        i += 1

    return merged_messages
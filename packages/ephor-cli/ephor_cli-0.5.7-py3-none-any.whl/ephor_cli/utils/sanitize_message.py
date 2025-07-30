from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage, ToolMessage


def sanitize_message(messages: list[BaseMessage]) -> list[BaseMessage]:
    tool_calls_to_remove = {}

    for message in messages:
        if isinstance(message, AIMessage):
            if message.tool_calls and len(message.tool_calls) > 0:
                for tool_call in message.tool_calls:
                    tool_calls_to_remove[tool_call.get("id")] = True
        elif isinstance(message, ToolMessage):
            if message.tool_call_id in tool_calls_to_remove:
                tool_calls_to_remove[message.tool_call_id] = False

    sanitized_messages = []
    for message in messages:
        to_add = True
        if isinstance(message, AIMessage):
            if message.tool_calls and len(message.tool_calls) > 0:
                for tool_call in message.tool_calls:
                    if tool_calls_to_remove[tool_call.get("id")]:
                        to_add = False
        if to_add:
            sanitized_messages.append(message)
    return sanitized_messages

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from google_a2a.common.types import Message, Part


def a2a_message_to_langchain_message(message: Message) -> BaseMessage:
    if message.role == "user":
        return a2a_user_message_to_langchain_message(message)
    else:
        raise ValueError(f"Unknown message role: {message.role}")


def a2a_user_message_to_langchain_message(message: Message) -> HumanMessage:
    return HumanMessage(
        content=[{"type": "text", "text": part.text} for part in message.parts]
    )


def langchain_message_to_a2a_message(message: BaseMessage) -> Message:
    if isinstance(message, AIMessage):
        return langchain_ai_message_to_a2a_message(message)
    else:
        raise ValueError(f"Unknown message type: {type(message)}")


def langchain_ai_message_to_a2a_message(message: AIMessage) -> Message:
    return Message(role="agent", parts=[{"type": "text", "text": message.content}])


def langchain_content_to_a2a_content(content: str | list[str | dict]) -> list[Part]:
    parts = []
    if isinstance(content, list):
        for item in content:
            parts.extend(langchain_content_to_a2a_content(item))
    elif isinstance(content, dict) and content["type"] == "text":
        parts.append(content)
    elif isinstance(content, str):
        parts.append({"type": "text", "text": content})
    return parts

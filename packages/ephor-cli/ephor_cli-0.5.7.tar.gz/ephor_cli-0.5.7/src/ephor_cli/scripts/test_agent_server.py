import asyncio
import json
from google_a2a.common.types import (
    TaskSendParams,
    Message,
    TextPart,
    TaskStatusUpdateEvent,
    TaskState,
)
from google_a2a.common.client import A2ACardResolver, A2AClient
from langchain_core.messages.utils import messages_from_dict, merge_message_runs
from langchain_core.messages.base import messages_to_dict


async def main():
    card_resolver = A2ACardResolver("http://localhost:10002/giphy-agent")
    card = card_resolver.get_agent_card()
    client = A2AClient(card)
    task_id = "9f34cb2a-8c1c-4f30-b3bc-61b5906b55cc"
    tool_call_id = "1234567890"
    conversation_id = "b92bc664-10ac-4cd7-a5da-c14d179f476b"
    project_id = "default"
    user_id = "ashish"
    message_text = "List 1 cat gif"
    metadata = {
        "task_id": task_id,
        "tool_call_id": tool_call_id,
        "conversation_id": conversation_id,
        "project_id": project_id,
        "user_id": user_id,
        "agent_name": card.name,
    }
    request = TaskSendParams(
        id=task_id,
        sessionId=conversation_id,
        message=Message(
            role="user",
            parts=[TextPart(text=message_text)],
            metadata=metadata,
        ),
        acceptedOutputModes=["text", "text/plain", "image/png"],
        metadata=metadata,
    )

    print("Sending task to remote agent...")
    chunks = []
    async for response in client.send_task_streaming(request):
        print(f"[STREAM] Response: {response}")

        event = response.result
        if isinstance(event, TaskStatusUpdateEvent):
            if event.status.state in [
                TaskState.COMPLETED,
                TaskState.FAILED,
                TaskState.CANCELED,
            ]:
                print(f"Task status update: {event}")
                break
            else:
                message = event.status.message
                content = message.parts[0].text
                content = json.loads(content)
                chunk = messages_from_dict([content])[0]
                chunks.append(chunk)
                merge_message_runs(chunks)

    merged_messages = merge_message_runs(chunks)
    with open("merged_messages.json", "w") as f:
        json.dump(messages_to_dict(merged_messages), f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())

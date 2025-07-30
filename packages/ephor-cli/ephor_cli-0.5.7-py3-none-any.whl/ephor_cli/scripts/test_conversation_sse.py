import asyncio
import httpx
from httpx_sse import connect_sse

API_URL = "http://localhost:12000"
USER_ID = "ashish"
PROJECT_ID = "default"
AGENT_URL = "http://localhost:10002/giphy-agent"


async def create_conversation():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{API_URL}/conversation/create",
            json={"params": {"user_id": USER_ID, "project_id": PROJECT_ID}},
        )
        resp.raise_for_status()
        return resp.json()["result"]["conversation_id"]


async def register_agent(conversation_id):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{API_URL}/agent/register",
            json={
                "params": {
                    "user_id": USER_ID,
                    "project_id": PROJECT_ID,
                    "conversation_id": conversation_id,
                    "url": AGENT_URL,
                }
            },
        )
        resp.raise_for_status()
        return resp.json()["result"]


async def send_message(conversation_id, message):
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.post(
            f"{API_URL}/message/send",
            json={
                "params": {
                    "user_id": USER_ID,
                    "project_id": PROJECT_ID,
                    "conversation_id": conversation_id,
                    "message": {"type": "human", "content": message},
                }
            },
        )
        resp.raise_for_status()
        return resp.json()["result"]["message_id"]


def stream_sse(conversation_id, message_id):
    url = f"{API_URL}/sse"
    payload = {
        "params": {
            "user_id": USER_ID,
            "project_id": PROJECT_ID,
            "conversation_id": conversation_id,
            "message_id": message_id,
        }
    }
    with httpx.Client(timeout=None) as client:
        with connect_sse(client, "POST", url, json=payload) as event_source:
            for sse in event_source.iter_sse():
                data = sse.data
                if data == "[[DONE]]":
                    print("[DONE]")
                    break
                print("Event data =>", data)
                print("=" * 100)


async def main():
    conversation_id = await create_conversation()
    print(f"Created conversation: {conversation_id}")
    agent = await register_agent(conversation_id)
    print(f"Registered agent: {agent}")
    message = input("Enter your message: ")
    message_id = await send_message(conversation_id, message)
    print("Sent message. Streaming response:")
    await asyncio.to_thread(stream_sse, conversation_id, message_id)


if __name__ == "__main__":
    asyncio.run(main())

import requests

BASE_URL = "http://localhost:12000"  # Change if your server runs elsewhere

USER_ID = "ashish"
PROJECT_ID = "default"


def list_conversations():
    url = f"{BASE_URL}/conversation/list"
    payload = {"params": {"user_id": USER_ID, "project_id": PROJECT_ID}}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()["result"]


def delete_conversation(conversation_id):
    url = f"{BASE_URL}/conversation/delete"
    payload = {
        "params": {
            "user_id": USER_ID,
            "project_id": PROJECT_ID,
            "conversation_id": conversation_id,
        }
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


def main():
    conversations = list_conversations()
    print(f"Found {len(conversations)} conversations.")
    for conv in conversations:
        conv_id = conv["conversation_id"]
        print(f"Deleting conversation {conv_id}...")
        result = delete_conversation(conv_id)
        print(f"Delete result: {result}")


if __name__ == "__main__":
    main()

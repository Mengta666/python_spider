import requests

BOT_TOKEN = "token"

def get_chat_id():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()
        if data["ok"] and data["result"]:
            for update in data["result"]:
                chat = update.get("message", {}).get("chat", {})
                chat_id = chat.get("id")
                chat_type = chat.get("type")
                chat_title = chat.get("title", chat.get("username", "Unknown"))
                print(f"Chat ID: {chat_id}, Type: {chat_type}, Name: {chat_title}")
        else:
            print("No updates found. Send a message to the bot first.")
    except Exception as e:
        print(f"Error: {e}")

get_chat_id()
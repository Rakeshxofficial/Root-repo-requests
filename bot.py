from pyrogram import Client, errors
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "my_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

async def approve_requests():
    try:
        async with app:
            async for request in app.get_chat_join_requests(int(os.getenv("CHANNEL_ID"))):
                try:
                    user_id = request.user.id
                    await app.approve_chat_join_request(int(os.getenv("CHANNEL_ID")), user_id)
                    print(f"Approved: {user_id}")
                    await asyncio.sleep(5)  # Non-blocking delay
                except errors.FloodWait as e:
                    print(f"FloodWait: Pausing for {e.value} seconds")
                    await asyncio.sleep(e.value + 10)  # Extra buffer
    except errors.FloodWait as e:
        print(f"FATAL FloodWait: Wait {e.value} seconds and redeploy")
    except Exception as e:
        print(f"Critical Error: {e}")

# Graceful startup with error handling
async def main():
    try:
        await approve_requests()
    except Exception as e:
        print(f"Shutdown due to: {e}")

if __name__ == "__main__":
    asyncio.run(main())

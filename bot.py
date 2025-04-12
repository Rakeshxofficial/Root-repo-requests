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

async def safe_start():
    try:
        await app.start()
        return True
    except errors.FloodWait as e:
        print(f"FATAL: Telegram requires {e.value} seconds wait")
        print(f"Stop deployment and wait {e.value // 60} minutes")
        return False
    except Exception as e:
        print(f"Authorization failed: {e}")
        return False

async def approve_requests():
    try:
        async for request in app.get_chat_join_requests(int(os.getenv("CHANNEL_ID"))):
            user_id = request.user.id
            await app.approve_chat_join_request(int(os.getenv("CHANNEL_ID")), user_id)
            print(f"Approved: {user_id}")
            await asyncio.sleep(10)  # Conservative delay

async def main():
    if not await safe_start():
        return  # Exit on authorization failure
    
    try:
        await approve_requests()
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())

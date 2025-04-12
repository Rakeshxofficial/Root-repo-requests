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

async def approve_join_requests():
    try:
        # Get pending join requests using BOT-ONLY method
        async for request in app.get_chat_join_requests(
            chat_id=int(os.getenv("CHANNEL_ID")),
            limit=100
        ):
            try:
                await app.approve_chat_join_request(
                    chat_id=int(os.getenv("CHANNEL_ID")),
                    user_id=request.user.id
                )
                print(f"Approved: {request.user.id}")
                await asyncio.sleep(5)  # Rate limiting
            except errors.FloodWait as e:
                print(f"Flood wait: Sleeping {e.value}s")
                await asyncio.sleep(e.value)
    except errors.RPCError as e:
        print(f"Telegram error: {e}")
    except Exception as e:
        print(f"General error: {e}")

async def main():
    async with app:  # Proper context manager for lifecycle
        await approve_join_requests()

if __name__ == "__main__":
    asyncio.run(main())

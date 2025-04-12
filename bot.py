from pyrogram import Client, errors
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Initialize Pyrogram client as Bot
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def approve_requests():
    async with app:
        try:
            async for request in app.get_chat_join_requests(CHANNEL_ID):
                try:
                    user_id = request.user.id
                    await app.approve_chat_join_request(CHANNEL_ID, user_id)
                    print(f"Approved: {user_id}")
                except errors.RPCError as e:
                    print(f"Error approving {user_id}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
        except errors.RPCError as e:
            print(f"Error fetching requests: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

app.run(approve_requests())

import os
from dotenv import load_dotenv

load_dotenv()

gemini_ai_api = os.environ.get("GEMINI_AI_API")
discord_sdk = os.environ.get("DISCORD_SDK")
discord_username = os.environ.get("DISCORD_USERNAME")
discord_owner_id = os.environ.get("DISCORD_OWNER_ID")

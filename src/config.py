import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

path = str(Path(__file__).parent.parent)
PATH_TO_LOGS = path + "/logs/"
PATH_TO_CHATS = path + "/chats/"

bot_config = {
    "owner_id": int(os.getenv("OWNER_ID")), # type: ignore
}

modules_config = {
    "geo": {
        "enabled": True,
        "location": "Moscow",
        "zone": "EET",
        "language": "en",
        "meteoKey": os.getenv("METEO_API"),
    },
    "chat": {
        "enabled": True,
        "open_router_key": os.getenv("OPEN_ROUTER_KEY"),
        "ai_horde_key": os.getenv("AI_HORDE_KEY"),
        "openai_key": os.getenv("OPENAI_KEY"),
        "huggingface_token": os.getenv("HUGGINGFACE_TOKEN"),
        "oobabooga_host": os.getenv("OOBABOOGA_HOST"),
    },
    "translate": {
        "enabled": True,
    },
}
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

path = str(Path(__file__).parent.parent)
PATH_TO_LOGS = path + "/logs/"
del path

bot_config = {
    "owner_id": os.getenv("OWNER_ID"),
}

modules_config = {
    "geo": True,
}
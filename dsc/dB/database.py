# we save the vars here // remove this line later
import os

ENV = bool(os.environ.get("ENV", False))


class Var(object):
    API_ID = int(os.environ.get("API_ID", 9))
    API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    SESSION = os.environ.get("SESSION", None)
    DB_URI = os.environ.get("DATABASE_URL", None)

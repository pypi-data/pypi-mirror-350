import multiprocessing
import pathlib

from environs import Env

env = Env()
env.read_env()
APP_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
USER_MEDIA_ROOT_PATH = env.str("USER_MEDIA_ROOT", ".media")
MEDIA_ROOT = APP_ROOT / "media"
KEY = env.str("KEY", "default")
BOT_TOKEN = env.str("BOT_TOKEN", "")
TELEGRAPH_TOKEN = env.str("TELEGRAPH_TOKEN", "")
SHORT_NAME = env.str("SHORT_NAME", "")
AUTHOR_NAME = env.str("AUTHOR_NAME", "")
AUTHOR_URL = env.str("AUTHOR_URL", "")
DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()
MAX_IMAGES_PER_POST = env.int("MAX_IMAGES_PER_POST", 99)
CHANNELS = ["@mycosplayposts0000", "@cosplayerscollection0000"]


def get_media_root() -> pathlib.Path:
    USER_MEDIA_ROOT_PATH = env.str("USER_MEDIA_ROOT", None)

    if USER_MEDIA_ROOT_PATH is not None:
        media_root = pathlib.Path(USER_MEDIA_ROOT_PATH)
    else:
        media_root = MEDIA_ROOT

    return media_root

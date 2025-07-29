from datetime import datetime
from pathlib import Path

from radiens.utils.constants import TIME_SPEC


def time_now():
    return datetime.now().strftime(TIME_SPEC)

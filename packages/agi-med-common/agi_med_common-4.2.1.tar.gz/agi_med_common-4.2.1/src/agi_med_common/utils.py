import codecs
import json
import os
from datetime import datetime
from pathlib import Path


def make_session_id() -> str:
    return f"{datetime.now():%y%m%d%H%M%S}"


def read_json(path: Path | os.PathLike[str] | str) -> list | dict:
    with codecs.open(path, "r", encoding="utf8") as file:
        return json.load(file)

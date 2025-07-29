import sys
import logging
import atexit
from types import FrameType
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger('auto_logger')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

_prev_locals: Dict[int, Dict[str, Any]] = {}

ts = datetime.now().strftime('%H:%M:%S')
logger.info(f"[{ts}] うぉぉぉおおおおおおおおおおおおおおおお")

def _on_exit():
    ts = datetime.now().strftime('%H:%M:%S')
    logger.info(f"[{ts}] うぉぉぉおおおおおおおおおおおおおおおお")
atexit.register(_on_exit)


def banagher_links(frame: FrameType, event: str, arg: Optional[Any]) -> Any:
    ts = datetime.now().strftime('%H:%M:%S')
    fid = id(frame)

    if event == 'line':
      
        logger.info(f"[{ts}] ユニコーーーーーーーーーーーーーーーーーーン！！！")
        cur = frame.f_locals.copy()
        prev = _prev_locals.get(fid, {})

    elif event == 'exception':
        exc_type, exc_value, exc_tb = arg
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        logger.error(f"[{ts}] それでも！！")
        logger.info(f"[{ts}] うぉぉぉおおおおおおおおおおおおおおおお")
        sys.settrace(None)
        sys.exit(1)

    return banagher_links


def start():
    """自動トレースを開始"""
    sys.settrace(banagher_links)
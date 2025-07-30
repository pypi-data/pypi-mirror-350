import json
import socket
from typing import Literal

import requests  # type: ignore

from util_common.datetime import format_now

Level = Literal['error', 'info', 'warning']


def post_message(webhook_url, message: str, level: Level, mentioned_mobile_list: list[str]):
    if level != 'error':
        mentioned_mobile_list = []

    requests.post(
        webhook_url,
        data=json.dumps(
            {
                'msgtype': 'text',
                'text': {
                    'content': f'{format_now()} - {socket.gethostname()}:\n{message}',
                    "mentioned_mobile_list": mentioned_mobile_list,
                },
            }
        ),
    )

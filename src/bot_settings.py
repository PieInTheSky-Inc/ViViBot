import os as _os
from typing import List as _List



DISCORD_BOT_CLIENT_ID: str = _os.environ.get('VIVIBOT_DISCORD_BOT_CLIENT_ID')
DISCORD_BOT_TOKEN: str = _os.environ.get('VIVIBOT_DISCORD_BOT_TOKEN')


PREFIXES: _List[str] = [
    'vivi ',
    'vv '
]


THROW_COMMAND_ERRORS: bool = bool(int(_os.environ.get('THROW_COMMAND_ERRORS', 0)))


VERSION: str = '0.3.3'
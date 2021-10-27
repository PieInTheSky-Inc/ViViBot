import asyncio
from typing import Callable as _Callable
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.core import bot_has_guild_permissions, is_owner

import app_settings
from confirmator import Confirmator
import model
from model import utils


# ---------- Setup ----------

BOT = commands.Bot(
    commands.when_mentioned_or('vivi '),
    intents=discord.Intents.all(),
    activity=discord.activity.Activity(type=discord.ActivityType.playing, name='vivi help')
)



# ---------- Event handlers ----------

@BOT.event
async def on_command_error(ctx: Context, err: Exception) -> None:
    if app_settings.THROW_COMMAND_ERRORS:
        raise err

    if isinstance(err, commands.errors.CommandInvokeError):
        err = err.original
    error_type = type(err).__name__
    error_text = (err.args[0] or '') if err.args else ''
    msg = f'**{error_type}**'
    if error_text:
        msg += f'\n{error_text}'

    await ctx.reply(f'{msg}', mention_author=False)


@BOT.event
async def on_ready() -> None:
    print(f'Bot logged in as {BOT.user.name} ({BOT.user.id})')
    print(f'Bot version: {app_settings.VERSION}')
    extensions = '\n'.join(f'- {key}' for key in BOT.extensions.keys())
    print(f'Loaded extensions:\n{extensions}')



# ---------- Module init ----------

async def __initialize() -> None:
    await model.setup_model()
    BOT.load_extension('about')
    BOT.load_extension('checks')
    BOT.load_extension('roles')
    BOT.load_extension('reactionroles')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__initialize())
    BOT.run(app_settings.DISCORD_BOT_TOKEN)
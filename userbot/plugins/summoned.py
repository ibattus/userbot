from pyrogram import Filters, Message
from userbot import UserBot
from userbot.helpers.file_sending_helpers import send_saved_image
from userbot.helpers.utility import random_interval, human_time
from userbot.database.summon import SUMMON
from userbot.plugins.help import add_command_help
import time


@UserBot.on_message(Filters.command('summonhere', '.') & Filters.me)
async def summon_here(bot: UserBot, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:

        chat_id = chat_details['chat_id']

        if chat_id == message.chat.id:
            await message.edit("```Summon message for this group is already enabled...```")

    elif chat_details is None:
        SUMMON().add_chat_id(message)
        await message.edit("```Summon message for this group has been enabled!!```")

    time.sleep(2)
    await message.delete()


@UserBot.on_message(Filters.command('summonhere', '!') & Filters.me)
async def not_summoned_here(bot: UserBot, message: Message):
    if SUMMON().delete_chat_id(message) is True:
        await message.edit("```Summon message disabled for this chat```")
    else:
        await message.edit("```Summon message for this group was never enabled.```")

    time.sleep(2)
    await message.delete()


@UserBot.on_message(Filters.incoming & Filters.mentioned & ~Filters.reply)
async def summoned(bot: UserBot, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:
        if chat_details['chat_id'] == message.chat.id:
            try:
                last_send = chat_details['last_send']
                next_send = chat_details['next_send']

                if (time.time() - last_send) >= next_send:
                    await send_saved_image(bot, message, "summoned_cat", "summoned_cat.jpg", )
                    last_send = time.time()
                    next_send = random_interval()
                    SUMMON().update(message, last_send, next_send)
            except:
                await send_saved_image(bot, message, "summoned_cat", "summoned_cat.jpg")
                last_send = time.time()
                next_send = random_interval()
                SUMMON().update(message, last_send, next_send)


@UserBot.on_message(Filters.command('nextsummon', '.') & Filters.me)
async def next_summon(bot: UserBot, message: Message):
    chat_details = SUMMON().find_chat_id(message)

    if chat_details is not None:
        if chat_details['chat_id'] == message.chat.id:
            try:
                last_send = chat_details['last_send']
                next_send = chat_details['next_send']

                delta = (last_send + next_send) - time.time()

                await message.edit(f"'''{human_time(seconds=int(delta))}'''")
                time.sleep(6)
                await message.delete()
            except:
                await message.edit("```This group does not have a summon message interval```")
                time.sleep(2)
                await message.delete()
        else:
            await message.delete()
    else:
        await message.delete()


add_command_help(
    'summon', [
        ['.summonhere', 'Enables summoning in the group it is activated in.'],
        ['!summonhere', 'Disables summoning in the group it is activated in.'],
        ['.nextsummon', 'Show the time left for the next summon that will occur in the group.'],
    ]
)

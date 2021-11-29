import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

from oda import app
from oda.database.chats import get_served_chats
from oda.utils.decorators import sudo_users_only, errors
from oda.utils.administrator import adminsOnly
from oda.utils.filters import command
from oda.tgcalls import client as USER
from oda.config import SUDO_USERS, ASSUSERNAME


@app.on_message(command(["userbotjoin", "odajoin"]) & ~filters.private & ~filters.bot)
@errors
async def addchannel(client, message):
    if message.sender_chat:
        return await message.reply_text(
            "You're an __Anonymous Admin__!\nRevert back to User Account."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chid = message.chat.id
    try:
        invite_link = await message.chat.export_invite_link()
        if "+" in invite_link:
            kontol = (invite_link.replace("+", "")).split("t.me/")[1]
            link_bokep = f"https://t.me/joinchat/{kontol}"
    except:
        await message.reply_text(
            "<b>Add me admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"@{ASSUSERNAME}"

    try:
        await USER.join_chat(link_bokep)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} Allready join this Group</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>Flood Wait Error\n{user.first_name} can't join your group due to many join requests for userbot! Make sure the user is not banned in the group."
            "\n\nOr manually add the Assistant bot to your Group and try again.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} Join Seccsesfully</b>",
    )


@USER.on_message(filters.group & command(["userbotleave", "odaleave"]))
async def rem(USER, message):
    if message.sender_chat:
        return await message.reply_text(
            "You're an __Anonymous Admin__!\nRevert back to User Account."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>Users cannot leave your group! Probably waiting for floodwaits.\n\nOr manually remove me from your Group</b>"
        )

        return


@app.on_message(command(["ubleaveall"]) & filters.user(SUDO_USERS) & ~filters.edited)
async def broadcast_message(client, message):
    sleep_time = 0.1
    left = 0
    schats = await get_served_chats()
    chats = [int(chat["chat_id"]) for chat in schats]
    m = await message.reply_text(
        f"Leaving in progress, will take {len(chats) * sleep_time} seconds."
    )
    for i in chats:
        try:
            await USER.leave_chat(i)
            await asyncio.sleep(sleep_time)
            left += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await m.edit(f"**Assistant leave {left} Chats.**")
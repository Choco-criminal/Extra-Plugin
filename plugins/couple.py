from datetime import datetime, timedelta
import pytz
import os
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType
from telegraph import upload_file
from PIL import Image, ImageDraw
import requests

from utils import get_image, get_couple, save_couple
from VIPMUSIC import app


# get current date in GMT+5:30 timezone
def get_today_date():
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")


# get tomorrow's date in GMT+5:30 timezone


def get_todmorrow_date():
    timezone = pytz.timezone("Asia/Kolkata")
    tomorrow = datetime.now(timezone) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")


# Download image from URL


# Dates
tomorrow = get_todmorrow_date()
today = get_today_date()


@app.on_message(filters.command(["couple", "couples"]))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")

    

    try:
        is_selected = await get_couple(cid, today)
        if not is_selected:
            msg = await message.reply_text("❣️")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot and not i.user.is_deleted:
                    list_of_users.append(i.user.id)

            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)

       

            N1 = (await app.get_users(c1_id)).mention
            N2 = (await app.get_users(c2_id)).mention

            

            
            TXT = f"""
**Tᴏᴅᴀʏ's ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ:

{N1} + {N2} = 💘

Nᴇxᴛ ᴄᴏᴜᴘʟᴇs ᴡɪʟʟ ʙᴇ sᴇʟᴇᴄᴛᴇᴅ ᴏɴ {tomorrow}!!**
            """

            if config.START_IMG_URL:
                return await message.reply_video(
                    video=START_IMG_URL,
                    caption=TXT, 
                    reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Aᴅᴅ ᴍᴇ 🌋",
                                url=f"https://t.me/{app.username}?startgroup=true",
                            )
                        ]
                    ]
                ),
            )

            
        else:
            msg = await message.reply_text("❣️")
            
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name

            TXT = f"""
**Tᴏᴅᴀʏ's ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ 🎉:

[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❣️

Nᴇxᴛ ᴄᴏᴜᴘʟᴇs ᴡɪʟʟ ʙᴇ sᴇʟᴇᴄᴛᴇᴅ ᴏɴ {tomorrow}!!**
            """
            if config.START_IMG_URL:
                return await message.reply_video(
                    video=START_IMG_URL,
                    caption=TXT, 
                    reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Aᴅᴅ ᴍᴇ🌋",
                                url=f"https://t.me/{app.username}?startgroup=true",
                            )
                        ]
                    ]
                ),
            )
            print(f"Error during cleanup: {cleanup_error}") 

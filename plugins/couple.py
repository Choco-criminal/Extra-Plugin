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

from config import COUPLE_IMG_URl  # Assuming COUPLE_IMG_URl is defined in config.py

from utils import get_image, get_couple, save_couple
from VIPMUSIC import app


# Get current date in GMT+5:30 timezone
def get_today_date():
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")


# Get tomorrow's date in GMT+5:30 timezone
def get_todmorrow_date():
    timezone = pytz.timezone("Asia/Kolkata")
    tomorrow = datetime.now(timezone) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")


# Dates
tomorrow = get_todmorrow_date()
today = get_today_date()


@app.on_message(filters.command(["couple", "couples"]))
async def ctest(_, message):
    cid = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups.")

    try:
        is_selected = await get_couple(cid, today)

        if not is_selected:
            # No couple selected yet, choose randomly from non-bot members
            msg = await message.reply_text("❣️")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot and not i.user.is_deleted:
                    list_of_users.append(i.user.id)

            if not list_of_users:
                # Handle the case where there are no non-bot members
                return await message.reply_text(
                    "There are no users to choose from. Please add some members to the group."
                )

            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)

            # Ensure chosen users are different
            while c1_id == c2_id:
                c2_id = random.choice(list_of_users)

            N1 = (await app.get_users(c1_id)).mention
            N2 = (await app.get_users(c2_id)).mention

            TXT = f"""
**Today's Couple of the Day:

{N1} + {N2} = 

Next couples will be selected on {tomorrow}!!**
            """

            # Handle optional couple image
            if config.COUPLE_IMG_URL:
                return await message.reply_video(
                    video=COUPLE_IMG_URL,
                    caption=TXT,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Add Me",
                                    url=f"https://t.me/{app.username}?startgroup=true",
                                )
                            ]
                        ]
                    ),
                )
            else:
                return await message.reply_text(TXT)

        else:
            # Couple already selected, retrieve their info
            msg = await message.reply_text("❣️")
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name

            TXT = f"""
**Today's Couple of the Day :

[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❣️

Next couples will be selected on {tomorrow}!!**
            """

            # Handle optional couple image
        

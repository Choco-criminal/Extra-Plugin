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
    chat_id = message.chat.id  # Use chat_id for clarity

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups.")

    try:
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            # Select random users if no couple exists for today
            msg = await message.reply_text("❣️")
            user_list = []

            async for member in app.get_chat_members(chat_id, limit=50):
                if not member.user.is_bot and not member.user.is_deleted:
                    user_list.append(member.user.id)

            user1_id = random.choice(user_list)
            user2_id = random.choice(user_list)
            while user1_id == user2_id:
                user2_id = random.choice(user_list)

            user1 = await app.get_users(user1_id)
            user2 = await app.get_users(user2_id)

            text = f"""
            **Today's Couple of the Day:

            {user1.mention} + {user2.mention} = 

            Next couples will be selected on {tomorrow}!!
            """

            # Use conditional logic to handle COUPLE_IMG_URL availability
            if config.COUPLE_IMG_URL:
                # If COUPLE_IMG_URL is set, use it as a video
                return await message.reply_video(
                    video=config.COUPLE_IMG_URL,
                    caption=text,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(text="Add Me", url=f"https://t.me/{app.username}?startgroup=true")
                            ]
                        ]
                    )
                )
            else:
                # If COUPLE_IMG_URL is not set, use a text message
                return await message.reply_text(text)

        else:
            # If a couple already exists for today, retrieve their details
            msg = await message.reply_text("❣️")
            user1_id = int(is_selected["c1_id"])
            user2_id = int(is_selected["c2_id"])
            user1 = await app.get_users(user1_id)
            user2 = await app.get_users(user2_id)

            text = f"""
**Today's Couple of the Day :

[{user1.first_name}](tg://openmessage?user_id={user1.id}) + [{user2.first_name}](tg://openmessage?user_id={user2.id}) = 

Next couples will be selected on {tomorrow}!!
"""

    except Exception as e:  # Catch any exceptions that might occur
        print(f"An error occurred: {e}")  # Log the error for debugging

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


from utils import get_image, get_couple, save_couple  # Assuming these functions exist
from VIPMUSIC import app  # Assuming this is your bot instance

import config


# Get current date and tomorrow's date in GMT+5:30 timezone
def get_today_date():
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")


def get_tomorrow_date():
    timezone = pytz.timezone("Asia/Kolkata")
    tomorrow = datetime.now(timezone) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")


# Function to download image from URL (implement if needed)
def download_image(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for failed requests

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


# Dates
tomorrow = get_tomorrow_date()
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

            try:
                user1 = await app.get_users(user1_id)
                user2 = await app.get_users(user2_id)
            except Exception as e:
                print(f"Error getting users: {e}")
                # Handle the error gracefully (e.g., send a message saying user not found)
                return await message.reply_text("An error occurred while selecting the couple. Please try again later.")

            text = f"""
            **Today's Couple of the Day:

            {user1.mention} + {user2.mention} = 

            Next couples will be selected on {tomorrow}!!
            """

            if config.COUPLE_IMG_URL:  # Assuming COUPLE_IMG_URL is a valid URL
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
            try:
                user1 = await app.get_users(user1_id)
            except Exception as e:
                print(f"Error getting user 1: {e}")

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

import config   

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
            msg = await message.reply_text("💘")
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
            **🎐 𝑰𝒏 𝒕𝒉𝒆 𝒆𝒎𝒃𝒓𝒂𝒄𝒆 𝒐𝒇 𝒍𝒐𝒗𝒆, 𝒕𝒘𝒐 𝒔𝒐𝒖𝒍𝒔 𝒇𝒊𝒏𝒅 𝒕𝒉𝒆𝒊𝒓 𝒉𝒐𝒎𝒆,
              𝒄𝒓𝒆𝒂𝒕𝒊𝒏𝒈 𝒂 𝒔𝒕𝒐𝒓𝒚 𝒇𝒊𝒍𝒍𝒆𝒅 𝒘𝒊𝒕𝒉 𝒑𝒂𝒔𝒔𝒊𝒐𝒏, 𝒍𝒂𝒖𝒈𝒉𝒕𝒆𝒓, 𝒂𝒏𝒅 𝒇𝒐𝒓𝒆𝒗𝒆𝒓 𝒎𝒐𝒎𝒆𝒏𝒕𝒔.
              ┏━━━━━━━━━━━━━━━━━━━━━┓
              ✧ Cᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ Dᴀʏ 💞
                       
              ✧ {user1.mention} + {user2.mention}
              ┗━━━━━━━━━━━━━━━━━━━━━┛
              Nᴇxᴛ Cᴏᴜᴘʟᴇ Sᴇʟᴇᴄᴛɪᴏɴ: 𝚜𝚘𝚘𝚗 🎀
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
            msg = await message.reply_text("💘")
            user1_id = int(is_selected["c1_id"])
            user2_id = int(is_selected["c2_id"])
            user1 = await app.get_users(user1_id)
            user2 = await app.get_users(user2_id)

            text = f"""
            **🎐 𝑰𝒏 𝒕𝒉𝒆 𝒆𝒎𝒃𝒓𝒂𝒄𝒆 𝒐𝒇 𝒍𝒐𝒗𝒆, 𝒕𝒘𝒐 𝒔𝒐𝒖𝒍𝒔 𝒇𝒊𝒏𝒅 𝒕𝒉𝒆𝒊𝒓 𝒉𝒐𝒎𝒆,
              𝒄𝒓𝒆𝒂𝒕𝒊𝒏𝒈 𝒂 𝒔𝒕𝒐𝒓𝒚 𝒇𝒊𝒍𝒍𝒆𝒅 𝒘𝒊𝒕𝒉 𝒑𝒂𝒔𝒔𝒊𝒐𝒏, 𝒍𝒂𝒖𝒈𝒉𝒕𝒆𝒓, 𝒂𝒏𝒅 𝒇𝒐𝒓𝒆𝒗𝒆𝒓 𝒎𝒐𝒎𝒆𝒏𝒕𝒔.
              ┏━━━━━━━━━━━━━━━━━━━━━┓
              ✧ Cᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ Dᴀʏ 💞
                       
              ✧ {user1.mention} + {user2.mention}
              ┗━━━━━━━━━━━━━━━━━━━━━┛
              Nᴇxᴛ Cᴏᴜᴘʟᴇ Sᴇʟᴇᴄᴛɪᴏɴ: 𝚜𝚘𝚘𝚗 🎀
                   """

    except Exception as e:  # Catch any exceptions that might occur
        print(f"An error occurred: {e}")  # Log the error for debugging

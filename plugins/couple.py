from datetime import datetime, timedelta
import pytz
import random
from pyrogram import filters
from pyrogram.types import InputMediaAnimation
from pyrogram.enums import ChatType
from ANNIEMUSIC import app  # Make sure you import your app correctly
from utils import get_image, get_couple, save_couple

# Get current date in GMT+5:30 timezone
def get_today_date():
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")

# Get tomorrow's date in GMT+5:30 timezone
def get_tomorrow_date():
    timezone = pytz.timezone("Asia/Kolkata")
    tomorrow = datetime.now(timezone) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")

# Dates
tomorrow = get_tomorrow_date()
today = get_today_date()

@app.on_message(filters.command(["couple", "couples"]))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups.")

    try:
        is_selected = await get_couple(cid, today)
        if not is_selected:
            msg = await message.reply_text("💞")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot and not i.user.is_deleted:
                    list_of_users.append(i.user.id)

            if len(list_of_users) < 2:
                return await msg.edit("Not enough users to form a couple.")

            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c2_id = random.choice(list_of_users)

            N1 = (await app.get_users(c1_id)).mention
            N2 = (await app.get_users(c2_id)).mention

            # Prepare the message text
            TXT = f"""
           **🎐 𝑰𝒏 𝒕𝒉𝒆 𝒆𝒎𝒃𝒓𝒂𝒄𝒆 𝒐𝒇 𝒍𝒐𝒗𝒆, 𝒕𝒘𝒐 𝒔𝒐𝒖𝒍𝒔 𝒇𝒊𝒏𝒅 𝒕𝒉𝒆𝒊𝒓 𝒉𝒐𝒎𝒆,
                𝒄𝒓𝒆𝒂𝒕𝒊𝒏𝒈 𝒂 𝒔𝒕𝒐𝒓𝒚 𝒇𝒊𝒍𝒍𝒆𝒅 𝒘𝒊𝒕𝒉 𝒑𝒂𝒔𝒔𝒊𝒐𝒏, 𝒍𝒂𝒖𝒈𝒉𝒕𝒆𝒓, 𝒂𝒏𝒅 𝒇𝒐𝒓𝒆𝒗𝒆𝒓 𝒎𝒐𝒎𝒆𝒏𝒕𝒔.
               ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                ✧Cᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ Dᴀʏ 💞
                       
                ✧{user1.mention} + {user2.mention}
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
               Nᴇxᴛ Cᴏᴜᴘʟᴇ Sᴇʟᴇᴄᴛɪᴏɴ: {tomorrow} 🎀
            **
            """

            # Delete the initial message
            await msg.delete()

            # List of GIF URLs to choose from
            gif_urls = [
                "https://telegra.ph/file/6ae3a399b96f70b6fda79.mp4",
                "https://telegra.ph/file/5df37a776933bb427b528.mp4",
                "https://telegra.ph/file/85a35e5a79525b70f5904.mp4",
                "https://telegra.ph/file/75764b093a76d08f51d2c.mp4",
                "https://telegra.ph/file/ea951700bb21f53df70c9.mp4",
                "https://telegra.ph/file/b74553a355a110d9a016b.mp4",
                "https://telegra.ph/file/959dc8b67413e50f1c4a5.mp4",
                "https://graph.org/file/2a7f857f31b32766ac6fc.mp4",
                "https://graph.org/file/83ebf52e8bbf138620de7.mp4",
                "https://graph.org/file/ba7699c28dab379b518ca.mp4"
            ]

            # Choose a random GIF URL
            gif_url = random.choice(gif_urls)

            # Send the GIF with the message
            await message.reply_video(video=gif_url, caption=TXT)

            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(cid, today, couple)

        else:
            # Handle the case when a couple has already been selected
            msg = await message.reply_text("❣️")
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name

            TXT = f"""
             ** 🎐 𝑰𝒏 𝒕𝒉𝒆 𝒆𝒎𝒃𝒓𝒂𝒄𝒆 𝒐𝒇 𝒍𝒐𝒗𝒆, 𝒕𝒘𝒐 𝒔𝒐𝒖𝒍𝒔 𝒇𝒊𝒏𝒅 𝒕𝒉𝒆𝒊𝒓 𝒉𝒐𝒎𝒆,
                𝒄𝒓𝒆𝒂𝒕𝒊𝒏𝒈 𝒂 𝒔𝒕𝒐𝒓𝒚 𝒇𝒊𝒍𝒍𝒆𝒅 𝒘𝒊𝒕𝒉 𝒑𝒂𝒔𝒔𝒊𝒐𝒏, 𝒍𝒂𝒖𝒈𝒉𝒕𝒆𝒓, 𝒂𝒏𝒅 𝒇𝒐𝒓𝒆𝒗𝒆𝒓 𝒎𝒐𝒎𝒆𝒏𝒕𝒔.
               ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                ✧Cᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ Dᴀʏ 💞
                       
                ✧{user1.mention} + {user2.mention}
               ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
               Nᴇxᴛ Cᴏᴜᴘʟᴇ Sᴇʟᴇᴄᴛɪᴏɴ: {tomorrow} 🎀
            **
            """

            # Choose a random GIF URL from the list
            gif_url = random.choice(gif_urls)

            # Delete the initial message and send the GIF with the message
            await msg.delete()
            await message.reply_animation(animation=gif_url, caption=TXT)

    except Exception as e:
        print("Error occurred:", str(e))
    finally:
        # Cleanup code (if any files are created)
        pass

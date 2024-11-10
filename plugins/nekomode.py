import random
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from ANNIEMUSIC import app
from ANNIEMUSIC.misc import SUDOERS
from config import OWNER_ID
from pyrogram.enums import ChatAction

# Define AUTHORIZED_USERS who can use certain commands
AUTH_USER = [1266240012]  # Add more user IDs as needed

# NSFW commands restricted to OWNER_ID, SUDOERS, and AUTH_USER
@app.on_message(filters.command(["neko", "blowjob", "cum", "anal", "fuck", "pussy", "nekoX", "yaoi", "yuri"])) 
async def get_image(_, m):
    # Check if the user is authorized
    if m.from_user.id not in AUTH_USER:
        await m.reply_text("𝚗𝚊𝚞𝚐𝚑𝚝𝚢 𝚑𝚘𝚛𝚊 𝚑𝚊𝚒 𝚋𝚔𝚕.")
        return

    # API links dictionary
    api_links = {
        "neko": {"api": "https://purrbot.site/api/img/sfw/neko/gif"},
        "blowjob": {"api": "https://purrbot.site/api/img/nsfw/blowjob/gif"},
        "cum": {"api": "https://purrbot.site/api/img/nsfw/cum/gif"},
        "anal": {"api": "https://purrbot.site/api/img/nsfw/anal/gif"},
        "fuck": {"api": "https://purrbot.site/api/img/nsfw/fuck/gif"},
        "pussy": {"api": "https://purrbot.site/api/img/nsfw/pussylick/gif"},
        "nekoX": {"api": "https://purrbot.site/api/img/nsfw/neko/gif"},
        "yaoi": {"api": "https://purrbot.site/api/img/nsfw/yaoi/gif"},
        "yuri": {"api": "https://purrbot.site/api/img/nsfw/yuri/gif"}
    }

    command = m.text[1:]  # Remove the "/" from the command
    api_url = api_links.get(command, {}).get('api')

    if api_url:
        api_response = requests.get(api_url).json()
        url = api_response.get('link') if 'link' in api_response else api_response.get('url')
        await app.send_animation(chat_id=m.chat.id, animation=url)
    else:
        await m.reply("𝚗𝚊𝚞𝚐𝚑𝚝𝚢 𝚑𝚘𝚛𝚊 𝚑𝚊𝚒 𝚋𝚔𝚕.")

# SFW commands open to everyone
@app.on_message(filters.command(["waifu", "neko"]))
async def image(_, m):
    api_urls = {
        "waifu": ["https://api.waifu.pics/sfw/waifu", "https://nekos.best/api/v2/waifu"],
        "neko": ["https://api.waifu.pics/sfw/neko", "https://nekos.best/api/v2/neko"],
    }

    command = m.text.split()[0][1:]  # Extract the command from the message
    selected_api = random.choice(api_urls.get(command, []))

    if selected_api:
        api = requests.get(selected_api).json()
        url = api['url'] if "url" in api else api["results"][0]['url']
        await app.send_photo(chat_id=m.chat.id, photo=url)
    else:
        await m.reply("Invalid command.")

# NSFW hentai command for authorized users
@app.on_message(filters.command("hentai"))
async def hentai(_, m):
    # Check if the user ID is in the list of authorized users
    if m.from_user.id not in AUTH_USER:
        await m.reply_text("naughty hora bll.")
        return

    # If the user is authorized, proceed with the API request
    api = requests.get("https://api.waifu.pics/nsfw/waifu").json()
    url = api['url']
    await app.send_photo(chat_id=m.chat.id, photo=url)

# Another neko command for everyone
@app.on_message(filters.command("neko"))
async def neko(_, m):
    api = requests.get("https://purrbot.site/api/img/sfw/neko/gif").json()
    url = api['link']
    await app.send_animation(chat_id=m.chat.id, animation=url)

# Multiple action commands open to all
@app.on_message(filters.command(["kill", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "spank", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "wink", "poke", "dance", "cringe", "tickle"]))
async def get_animation(_, m):
    api_links = {
        "kill": {"api": "https://api.waifu.pics/sfw/kill"},
        "megumin": {"api": "https://api.waifu.pics/sfw/megumin"},
        "bully": {"api": "https://nekos.best/api/v2/bully"},
        "cuddle": {"api": "https://nekos.best/api/v2/cuddle"},
        "cry": {"api": "https://nekos.best/api/v2/cry"},
        "hug": {"api": "https://nekos.best/api/v2/hug"},
        "awoo": {"api": "https://api.waifu.pics/sfw/awoo"},
        "kiss": {"api": "https://nekos.best/api/v2/kiss"},
        "lick": {"api": "https://api.waifu.pics/sfw/lick"},
        "pat": {"api": "https://api.waifu.pics/sfw/pat"},
        "smug": {"api": "https://api.waifu.pics/sfw/smug"},
        "bonk": {"api": "https://api.waifu.pics/sfw/bonk"},
        "yeet": {"api": "https://api.waifu.pics/sfw/yeet"},
        "blush": {"api": "https://nekos.best/api/v2/blush"},
        "smile": {"api": "https://api.waifu.pics/sfw/smile"},
        "spank": {"api": "https://api.waifu.pics/sfw/spank"},
        "wave": {"api": "https://api.waifu.pics/sfw/wave"},
        "highfive": {"api": "https://api.waifu.pics/sfw/highfive"},
        "handhold": {"api": "https://api.waifu.pics/sfw/handhold"},
        "nom": {"api": "https://api.waifu.pics/sfw/nom"},
        "bite": {"api": "https://api.waifu.pics/sfw/bite"},
        "glomp": {"api": "https://api.waifu.pics/sfw/glomp"},
        "slap": {"api": "https://nekos.best/api/v2/slap"},
        "wink": {"api": "https://nekos.best/api/v2/wink"},
        "poke": {"api": "https://api.waifu.pics/sfw/poke"},
        "dance": {"api": "https://nekos.best/api/v2/dance"},
        "cringe": {"api": "https://api.waifu.pics/sfw/cringe"},
        "tickle": {"api": "https://api.waifu.pics/sfw/tickle"},
    }

    command = m.text[1:]  # Remove the "/" from the command
    api_url = api_links.get(command, {}).get('api')

    if api_url:
        api = requests.get(api_url).json()
        url = api['url'] if "url" in api else api["results"][0]['url']
        await app.send_animation(chat_id=m.chat.id, animation=url)
    else:
        await m.reply("Invalid command.")

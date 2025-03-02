import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import youtube_dl

# Import config
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize bot
bot = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(bot)

# Dictionary to store queues
queues = {}

# Function to download audio
def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        "outtmpl": "song.%(ext)s",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "song.mp3"

# Play music command
@bot.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a **YouTube URL** or **song name**!")

    url = message.command[1]
    await message.reply("Downloading music, please wait... 🎵")
    audio_file = download_audio(url)

    chat_id = message.chat.id

    if chat_id not in queues:
        queues[chat_id] = []
    
    queues[chat_id].append(audio_file)

    if len(queues[chat_id]) == 1:
        await play_next_song(chat_id, message)

# Play next song in queue
async def play_next_song(chat_id, message):
    if queues[chat_id]:
        song = queues[chat_id].pop(0)
        await call_py.join_group_call(chat_id, AudioPiped(song))
        await message.reply(f"🎶 Now playing: {song}")
    else:
        await message.reply("Queue is empty!")

# Pause music
@bot.on_message(filters.command("pause") & filters.group)
async def pause_music(client, message):
    chat_id = message.chat.id
    await call_py.pause_stream(chat_id)
    await message.reply("⏸ Music paused!")

# Resume music
@bot.on_message(filters.command("resume") & filters.group)
async def resume_music(client, message):
    chat_id = message.chat.id
    await call_py.resume_stream(chat_id)
    await message.reply("▶️ Music resumed!")

# Skip music
@bot.on_message(filters.command("skip") & filters.group)
async def skip_music(client, message):
    chat_id = message.chat.id
    await call_py.leave_group_call(chat_id)
    await play_next_song(chat_id, message)
    await message.reply("⏭ Skipping to the next song...")

# Stop music
@bot.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    chat_id = message.chat.id
    queues[chat_id] = []
    await call_py.leave_group_call(chat_id)
    await message.reply("⏹ Music stopped!")

# Start the bot
bot.start()
call_py.start()
print("🎵 Music Bot is Running...")
bot.idle()

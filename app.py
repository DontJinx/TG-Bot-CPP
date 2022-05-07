#@voidautobot
import os
import asyncio
import wget
from pyrogram import Client, filters
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import json
import imdb
import os

bot = Client(
    "Music Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"] 
)

OMDB_API_KEY = '558c75c8'
BOT_TOKEN = "5142295957:AAEiQ-DMehSmGNBD13Hn1KlRZUblLOCTU-Y"
API_ID = 8297647
API_HASH = "3aff526a1127dd7c27cdb62fd8ba281a"

START_TEXT = """
Hi **{}** 👋

Just send me a song name and I'll send the audio to you on Telegram.

__Follow dev on github [ABHI](https://github.com/DontJinx)__

__Made by **@Sync_0**__
"""

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
    msg = START_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg, disable_web_page_preview=True)
    
    
@bot.on_message(filters.text & filters.private & ~filters.command("song"))
async def get_songs(_, message):
    query = message.text
    m = await message.reply_text("Searching", quote=True)
    search = SearchVideos(f"{query}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    lenk = mio[0]["link"]
    title = mio[0]["title"]                               #pyrogram
    ytid = mio[0]["id"]
    channel = mio[0]["channel"]
    #views = mio[0]["views"]
    dur = mio[0]["duration"]
    tblink = f"https://img.youtube.com/vi/{ytid}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    tb = wget.download(tblink)
    
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    
    await m.edit("Downloading speed could be slow. Please hold on...")
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(lenk, download=True)
    except Exception as e:
        return await m.edit(f"**Download Failed** \n\n```{e}```")
      
    cap = f"**🎧 Title:** {title} \n**🎥 Channel:** {channel} \n**⏳ Duration:** {dur} \n\n**📮 By @voidautobot**"
    aud = f"{ytdl_data['id']}.mp3"
    await m.edit("Uploading")
    await message.reply_audio(audio=open(aud, "rb"), 
                              duration=int(ytdl_data["duration"]), 
                              title=str(ytdl_data["title"]), 
                              performer=str(ytdl_data["uploader"]),
                              thumb=tb,
                              caption=cap,
                              quote=True)
    await m.delete()
    for files in (tb, aud):
        if files and os.path.exists(files):
            os.remove(files)


ia = imdb.IMDb() 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def help(update, context):
    update.message.reply_text('Send me the name of any movie to get its details. \nTry out "Avengers Endgame"')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def reply(update, context):
    movie_name=update.message.text
    search = ia.search_movie(movie_name)
      
    id='tt'+search[0].movieID
    
    url= 'http://www.omdbapi.com/?i='+id+'&apikey='+OMDB_API_KEY
    
    x=urllib.request.urlopen(url)
    
    for line in x:
        x=line.decode()
    
    data=json.loads(x)
    
    ans=''
    ans+='*'+data['Title']+'* ('+data['Year']+')'+'\n\n'
    ans+='*IMDb Rating*: '+data['imdbRating']+' \n'
    ans+='*Cast*: '+data['Actors']+'\n'
    ans+='*Genre*: '+data['Genre']+'\n\n'
    ans+='*Plot*: '+data['Plot']+'\n'
    ans+='[.]('+data['Poster']+')'
    update.message.reply_text(ans,parse_mode='markdown')  


def main():

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 
    
    
bot.run()

import os
import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Настройки для идеального звука
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k'
}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'default_search': 'ytsearch',
    'noplaylist': True,
    'quiet': True,
}

class MusicBot(commands.Bot):
    def __init__(self):
        # Статус со ссылкой на твой сайт
        activity = discord.Activity(type=discord.ActivityType.listening, name="dazrex.pages.dev")
        super().__init__(command_prefix='!', intents=discord.Intents.all(), activity=activity, help_command=None)

    async def on_ready(self):
        print(f"🚀 DAZREX SYSTEM ONLINE: {self.user.name}")

bot = MusicBot()

@bot.command(name='help', aliases=['хелп', 'помощь'])
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 Bot Commands / Команды бота",
        description="Music & Info system for **dazrex.pages.dev**",
        color=0x00ff00
    )
    
    # English Section
    embed.add_field(
        name="🇬🇧 English",
        value=(
            "`!p [link/name]` - Play music from YT / SoundCloud / Spotify\n"
            "`!s` - Stop music and leave channel\n"
            "`!info` - Show owner's website\n"
            "`!help` - Show this message"
        ),
        inline=False
    )
    
    # Russian Section
    embed.add_field(
        name="🇷🇺 Русский",
        value=(
            "`!p [ссылка/название]` - Играть музыку из YT / SoundCloud / Spotify\n"
            "`!s` - Остановить музыку и выйти\n"
            "`!info` - Показать сайт владельца\n"
            "`!help` - Показать это сообщение"
        ),
        inline=False
    )
    
    embed.set_footer(text="Developed for dazrex.pages.dev")
    await ctx.send(embed=embed)

@bot.command(name='p', aliases=['play', 'плей'])
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("❌ Join a voice channel first! / Сначала зайди в голосовой канал!")

    vc = ctx.voice_client or await ctx.author.voice.channel.connect()

    async with ctx.typing():
        query = f"ytsearch:{search}" if not search.startswith("http") else search
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info: info = info['entries'][0]
            url = info['url']
            
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            if vc.is_playing(): vc.stop()
            vc.play(source)
            await ctx.send(f"🎶 **Playing:** {info['title']}\n🔗 [dazrex.pages.dev](https://dazrex.pages.dev)")

@bot.command(name='s', aliases=['stop', 'стоп'])
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹ Stopped / Остановлено")

@bot.command(name='info', aliases=['инфо', 'site'])
async def site_info(ctx):
    await ctx.send("🌐 My website / Мой сайт: https://dazrex.pages.dev")

# ПЛАН Б: Берем токен из переменных Koyeb
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ ERROR: DISCORD_TOKEN not found in Koyeb settings!")
    

import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Настройки для идеального звука на ПК (высокий битрейт)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k'
}

# Настройки поиска: YouTube + SoundCloud
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'default_search': 'ytsearch',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

class MusicBot(commands.Bot):
    def __init__(self):
        # Автоматический статус: "Слушает dazrex.pages.dev"
        activity = discord.Activity(type=discord.ActivityType.listening, name="dazrex.pages.dev")
        super().__init__(command_prefix='!', intents=discord.Intents.all(), activity=activity)

    async def on_ready(self):
        print("\n" + "═"*50)
        print(f"🚀 СИСТЕМА DAZREX ЗАПУЩЕНА")
        print(f"🌐 МОЙ САЙТ: https://dazrex.pages.dev")
        print(f"👤 БОТ: {self.user.name}")
        print("═"*50 + "\n")

bot = MusicBot()

@bot.command(name='p', aliases=['play', 'плей', 'играть'])
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("❌ Сначала зайди в голосовой канал!")

    vc = ctx.voice_client or await ctx.author.voice.channel.connect()

    async with ctx.typing():
        # Если кидаешь ссылку на Spotify - ищем её на YouTube автоматически
        query = f"ytsearch:{search}" if not search.startswith("http") or "spotify" in search else search
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info: info = info['entries'][0]
                
                url = info['url']
                title = info.get('title', 'Без названия')
                thumb = info.get('thumbnail', '')
                
                source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                
                if vc.is_playing(): vc.stop()
                vc.play(source)

                # КРАСИВАЯ КАРТОЧКА С ТВОИМ САЙТОМ
                embed = discord.Embed(
                    title="🎶 СЕЙЧАС ИГРАЕТ",
                    description=f"**{title}**\n\n🔗 [Посети мой сайт](https://dazrex.pages.dev)",
                    color=0x5865F2 # Фирменный цвет Discord
                )
                if thumb: embed.set_thumbnail(url=thumb)
                embed.add_field(name="Качество", value="192kbps Hi-Fi", inline=True)
                embed.add_field(name="Источник", value="YouTube HQ", inline=True)
                embed.set_footer(text="Cloudflare Pages | dazrex.pages.dev", icon_url=bot.user.avatar.url if bot.user.avatar else None)
                
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"⚠️ Ошибка: {e}")

@bot.command(name='s', aliases=['stop', 'стоп', 'выход'])
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹ Музыка выключена. Жду тебя на **dazrex.pages.dev**")

@bot.command(name='сайт', aliases=['site'])
async def site_info(ctx):
    await ctx.send("🌐 Мой сайт на Cloudflare Pages: https://dazrex.pages.dev")

bot.run('MTQ2MDczNDA1MzI0OTcxMjEyOQ.G2w4pY.7V3RiNHm_ztvUlXPjL0zpZP6S_Es1Dj2EdMNvM')

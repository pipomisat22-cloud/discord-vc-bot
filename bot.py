import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import threading
from flask import Flask

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ---- Flask keep-alive server ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive! 🤖", 200

@app.route("/health")
def health():
    return {"status": "ok", "bot": str(bot.user) if bot.user else "loading"}, 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# ---- Discord Bot ----
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว: {bot.user} (ID: {bot.user.id})")
    print("-------------------------------------------")

    # Auto-join voice channel on startup
    channel_id = os.getenv("VOICE_CHANNEL_ID")
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                await channel.connect(self_deaf=True, self_mute=True)
                await channel.guild.change_voice_state(
                    channel=channel,
                    self_deaf=True,
                    self_mute=True,
                )
                print(f"[AUTO-JOIN] เข้าห้อง: {channel.name}")
            except Exception as e:
                print(f"[AUTO-JOIN ERROR] {e}")
        else:
            print(f"[AUTO-JOIN] ไม่เจอห้อง ID: {channel_id}")
    else:
        print("[AUTO-JOIN] ไม่ได้ตั้ง VOICE_CHANNEL_ID — ใช้คำสั่ง !join แทน")


@bot.command(name="join")
async def join(ctx, *, channel_name: str = None):
    """เข้าห้อง Voice แบบปิดหูปิดไมค์"""
    if channel_name:
        vc_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
        if not vc_channel:
            await ctx.send(f"❌ ไม่เจอห้อง **{channel_name}**")
            return
    elif ctx.author.voice and ctx.author.voice.channel:
        vc_channel = ctx.author.voice.channel
    else:
        await ctx.send("❌ กรุณาอยู่ในห้อง Voice หรือระบุชื่อห้องด้วย `!join <ชื่อห้อง>`")
        return

    if ctx.voice_client:
        await ctx.voice_client.move_to(vc_channel)
    else:
        await vc_channel.connect(self_deaf=True, self_mute=True)

    await ctx.guild.change_voice_state(
        channel=vc_channel,
        self_deaf=True,
        self_mute=True,
    )

    await ctx.send(f"🔇 เข้าห้อง **{vc_channel.name}** แล้ว (ปิดหู + ปิดไมค์)")


@bot.command(name="leave")
async def leave(ctx):
    """ออกจากห้อง Voice"""
    if ctx.voice_client:
        channel_name = ctx.voice_client.channel.name
        await ctx.voice_client.disconnect()
        await ctx.send(f"👋 ออกจากห้อง **{channel_name}** แล้ว")
    else:
        await ctx.send("❌ บอทไม่ได้อยู่ในห้อง Voice")


@bot.command(name="status")
async def status(ctx):
    """เช็คสถานะบอท"""
    if ctx.voice_client and ctx.voice_client.is_connected():
        vc = ctx.voice_client
        await ctx.send(
            f"📊 **สถานะบอท**\n"
            f"ห้อง: **{vc.channel.name}**\n"
            f"ปิดหู: {'✅' if vc.self_deaf else '❌'}\n"
            f"ปิดไมค์: {'✅' if vc.self_mute else '❌'}"
        )
    else:
        await ctx.send("📊 บอทยังไม่ได้เข้าห้อง Voice")


# Start keep-alive server ก่อน run bot
keep_alive()
bot.run(TOKEN)

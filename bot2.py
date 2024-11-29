import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@client.command(name="wake")
async def wake(ctx, user: discord.Member):
    if not user.voice:
        await ctx.send(f"{user.mention} is not in a voice channel.")
        return

    voice_channels = ctx.guild.voice_channels
    for _ in range(10):  # Repeat 10 times
        for channel in voice_channels:
            await user.move_to(channel)
            await asyncio.sleep(0.1)  # 100 ms delay

    await ctx.send(f"{user.mention} has been thoroughly awakened!")

client.run("MTIyMDI3MjMwNDYyNjMzNTc3Ng.GAyFvc.nPHiuzSasLN-JiBP6bcZoRCP0ehmjU2MrSePBM")
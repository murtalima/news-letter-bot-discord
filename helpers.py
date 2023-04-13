import time


async def make_members_roll(message):
    for member in message.mentions:
        await roller(member=member, guild=message.guild)


async def roller(member, guild):
    for channel in guild.voice_channels:
        await member.move_to(channel=channel)
        time.sleep(0.4)

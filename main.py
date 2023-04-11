import asyncio
import os
import time
import discord
from dotenv import load_dotenv
from backendProvider import BackendProvider

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

backendProvider = BackendProvider(3000, '192.168.0.18')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    backendProvider.createUser(360209386682974208, 'Primata(MacacoLima)', True, False, client.guilds[0])

    for guild in client.guilds:
        backendProvider.createGuild(guild.id, guild.name, guild.member_count)


@client.event
async def on_voice_state_update(member, before, after):
    response = backendProvider.findUser(member.id)

    if response.status_code == 200:
        response_json = response.json()

        if not any(str(member.guild.id) in guild['discordId'] for guild in response_json['guilds']):
            backendProvider.updateUser(
                response_json['discordId'],
                response_json['name'],
                response_json['isAdm'],
                response_json['isMuted'],
                member.guild.id
            )

        user = response.json()

        if user['isMuted'] and (not after.mute or not after.deaf):
            await member.edit(mute=True, deafen=True)

        if user['isAdm'] and (after.mute or after.deaf):
            await member.edit(mute=False, deafen=False)
    if response.status_code == 404:
        backendProvider.createUser(member.id, member.name, False, False, member.guild.id)


@client.event
async def on_message(message):
    response = backendProvider.findUser(message.author.id)

    if response.status_code == 200:
        user = response.json()
        
        if not any(str(message.guild.id) in guild['discordId'] for guild in user['guilds']):
            backendProvider.updateUser(
                user['discordId'],
                user['name'],
                user['isAdm'],
                user['isMuted'],
                message.guild.id
            )

        is_user_adm = user['isAdm']
        if is_user_adm:
            if message.content.startswith('$'):
                await message.delete()

            if message.content.startswith('$hello'):
                await message.channel.send('Hello')

            if message.content.startswith('$roda roda'):
                await asyncio.gather(teste(message))

            if message.content.startswith('$nao fala comigo'):
                for member in message.mentions:
                    if response.status_code == 200:
                        user = response.json()
                        backendProvider.updateUser(member.id, member.name, user['isAdm'], True)

                        try:
                            await member.edit(mute=True, deafen=True)
                        except:
                            pass
                    elif response.status_code == 404:
                        backendProvider.createUser(member.id, member.name, False)

            if message.content.startswith('$fala comigo'):
                for member in message.mentions:
                    if response.status_code == 200:
                        user = response.json()
                        backendProvider.updateUser(member.id, member.name, user['isAdm'], False)
                        try:
                            await member.edit(mute=False, deafen=False)
                        except:
                            pass

            if message.content.startswith('$add'):
                for member in message.mentions:
                    response = backendProvider.findUser(member.id)
                    if response.status_code == 200:
                        user = response.json()
                        if user['isAdm']:
                            await message.channel.send(member.name + ' ja é Adm')

                        update_response = backendProvider.updateUser(member.id, member.name, True, False)

                        if update_response.status_code != 200:
                            await message.channel.send(member.name + ' erro ao transformar em adm')

                    elif response.status_code == 404:
                        backendProvider.createUser(member.id, member.name, True, False, message.guild.id)

            if message.content.startswith('$remove'):
                for member in message.mentions:
                    response = backendProvider.findUser(member.id)
                    if response.status_code == 200:
                        user = response.json()

                        if user['isAdm'] == False:
                            await message.channel.send(member.name + ' não tem poderes de adm')

                        update_response = backendProvider.updateUser(member.id, member.name, False, False)

                        if update_response.status_code != 200:
                            await message.channel.send(member.name + ' erro ao transformar em adm')

                    elif response.status_code == 404:
                        backendProvider.createUser(member.id, member.name, False, False)

    print(message.author.id, message.author.name, ' -> ', message.content)


async def teste(message):
    for member in message.mentions:
        await roller(member=member, guild=message.guild)


async def roller(member, guild):
    for channel in guild.voice_channels:
        await member.move_to(channel=channel)
        time.sleep(0.4)


client.run(TOKEN)

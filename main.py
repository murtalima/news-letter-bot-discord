import asyncio
import os
import discord

from views import MyView
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from backendProvider import BackendProvider
from helpers import make_members_roll
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
backendProvider = BackendProvider(3000, '192.168.0.18')

@tree.command(name = "hello", description = "Fala hello", guild=discord.Object(id=451143076983865344))
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(name = "news", description = "Busca noticias do newsletters", guild=discord.Object(id=451143076983865344))
async def news(interaction):
    response=backendProvider.getNewspaper(interaction.user.id)
    if(response.status_code == 200):
        content =response.json()['content']
        embed = discord.Embed(
                    description=content,
                    color= discord.Color.blue()
                )
        await interaction.response.send_message(embed=embed, view=MyView())

@client.event
async def on_voice_state_update(member, before, after):
    response = backendProvider.findUser(member.id)

    if response.status_code == 200:
        response_json = response.json()

        if not any(str(member.guild.id) in guild['discordId'] for guild in response_json['guilds']):
            print('a')
            backendProvider.addGuildUsers(member.id, member.guild.id)

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
            backendProvider.addGuildUsers(message.author.id, message.guild.id)
            
        is_user_adm = user['isAdm']
        
        if is_user_adm:
            if message.content.startswith('$roda roda'):
                await asyncio.gather(make_members_roll(message))

            if message.content.startswith('$nao fala comigo'):
                for member in message.mentions:
                    if response.status_code == 200:
                        response = backendProvider.findUser(member.id)
                        user = response.json()
                        backendProvider.updateUser(member.id, member.name, False, True)

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
                        backendProvider.updateUser(member.id, member.name, False, False)
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

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=451143076983865344))
    print(f'{client.user} has connected to Discord!')
    backendProvider.createUser(360209386682974208, 'Primata(MacacoLima)', True, False, client.guilds[0])

    for guild in client.guilds:
        res = backendProvider.createGuild(guild.id, guild.name, guild.member_count)


client.run(TOKEN)
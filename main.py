import os
import discord

from discord import app_commands
from dotenv import load_dotenv
from services.backend_service import BackendService
from events.on_voice_state_update_event import OnVoiceStateUpdateEvent
from events.on_message_event import OnMessageEvent
from services.commands_service import CommandsService

load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
backend_service = BackendService(3000, BACKEND_URL)
on_message_event = OnMessageEvent(backend_service=backend_service)
on_voice_state_update_event = OnVoiceStateUpdateEvent(backend_service=backend_service)
commands = CommandsService(backend_service=backend_service)

@tree.command(name = "hello", description = "Fala hello")
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(name = "news", description = "Busca noticias do newsletters")
async def news(interaction):
    await commands.news(interaction)

@client.event
async def on_voice_state_update(member, before, after):
    await on_voice_state_update_event.exec(member,before,after)

@client.event
async def on_message(message):
    await on_message_event.exec(message)

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
    backend_service.createUser(360209386682974208, 'Primata(MacacoLima)', True, False, client.guilds[0])

    for guild in client.guilds:
        backend_service.createGuild(guild.id, guild.name, guild.member_count)


client.run(TOKEN)
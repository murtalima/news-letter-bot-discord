from typing import Optional
import discord
from ..backend_service import BackendService

class NewsView(discord.ui.View):   
    
    @discord.ui.button(label="Like", row=0, style=discord.ButtonStyle.green)
    async def first_button_callback(self, interaction, button):
        backend_provider = BackendService(3000, '192.168.0.18')
        
        embed = interaction.message.embeds[0]
        
        id = interaction.message.embeds[0].fields[3].value
        response = backend_provider.gradeNewspaper(interaction.user.id, id, 'Like')
        response_json = response.json()
        
        new_embed = discord.Embed(color= discord.Color.blue())
        new_embed.add_field(name= 'likes', value=response_json['likes'], inline= True)
        new_embed.add_field(name= 'dislikes', value=response_json['dislikes'], inline= True)
        new_embed.add_field(name= 'views', value=response_json['views'], inline= True)
        new_embed.add_field(name= 'id', value=id, inline= True)
        
        await interaction.response.edit_message(embed=new_embed)

    @discord.ui.button(label="Dislike", row=0, style=discord.ButtonStyle.red)
    async def second_button_callback(self, interaction, button):
        backend_provider = BackendService(3000, '192.168.0.18')
        
        embed = interaction.message.embeds[0]
        
        id = interaction.message.embeds[0].fields[3].value
        response = backend_provider.gradeNewspaper(interaction.user.id, id, 'Dislike')
        response_json = response.json()
        
        new_embed = discord.Embed(color= discord.Color.blue())
        new_embed.add_field(name= 'likes', value=response_json['likes'], inline= True)
        new_embed.add_field(name= 'dislikes', value=response_json['dislikes'], inline= True)
        new_embed.add_field(name= 'views', value=response_json['views'], inline= True)
        new_embed.add_field(name= 'id', value=id, inline= True)
        
        await interaction.response.edit_message(embed=new_embed)
        

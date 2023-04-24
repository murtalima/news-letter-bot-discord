import discord
from .views.news_view import NewsView 

class CommandsService():
    def __init__(self, backend_service):
        self.backend_service = backend_service
    
    async def hello_world(self, interaction):
        await interaction.response.send_message("Hello!")
        
    async def news(self, interaction):
        response = self.backend_service.getNewspaper(interaction.user.id)
        
        if(response.status_code == 200):
            response_json = response.json()
            
            content =response_json['content']
            likes = response_json['likes']
            dislikes = response_json['dislikes']
            views = response_json['views']
            id = response_json['id']
            
            embed_content = discord.Embed(
                        color= discord.Color.blue()
                    )
            
            embed_content.add_field(name= 'likes', value=likes)
            embed_content.add_field(name= 'dislikes', value=dislikes, inline= True)
            embed_content.add_field(name= 'views', value=views, inline= True)
            embed_content.add_field(name= 'id', value=id, inline= True)
            
            await interaction.response.send_message(content=content,embed=embed_content, view=NewsView())
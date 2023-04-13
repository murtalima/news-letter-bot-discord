import discord


class MyView(discord.ui.View):
    @discord.ui.button(label="Like", row=0, style=discord.ButtonStyle.green)
    async def first_button_callback(self, interaction, button):
        file = discord.File("../like10.png", filename="like.png")
        embed = interaction.message.embeds[0]
        new_embed = discord.Embed(color= discord.Color.green(), description= embed.description)
        new_embed.set_image(url='attachment://like.png')
        await interaction.response.edit_message(view=None, embed=new_embed, attachments=[file])

    @discord.ui.button(label="Dislike", row=0, style=discord.ButtonStyle.red)
    async def second_button_callback(self, interaction, button):
        file = discord.File("../dislike10.png", filename="dislike.png")
        embed = interaction.message.embeds[0]
        new_embed = discord.Embed(color= discord.Color.red(), description= embed.description)
        new_embed.set_image(url='attachment://dislike.png')
        await interaction.response.edit_message(view=None, embed=new_embed, attachments=[file])

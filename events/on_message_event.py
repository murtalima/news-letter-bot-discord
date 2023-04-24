import asyncio
import time

class OnMessageEvent():
    def __init__(self, backend_service):
        self.backend_service = backend_service
        
    async def exec(self, message):
        response = self.backend_service.findUser(message.author.id)

        if response.status_code == 200:
            user = response.json()
            
            if not any(str(message.guild.id) in guild['discordId'] for guild in user['guilds']):
                self.backend_service.addGuildUsers(message.author.id, message.guild.id)
                
            is_user_adm = user['isAdm']
            
            if is_user_adm:
                if message.content.startswith('$roda roda'):
                    await asyncio.gather(self.make_members_roll(message))

                if message.content.startswith('$nao fala comigo'):
                    for member in message.mentions:
                            response = self.backend_service.findUser(member.id)
                            if(response.status_code == 200):
                                target = response.json()
                                self.backend_service.updateUser(member.id, member.name, target['isAdm'], True)
                            else:
                                target = self.backend_service.createUser(member.id, member.name, False, True)

                            try:
                                await member.edit(mute=True, deafen=True)
                            except:
                                pass
                        

                if message.content.startswith('$fala comigo'):
                    for member in message.mentions:
                            if(response.status_code == 200):
                                target = response.json()
                                self.backend_service.updateUser(member.id, member.name, target['isAdm'], False)
                            else:
                                target = self.backend_service.createUser(member.id, member.name, False, False)
                            
                            try:
                                await member.edit(mute=False, deafen=False)
                            except:
                                pass

                if message.content.startswith('$add'):
                    for member in message.mentions:
                        response = self.backend_service.findUser(member.id)
                        
                        if response.status_code == 200:
                            target = response.json()
                            if target['isAdm']:
                                await message.channel.send(member.name + ' ja é Adm')

                            update_response = self.backend_service.updateUser(member.id, member.name, True, False)

                            if update_response.status_code != 200:
                                await message.channel.send(member.name + ' erro ao transformar em adm')

                        elif response.status_code == 404:
                            self.backend_service.createUser(member.id, member.name, True, False, message.guild.id)

                if message.content.startswith('$remove'):
                    for member in message.mentions:
                        response = self.backend_service.findUser(member.id)
                        
                        if response.status_code == 200:
                            target = response.json()

                            if target['isAdm'] == False:
                                await message.channel.send(member.name + ' não tem poderes de adm')

                            update_response = self.backend_service.updateUser(member.id, member.name, False, False)

                            if update_response.status_code != 200:
                                await message.channel.send(member.name + ' erro ao transformar em adm')

                        elif response.status_code == 404:
                            self.backend_service.createUser(member.id, member.name, False, False)

                
        print(message.author.id, message.author.name, ' -> ', message.content)
        
    async def make_members_roll(self, message):
        for member in message.mentions:
            await self.roller(member=member, guild=message.guild)


    async def roller(self, member, guild):
        for channel in guild.voice_channels:
            await member.move_to(channel=channel)
            time.sleep(0.4)

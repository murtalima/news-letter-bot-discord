class OnVoiceStateUpdateEvent():
    def __init__(self, backend_service):
        self.backend_service = backend_service
        
    async def exec(self, member, before, after):
        response = self.backend_service.findUser(member.id)

        if response.status_code == 200:
            response_json = response.json()

            if not any(str(member.guild.id) in guild['discordId'] for guild in response_json['guilds']):
                self.backend_service.addGuildUsers(member.id, member.guild.id)

            user = response.json()

            if user['isMuted'] and (not after.mute or not after.deaf):
                await member.edit(mute=True, deafen=True)

            if user['isAdm'] and (after.mute or after.deaf):
                await member.edit(mute=False, deafen=False)
                
        if response.status_code == 404:
            self.backend_service.createUser(member.id, member.name, False, False, member.guild.id)
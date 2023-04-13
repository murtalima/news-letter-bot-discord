import requests as req

class BackendProvider:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip
        self.url = 'http://' + self.ip + ':' + str(self.port)+ '/'
        self.endpoints = {
            'users': self.url + 'users/',
            'guilds': self.url + 'guilds/',
            'newspapers': self.url + 'newspapers'
        }

    def createUser(self, discord_id, name, is_adm, is_muted, guild_id):
        body = {
            "discordId": str(discord_id),
            "name" : name,
            "isAdm": is_adm,
            "isMuted": is_muted,
            "guildId": str(guild_id)
        }
        return req.post(url=self.endpoints['users'], json=body)

    def deleteUser(self, discord_id):
        return req.delete(self.endpoints['users'] + str(discord_id))

    def findUser(self, discord_id):
        return req.get(url=self.endpoints['users'] + str(discord_id))

    def updateUser(self, discord_id, name, is_adm, is_muted):
        body = {
            "discordId": str(discord_id),
            "name": name,
            "isAdm": is_adm,
            "isMuted": is_muted,
        }

        return req.put(url=self.endpoints['users'] + str(discord_id) , json=body )

    def createGuild(self, discord_id, name, members_count):
        body = {
            "discordId": str(discord_id),
            "name": name,
            "membersCount": members_count
        }
        return req.post(url=self.endpoints['guilds'], json=body)

    def deleteGuild(self, discord_id):
        return req.delete(self.endpoints['guilds'] + str(discord_id))

    def findGuild(self, discord_id):
        return req.get(url=self.endpoints['guilds'] + str(discord_id))

    def updateGuild(self, discord_id, name, members_count):
        body = {
            "discordId": str(discord_id),
            "name": name,
            "membersCount": members_count
        }

        return req.put(url=self.endpoints['guilds'] + str(discord_id), json=body)
    
    def getNewspaper(self, discord_id):
        return req.get(url=self.endpoints['newspapers'] + '/user/' + str(discord_id))

    def addGuildUsers(self, user_id, guild_id):
        return req.post(url=self.endpoints['users']+ str(user_id) + '/guild' , json= {  "guildId": str(guild_id)})
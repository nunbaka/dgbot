        # recebe o prefixo da guild em questão
        prefix = self.getPrefix(message.guild)
        # instancia um club a partir da guild
        club = self.getClub(message.guild)
        # instancia um objeto contendo as informações do contexto
        context = Context(self, prefix, message)
        # por fim roda o contexto no club criado
        await club.run(context)

    def getClub(self, guild: discord.Guild) -> Club:
        # FUNÇÃO PARA INSTANCIAR UM CLUB
        # cria a chave do club através da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.clubs):
            # se a se esta chave não foi instanciada, faça
            strings = self.getLanguage(guild)
            # instanciando passando a chave e a linguagem
            self.clubs[cKey] = Club(cKey, guild, strings)
        return self.clubs[cKey]

    def getPrefix(self, guild: discord.Guild):
        # DATABASE DOS PREFIXOS
        # cria a chave da guild
        cKey = str(guild.id)
        if not existKey(cKey, self.prefixes):
            # se o prefixo não existir
            return '/'
        else:
            # se existir prefixo, retorne-o
            return self.prefixes[cKey]

    def getLanguage(self, guild: discord.Guild):
        # DATABASE DAS LINGUAGENS
        # cria a chave da guild
        languages = {
            "portuguese": self.language.portuguese
        }
        cKey = str(guild.id)
        if not existKey(cKey, self.languages):
            # se o prefixo não existir
            return languages['portuguese']
        else:
            # se existir prefixo, retorne-o
            return languages[self.languages[cKey]]


client = Client()

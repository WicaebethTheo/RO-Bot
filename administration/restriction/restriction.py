import discord
from redbot.core import commands, checks, Config
import re

class Restriction(commands.Cog):
    """<a:uncheck_ravena:1380884331534483629> Système de restriction des invitations Discord"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild = {
            "enabled": True,  # État de la restriction
            "monitored_channels": [
                # Catégorie Radiant Order
                1380647428465627146,  # Membres
                1380647292796665966,  # Boosts
                
                # Catégorie Bienvenue
                1380560522977742909,  # bienvenue
                1380560525871550502,  # règlement
                1380560529810002073,  # auto-rôles
                1380560533102530560,  # support
                1380560536546316348,  # recrutements
                1380560540258271323,  # nous-soutenir
                
                # Catégorie Informations
                1380560545714798674,  # annonces
                1380560549187686551,  # giveaways
                1380560556389568682,  # soutiens
                1380560559614857380,  # sondages
                
                # Catégorie Communauté
                1380582808673718372,  # Inactifs
                1380582889514729615,  # Crée ton salon
                1380617279804411925,  # discussion
                1380617121213579295,  # médias
                1380560565419638964,  # clip-pp
                1380560568628412447,  # ranked
                1380560571874934896,  # suggestions
                1380560575121326181,  # commandes
                1380560578216722573,  # vos-réseaux
                
                # Catégorie PARTIES PERSO
                1380653561234456707,  # -----------------
                1380560625654304829,  # Préparation 1
                1380560629315670139,  # Attaque
                1380560633107578951,  # Défense
                1380615405789515816,  # -----------------
                1380615433303883999,  # Préparation 2
                1380615452757065738,  # Attaque
                1380615475351916672,  # Défense
                1380615579496611941,  # -----------------
                1380615512161255425,  # Préparation 3
                1380615529412427806,  # Attaque
                1380615563683823738,  # Défense
                1380615493433688226,  # -----------------
                1380617021359915190,  # Préparation 4
                1380617038606762046,  # Attaque
                1380560601004118036,  # parties-perso
                1380617055119740979,  # Défense
                1380560604376596500,  # règlement-pp
                1380560607383912511,  # roulette-maps
                1380560611028635700,  # party-code
                1380560617676603402   # demande-organisateur-pp
            ],  # Canaux surveillés
            "whitelist_roles": []  # Rôles exemptés
        }
        self.config.register_guild(**default_guild)

        # Regex pour détecter les liens d'invitation Discord
        self.invite_regex = re.compile(r"(?:https?://)?(?:www\.)?(?:discord\.(?:gg|io|me|li)|discordapp\.com/invite)/[a-zA-Z0-9]+")

    @commands.group()
    @checks.admin_or_permissions(administrator=True)
    async def antiinvite(self, ctx):
        """<a:boost:1380882468621520916> Commandes de gestion des restrictions d'invitations"""
        if ctx.invoked_subcommand is None:
            await self.show_status(ctx)

    async def show_status(self, ctx):
        """Affiche l'état actuel des restrictions"""
        settings = await self.config.guild(ctx.guild).all()
        
        embed = discord.Embed(
            title="<a:uncheck_ravena:1380884331534483629> Système Anti-Invitations",
            color=discord.Color.blue()
        )
        
        status = "<a:check_ravena:1380884332708626493> Activé" if settings["enabled"] else "<a:uncheck_ravena:1380884331534483629> Désactivé"
        embed.add_field(name="<a:speechbubble:1380892653847314534> État", value=status, inline=False)
        
        # Nombre de canaux surveillés
        monitored_channels = settings["monitored_channels"]
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canaux Surveillés", 
            value=f"{len(monitored_channels)} canaux configurés", 
            inline=False
        )
        
        # Liste des rôles exemptés
        whitelist_roles = settings["whitelist_roles"]
        roles_text = "Aucun" if not whitelist_roles else ", ".join([f"<@&{r}>" for r in whitelist_roles])
        embed.add_field(name="<a:whitecrown:1380899677297315880> Rôles Exemptés", value=roles_text, inline=False)
        
        embed.add_field(
            name="<a:Animated_Arrow_Blue:1380888378953961472> Fonctionnement",
            value="Les restrictions s'appliquent **uniquement** dans les canaux configurés.\n"
                  "Les autres canaux ne sont pas surveillés.",
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Système Anti-Invitations")
        
        await ctx.send(embed=embed)

    @antiinvite.command()
    async def toggle(self, ctx):
        """<a:boost:1380882468621520916> Active/Désactive la restriction des invitations"""
        current = await self.config.guild(ctx.guild).enabled()
        await self.config.guild(ctx.guild).enabled.set(not current)
        
        if not current:
            status_emoji = "<a:check_ravena:1380884332708626493>"
            status_text = "activée"
        else:
            status_emoji = "<a:uncheck_ravena:1380884331534483629>"
            status_text = "désactivée"
            
        await ctx.send(f"{status_emoji} La restriction des invitations est maintenant **{status_text}**.")

    @antiinvite.command()
    async def addchannel(self, ctx, channel: discord.TextChannel):
        """<a:boost:1380882468621520916> Ajoute un canal à la surveillance"""
        async with self.config.guild(ctx.guild).monitored_channels() as monitored:
            if channel.id in monitored:
                await ctx.send(f"<a:Warning:1380884984595742790> Ce canal est déjà surveillé.")
                return
            monitored.append(channel.id)
        await ctx.send(f"<a:check_ravena:1380884332708626493> Le canal {channel.mention} est maintenant surveillé.")

    @antiinvite.command()
    async def removechannel(self, ctx, channel: discord.TextChannel):
        """<a:uncheck_ravena:1380884331534483629> Retire un canal de la surveillance"""
        async with self.config.guild(ctx.guild).monitored_channels() as monitored:
            if channel.id not in monitored:
                await ctx.send(f"<a:Warning:1380884984595742790> Ce canal n'est pas surveillé.")
                return
            monitored.remove(channel.id)
        await ctx.send(f"<a:check_ravena:1380884332708626493> Le canal {channel.mention} n'est plus surveillé.")

    @antiinvite.command()
    async def listchannels(self, ctx):
        """<a:speechbubble:1380892653847314534> Affiche la liste des canaux surveillés"""
        monitored_channels = await self.config.guild(ctx.guild).monitored_channels()
        
        if not monitored_channels:
            await ctx.send("<a:Warning:1380884984595742790> Aucun canal n'est surveillé.")
            return
        
        # Diviser en chunks pour éviter les messages trop longs
        chunks = [monitored_channels[i:i+20] for i in range(0, len(monitored_channels), 20)]
        
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"<a:speechbubble:1380892653847314534> Canaux Surveillés {i+1}/{len(chunks)}",
                color=discord.Color.blue()
            )
            
            channels_text = ""
            for channel_id in chunk:
                channel = ctx.guild.get_channel(channel_id)
                if channel:
                    channels_text += f"• {channel.mention}\n"
                else:
                    channels_text += f"• Canal supprimé (ID: {channel_id})\n"
            
            embed.description = channels_text
            embed.set_footer(text=f"Total: {len(monitored_channels)} canaux")
            
            await ctx.send(embed=embed)

    @antiinvite.command()
    async def addrole(self, ctx, role: discord.Role):
        """<a:whitecrown:1380899677297315880> Ajoute un rôle à la liste d'exemption"""
        async with self.config.guild(ctx.guild).whitelist_roles() as whitelist:
            if role.id in whitelist:
                await ctx.send(f"<a:Warning:1380884984595742790> Ce rôle est déjà exempté.")
                return
            whitelist.append(role.id)
        await ctx.send(f"<a:check_ravena:1380884332708626493> Le rôle {role.mention} est maintenant exempté des restrictions.")

    @antiinvite.command()
    async def removerole(self, ctx, role: discord.Role):
        """<a:uncheck_ravena:1380884331534483629> Retire un rôle de la liste d'exemption"""
        async with self.config.guild(ctx.guild).whitelist_roles() as whitelist:
            if role.id not in whitelist:
                await ctx.send(f"<a:Warning:1380884984595742790> Ce rôle n'est pas exempté.")
                return
            whitelist.remove(role.id)
        await ctx.send(f"<a:check_ravena:1380884332708626493> Le rôle {role.mention} n'est plus exempté des restrictions.")

    @antiinvite.command()
    async def reset(self, ctx):
        """<a:Warning:1380884984595742790> Remet les canaux surveillés par défaut"""
        # Confirmation
        confirm_embed = discord.Embed(
            title="<a:Warning:1380884984595742790> Confirmation requise",
            description="Êtes-vous sûr de vouloir remettre la liste des canaux surveillés par défaut ?\n"
                       "Cette action écrasera la configuration actuelle.",
            color=0xFFA500
        )
        
        confirm_message = await ctx.send(embed=confirm_embed)
        await confirm_message.add_reaction("✅")
        await confirm_message.add_reaction("❌")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirm_message.id
        
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            
            if str(reaction.emoji) == "✅":
                # Remettre les canaux par défaut
                default_channels = [
                    # Catégorie Radiant Order
                    1380647428465627146, 1380647292796665966,
                    # Catégorie Bienvenue
                    1380560522977742909, 1380560525871550502, 1380560529810002073,
                    1380560533102530560, 1380560536546316348, 1380560540258271323,
                    # Catégorie Informations
                    1380560545714798674, 1380560549187686551, 1380560556389568682, 1380560559614857380,
                    # Catégorie Communauté
                    1380582808673718372, 1380582889514729615, 1380617279804411925, 1380617121213579295,
                    1380560565419638964, 1380560568628412447, 1380560571874934896, 1380560575121326181,
                    1380560578216722573,
                    # Catégorie PARTIES PERSO
                    1380653561234456707, 1380560625654304829, 1380560629315670139, 1380560633107578951,
                    1380615405789515816, 1380615433303883999, 1380615452757065738, 1380615475351916672,
                    1380615579496611941, 1380615512161255425, 1380615529412427806, 1380615563683823738,
                    1380615493433688226, 1380617021359915190, 1380617038606762046, 1380560601004118036,
                    1380617055119740979, 1380560604376596500, 1380560607383912511, 1380560611028635700,
                    1380560617676603402
                ]
                
                await self.config.guild(ctx.guild).monitored_channels.set(default_channels)
                
                success_embed = discord.Embed(
                    title="<a:check_ravena:1380884332708626493> Configuration restaurée !",
                    description=f"**{len(default_channels)}** canaux ont été configurés pour la surveillance.",
                    color=0x00FF00
                )
                await confirm_message.edit(embed=success_embed)
            else:
                cancel_embed = discord.Embed(
                    title="<a:uncheck_ravena:1380884331534483629> Annulé",
                    description="La remise à zéro a été annulée.",
                    color=0xFF0000
                )
                await confirm_message.edit(embed=cancel_embed)
                
        except discord.errors.TimeoutError:
            timeout_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Temps écoulé",
                description="La confirmation a expiré. Remise à zéro annulée.",
                color=0xFFA500
            )
            await confirm_message.edit(embed=timeout_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorer les messages des bots
        if message.author.bot:
            return

        # Vérifier si c'est dans un serveur
        if not message.guild:
            return

        # Vérifier si la restriction est activée
        if not await self.config.guild(message.guild).enabled():
            return

        # Vérifier si l'utilisateur est administrateur
        if message.author.guild_permissions.administrator:
            return

        # Vérifier si le canal est dans la liste des canaux surveillés
        monitored_channels = await self.config.guild(message.guild).monitored_channels()
        if message.channel.id not in monitored_channels:
            return  # Ne pas surveiller ce canal

        # Vérifier si l'utilisateur a un rôle exempté
        whitelist_roles = await self.config.guild(message.guild).whitelist_roles()
        if any(role.id in whitelist_roles for role in message.author.roles):
            return

        # Vérifier si le message contient un lien d'invitation
        if self.invite_regex.search(message.content):
            try:
                await message.delete()
                warning_message = await message.channel.send(
                    f"<a:Warning:1380884984595742790> {message.author.mention}, les liens d'invitation Discord ne sont pas autorisés dans ce salon.",
                    delete_after=10
                )
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(Restriction(bot))

import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import random
import datetime

class Welcome(commands.Cog):
    """<a:FallingPetals:1380882470060425267> Système de bienvenue Radiant Order avec rotation de GIFs"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        
        default_guild = {
            "enabled": True,
            "welcome_channel": 1380560522977742909,
            "rules_channel": 1380560525871550502,
            "autoroles_channel": 1380560529810002073,
            "gif_urls": [
                "https://cdn.pixabay.com/animation/2023/01/30/00/43/00-43-04-563_512.gif",
                "https://i.redd.it/xj1v6ehscnt61.gif",
                "https://mir-s3-cdn-cf.behance.net/project_modules/source/68921b29340193.55eea8837b0d9.gif",
                "https://giffiles.alphacoders.com/214/214384.gif"
            ]
        }
        
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Événement déclenché quand un membre rejoint le serveur"""
        if await self.bot.cog_disabled_in_guild(self, member.guild):
            return
        
        guild_config = self.config.guild(member.guild)
        
        if not await guild_config.enabled():
            return
        
        # Récupérer la configuration
        welcome_channel_id = await guild_config.welcome_channel()
        rules_channel_id = await guild_config.rules_channel()
        autoroles_channel_id = await guild_config.autoroles_channel()
        gif_urls = await guild_config.gif_urls()
        
        # Récupérer le canal de bienvenue
        welcome_channel = member.guild.get_channel(welcome_channel_id)
        if not welcome_channel:
            return
        
        # Choisir un GIF aléatoirement
        random_gif = random.choice(gif_urls)
        
        # Créer l'embed de bienvenue pour le canal
        welcome_embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Nouveau membre !",
            description=f"<a:boost:1380882468621520916> Bienvenue sur Radiant Order !\n\n"
                       f"Hey {member.mention}, bienvenue parmi nous !\n"
                       f"Nous sommes ravis de t'accueillir dans notre communauté gaming.",
            color=0xFF6B6B,  # Couleur rouge-orange comme l'exemple
            timestamp=datetime.datetime.now()
        )
        
        # Informations sur le membre
        account_age = (datetime.datetime.now() - member.created_at.replace(tzinfo=None)).days
        join_date = member.joined_at.strftime("%A, %B %d, %Y %I:%M %p") if member.joined_at else "Inconnue"
        
        welcome_embed.add_field(
            name="<a:speechbubble:1380892653847314534> À propos de toi",
            value=f"• Pseudo: **{member.name}**\n"
                  f"• Membre n°**{member.guild.member_count}**\n"
                  f"• Rejoint le: **{join_date}**\n"
                  f"• Compte créé: **{account_age} jours**",
            inline=False
        )
        
        welcome_embed.add_field(
            name="<a:Animated_Arrow_Blue:1380888378953961472> Pour commencer",
            value=f"• Lis le <a:speechbubble:1380892653847314534> <#{rules_channel_id}> pour connaître nos règles\n"
                  f"• Choisis tes rôles dans <a:boost:1380882468621520916> <#{autoroles_channel_id}>",
            inline=False
        )
        
        welcome_embed.set_image(url=random_gif)
        welcome_embed.set_thumbnail(url=member.display_avatar.url)
        welcome_embed.set_footer(
            text=f"Radiant Order • {datetime.datetime.now().strftime('%m/%d/%Y')}", 
            icon_url=member.guild.icon.url if member.guild.icon else None
        )
        
        # Envoyer le message de bienvenue dans le canal
        try:
            await welcome_channel.send(embed=welcome_embed)
        except discord.Forbidden:
            pass  # Pas de permissions pour envoyer dans le canal

    @commands.group(name="welcome")
    @checks.admin_or_permissions(manage_guild=True)
    async def welcome_settings(self, ctx):
        """<a:boost:1380882468621520916> Gestion du système de bienvenue"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @welcome_settings.command(name="toggle")
    async def toggle_welcome(self, ctx, enabled: bool = None):
        """<a:check_ravena:1380884332708626493> Activer/désactiver le système de bienvenue"""
        if enabled is None:
            current = await self.config.guild(ctx.guild).enabled()
            enabled = not current
        
        await self.config.guild(ctx.guild).enabled.set(enabled)
        
        status = "activé" if enabled else "désactivé"
        status_emoji = "<a:check_ravena:1380884332708626493>" if enabled else "<a:uncheck_ravena:1380884331534483629>"
        embed = discord.Embed(
            title="<a:boost:1380882468621520916> Configuration Welcome",
            description=f"{status_emoji} Le système de bienvenue est maintenant **{status}**.",
            color=discord.Color.green() if enabled else discord.Color.red()
        )
        await ctx.send(embed=embed)

    @welcome_settings.command(name="channel")
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal de bienvenue"""
        await self.config.guild(ctx.guild).welcome_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal configuré",
            description=f"Le canal de bienvenue est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @welcome_settings.command(name="rules")
    async def set_rules_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal des règles"""
        await self.config.guild(ctx.guild).rules_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal des règles configuré",
            description=f"Le canal des règles est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @welcome_settings.command(name="autoroles")
    async def set_autoroles_channel(self, ctx, channel: discord.TextChannel):
        """<a:boost:1380882468621520916> Définir le canal des auto-rôles"""
        await self.config.guild(ctx.guild).autoroles_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal des auto-rôles configuré",
            description=f"Le canal des auto-rôles est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @welcome_settings.command(name="addgif")
    async def add_gif(self, ctx, url: str):
        """<a:FallingPetals:1380882470060425267> Ajouter un GIF à la rotation"""
        async with self.config.guild(ctx.guild).gif_urls() as gif_list:
            if url not in gif_list:
                gif_list.append(url)
                embed = discord.Embed(
                    title="<a:check_ravena:1380884332708626493> GIF ajouté",
                    description=f"Le GIF a été ajouté à la rotation.\nTotal : {len(gif_list)} GIFs",
                    color=discord.Color.green()
                )
                embed.set_image(url=url)
            else:
                embed = discord.Embed(
                    title="<a:Warning:1380884984595742790> GIF déjà présent",
                    description="Ce GIF est déjà dans la liste de rotation.",
                    color=discord.Color.orange()
                )
        
        await ctx.send(embed=embed)

    @welcome_settings.command(name="removegif")
    async def remove_gif(self, ctx, gif_number: int):
        """<a:uncheck_ravena:1380884331534483629> Retirer un GIF de la rotation (numéro du GIF)"""
        async with self.config.guild(ctx.guild).gif_urls() as gif_list:
            if 1 <= gif_number <= len(gif_list):
                removed_gif = gif_list.pop(gif_number - 1)
                embed = discord.Embed(
                    title="<a:check_ravena:1380884332708626493> GIF retiré",
                    description=f"Le GIF #{gif_number} a été retiré de la rotation.\nTotal : {len(gif_list)} GIFs",
                    color=discord.Color.green()
                )
                embed.set_image(url=removed_gif)
            else:
                embed = discord.Embed(
                    title="<a:uncheck_ravena:1380884331534483629> Numéro invalide",
                    description=f"Choisissez un numéro entre 1 et {len(gif_list)}.",
                    color=discord.Color.red()
                )
        
        await ctx.send(embed=embed)

    @welcome_settings.command(name="listgifs")
    async def list_gifs(self, ctx):
        """<a:speechbubble:1380892653847314534> Afficher tous les GIFs de la rotation"""
        gif_urls = await self.config.guild(ctx.guild).gif_urls()
        
        if not gif_urls:
            embed = discord.Embed(
                title="<a:speechbubble:1380892653847314534> Liste des GIFs",
                description="Aucun GIF configuré.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)
        
        description = ""
        for i, gif_url in enumerate(gif_urls, 1):
            description += f"**{i}.** {gif_url}\n"
        
        embed = discord.Embed(
            title="<a:speechbubble:1380892653847314534> Liste des GIFs de rotation",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Total : {len(gif_urls)} GIFs")
        
        await ctx.send(embed=embed)

    @welcome_settings.command(name="test")
    async def test_welcome(self, ctx, member: discord.Member = None):
        """<a:PinkLoading:1380886781062414356> Tester le système de bienvenue"""
        test_member = member or ctx.author
        
        # Simuler l'événement on_member_join
        await self.on_member_join(test_member)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Test effectué",
            description=f"Le système de bienvenue a été testé pour {test_member.mention}.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        guild_config = self.config.guild(ctx.guild)
        
        enabled = await guild_config.enabled()
        welcome_channel_id = await guild_config.welcome_channel()
        rules_channel_id = await guild_config.rules_channel()
        autoroles_channel_id = await guild_config.autoroles_channel()
        gif_count = len(await guild_config.gif_urls())
        
        welcome_channel = ctx.guild.get_channel(welcome_channel_id)
        rules_channel = ctx.guild.get_channel(rules_channel_id)
        autoroles_channel = ctx.guild.get_channel(autoroles_channel_id)
        
        embed = discord.Embed(
            title="<a:boost:1380882468621520916> Configuration Welcome Radiant Order",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        status_emoji = "<a:check_ravena:1380884332708626493>" if enabled else "<a:uncheck_ravena:1380884331534483629>"
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Statut",
            value=f"{status_emoji} {'Activé' if enabled else 'Désactivé'}",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal de bienvenue",
            value=welcome_channel.mention if welcome_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal des règles",
            value=rules_channel.mention if rules_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:boost:1380882468621520916> Canal auto-rôles",
            value=autoroles_channel.mention if autoroles_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:FallingPetals:1380882470060425267> GIFs configurés",
            value=f"{gif_count} GIFs",
            inline=True
        )
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Commandes disponibles",
            value="`!welcome toggle` - Activer/désactiver\n"
                  "`!welcome test` - Tester le système\n"
                  "`!welcome listgifs` - Voir les GIFs",
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Système de bienvenue")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))

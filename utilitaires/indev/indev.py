import discord
from redbot.core import commands, checks
from redbot.core.bot import Red
import datetime
import asyncio

class InDev(commands.Cog):
    """<a:PinkLoading:1380886781062414356> Système de message de développement en cours"""

    def __init__(self, bot: Red):
        self.bot = bot

    def has_required_role():
        async def predicate(ctx):
            # ID de Wicaebeth
            wicaebeth_id = 257152912776495104
            # Si c'est Wicaebeth, autoriser
            if ctx.author.id == wicaebeth_id:
                return True
            
            # Liste des IDs des rôles autorisés
            authorized_role_ids = [
                1380562058461839400,  # Administrateur
                1380562966575059116,  # Responsables
                1380575934410915911,  # Assistants Responsable
                1380563626846322819,  # Modérateurs
                1380564333242613821,  # Helper
                1380574085708513340,  # Staff Interne
                1380574650689388695,  # Développeur
                1380573287834456184,   # Ressources Humaines
                1380637614696042617
            ]
            
            # Vérifier si l'utilisateur a l'un des rôles autorisés
            for role_id in authorized_role_ids:
                role = ctx.guild.get_role(role_id)
                if role and role in ctx.author.roles:
                    return True
                    
            raise commands.CheckFailure("Tu n'as pas les rôles requis pour utiliser cette commande.")
            return False
        return commands.check(predicate)

    @commands.command(name="indev")
    @has_required_role()
    async def indev(self, ctx):
        """<a:PinkLoading:1380886781062414356> Affiche un message indiquant que le salon est en développement"""
        
        # Supprimer la commande de l'utilisateur
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

        # Récupérer les informations de l'auteur et du serveur
        author_name = ctx.author.display_name
        author_avatar = ctx.author.display_avatar.url
        guild_icon = ctx.guild.icon.url if ctx.guild.icon else None
        channel_name = ctx.channel.name

        # Créer l'embed informatif
        embed = discord.Embed(
            title="<a:PinkLoading:1380886781062414356> Salon en Développement",
            description=(
                f"**Ce salon est actuellement en cours de développement !** <a:boost:1380882468621520916>\n\n"
                f"<a:FallingPetals:1380882470060425267> **Statut actuel :**\n"
                f"• <a:PinkLoading:1380886781062414356> Fonctionnalités en cours d'implémentation\n"
                f"• <a:speechbubble:1380892653847314534> Interface en cours de conception\n"
                f"• <a:boost:1380882468621520916> Optimisations et tests en cours\n\n"
                f"<a:Lightblueheartgif:1380882450439471165> **Vous avez une idée pour ce salon ?**\n"
                f"<a:Animated_Arrow_Blue:1380888378953961472> N'hésitez pas à contacter le staff !\n\n"
                f"<a:whitecrown:1380899677297315880> **Comment nous contacter :**\n"
                f"• Message privé à un membre du staff\n"
                f"• Création d'un ticket\n"
                f"• Mention dans les salons appropriés\n\n"
                f"<a:agooglebell:1380895257541083300> **Vos suggestions sont importantes pour améliorer Radiant Order !**"
            ),
            color=0x9B59B6,
            timestamp=datetime.datetime.now()
        )

        # Ajouter des champs informatifs
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Types de suggestions acceptées",
            value=(
                "• Fonctionnalités à ajouter\n"
                "• Améliorations d'interface\n"
                "• Idées créatives\n"
                "• Optimisations\n"
                "• Intégrations avec d'autres systèmes"
            ),
            inline=True
        )

        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Staff à contacter",
            value=(
                "• Administrateurs\n"
                "• Responsables\n"
                "• Développeurs\n"
                "• Modérateurs\n"
                "• Équipe technique"
            ),
            inline=True
        )

        # Ajouter le footer avec l'auteur
        embed.set_footer(text=f"Message affiché par {author_name} • Radiant Order", icon_url=author_avatar)
        
        # Ajouter l'icône du serveur comme thumbnail si disponible
        if guild_icon:
            embed.set_thumbnail(url=guild_icon)

        # Envoyer le message
        await ctx.send(embed=embed)

    @indev.error
    async def indev_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            error_msg = await ctx.send("<a:uncheck_ravena:1380884331534483629> Tu n'as pas les rôles requis pour utiliser cette commande.")
            await asyncio.sleep(5)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

async def setup(bot):
    await bot.add_cog(InDev(bot))

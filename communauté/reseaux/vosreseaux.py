import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime

class VosReseaux(commands.Cog):
    """<a:speechbubble:1380892653847314534> Gestion du canal vos réseaux"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=789456123)
        
        default_guild = {
            "reseaux_channel": None,
            "actif_role": None
        }
        
        self.config.register_guild(**default_guild)

    @commands.group(name="vosreseaux")
    @checks.admin_or_permissions(manage_guild=True)
    async def vosreseaux_settings(self, ctx):
        """<a:speechbubble:1380892653847314534> Gestion du système vos réseaux"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @vosreseaux_settings.command(name="setup")
    async def setup_vosreseaux(self, ctx):
        """<a:FallingPetals:1380882470060425267> Configurer le message du canal vos réseaux"""
        reseaux_channel_id = await self.config.guild(ctx.guild).reseaux_channel()
        
        if not reseaux_channel_id:
            return await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Le canal vos réseaux n'est pas configuré. Utilisez `!vosreseaux channel #canal`"
            )
        
        reseaux_channel = ctx.guild.get_channel(reseaux_channel_id)
        
        if not reseaux_channel:
            return await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Le canal configuré n'existe pas."
            )
        
        # Nettoyer le canal avant d'envoyer le nouveau message
        try:
            await reseaux_channel.purge(limit=None)
        except discord.Forbidden:
            await ctx.send(
                "<a:Warning:1380884984595742790> Je n'ai pas les permissions pour nettoyer le canal. Le message sera envoyé sans nettoyage."
            )
        except Exception as e:
            await ctx.send(
                f"<a:uncheck_ravena:1380884331534483629> Erreur lors du nettoyage : {str(e)}"
            )
        
        # Récupérer le rôle actif
        actif_role_id = await self.config.guild(ctx.guild).actif_role()
        actif_role = ctx.guild.get_role(actif_role_id) if actif_role_id else None
        
        # Créer l'embed informatif
        embed = discord.Embed(
            title="<a:speechbubble:1380892653847314534> Vos Réseaux - Conditions de Publication",
            description=(
                f"**Bienvenue dans le canal vos réseaux !** <a:FallingPetals:1380882470060425267>\n\n"
                f"<a:Warning:1380884984595742790> **Conditions pour poster dans ce canal :**\n\n"
                f"<a:check_ravena:1380884332708626493> **Option 1 :** Avoir le rôle {actif_role.mention if actif_role else '**Actif**'}\n"
                f"<a:whitecrown:1380899677297315880> **Option 2 :** Demander une whitelist aux administrateurs/modérateurs\n\n"
                f"<a:agooglebell:1380895257541083300> **Pourquoi ces conditions ?**\n"
                f"• <a:boost:1380882468621520916> Maintenir la qualité du contenu\n"
                f"• <a:Lightblueheartgif:1380882450439471165> Encourager l'activité communautaire\n"
                f"• <a:PinkLoading:1380886781062414356> Éviter le spam et les contenus non pertinents\n\n"
                f"<a:Animated_Arrow_Blue:1380888378953961472> **Comment obtenir l'accès ?**\n"
                f"• **Rôle Actif** : Participez activement à la communauté\n"
                f"• **Whitelist** : Contactez un membre du staff en privé\n\n"
                f"<a:speechbubble:1380892653847314534> **Partagez vos réseaux sociaux, chaînes, projets et créations !**"
            ),
            color=0x3498DB,
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:agooglebell:1380895257541083300> Types de contenus acceptés",
            value=(
                "• Chaînes YouTube/Twitch\n"
                "• Profils Instagram/TikTok\n"
                "• Projets créatifs\n"
                "• Contenu lié au gaming\n"
                "• Créations artistiques"
            ),
            inline=True
        )
        
        embed.add_field(
            name="<a:uncheck_ravena:1380884331534483629> Contenus interdits",
            value=(
                "• Spam répétitif\n"
                "• Contenu NSFW\n"
                "• Publicités non liées\n"
                "• Self-promotion excessive\n"
                "• Liens malveillants"
            ),
            inline=True
        )
        
        embed.set_footer(text="Radiant Order - Partagez vos passions !")
        
        # Envoyer le message
        try:
            await reseaux_channel.send(embed=embed)
            await ctx.send(
                f"<a:check_ravena:1380884332708626493> Le message informatif a été configuré dans {reseaux_channel.mention} !"
            )
        except discord.Forbidden:
            await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Je n'ai pas les permissions pour envoyer dans le canal vos réseaux."
            )

    @vosreseaux_settings.command(name="channel")
    async def set_reseaux_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal vos réseaux"""
        await self.config.guild(ctx.guild).reseaux_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal configuré",
            description=f"Le canal vos réseaux est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @vosreseaux_settings.command(name="role")
    async def set_actif_role(self, ctx, role: discord.Role):
        """<a:boost:1380882468621520916> Définir le rôle actif"""
        await self.config.guild(ctx.guild).actif_role.set(role.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Rôle configuré",
            description=f"Le rôle actif est maintenant {role.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        reseaux_channel_id = await self.config.guild(ctx.guild).reseaux_channel()
        actif_role_id = await self.config.guild(ctx.guild).actif_role()
        
        reseaux_channel = ctx.guild.get_channel(reseaux_channel_id)
        actif_role = ctx.guild.get_role(actif_role_id)
        
        embed = discord.Embed(
            title="<a:speechbubble:1380892653847314534> Configuration Vos Réseaux",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal vos réseaux",
            value=reseaux_channel.mention if reseaux_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:boost:1380882468621520916> Rôle actif",
            value=actif_role.mention if actif_role else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:agooglebell:1380895257541083300> Commandes disponibles",
            value=(
                "`!vosreseaux setup` - Configurer le message\n"
                "`!vosreseaux channel #canal` - Définir le canal\n"
                "`!vosreseaux role @role` - Définir le rôle actif"
            ),
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Gestion vos réseaux")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VosReseaux(bot))

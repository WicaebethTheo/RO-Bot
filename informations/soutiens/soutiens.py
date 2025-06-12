import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
from discord.ui import Button, View

class SoutienContactView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Contacter Wicaebeth",
        style=discord.ButtonStyle.primary,
        emoji="<a:whitecrown:1380899677297315880>",
        custom_id="contact_wica"
    )
    async def contact_wica(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ID de Wicaebeth
        wica_id = 257152912776495104
        wica = interaction.guild.get_member(wica_id)
        
        embed = discord.Embed(
            title="<a:whitecrown:1380899677297315880> Contact Wicaebeth",
            description=(
                f"Pour soutenir **Radiant Order**, vous pouvez contacter directement :\n\n"
                f"<a:whitecrown:1380899677297315880> **Wicaebeth** : {wica.mention if wica else f'<@{wica_id}>'}\n\n"
                f"<a:speechbubble:1380892653847314534> **Moyens de soutien possibles :**\n"
                f"• <a:boost:1380882468621520916> Soutien monétaire\n"
                f"• <a:FallingPetals:1380882470060425267> Services (développement, design, etc.)\n"
                f"• <a:agooglebell:1380895257541083300> Promotion du serveur\n"
                f"• <a:Lightblueheartgif:1380882450439471165> Toute autre forme de contribution\n\n"
                f"<a:Animated_Arrow_Blue:1380888378953961472> N'hésitez pas à envoyer un message privé ou mentionner directement !"
            ),
            color=0x9B59B6,
            timestamp=datetime.datetime.now()
        )
        
        embed.set_footer(text="Radiant Order - Système de soutien")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="Créer un ticket",
        style=discord.ButtonStyle.success,
        emoji="<a:speechbubble:1380892653847314534>",
        custom_id="create_support_ticket"
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Récupérer l'ID du canal tickets depuis la config
        bot = interaction.client
        config = bot.get_cog("Soutiens").config
        tickets_channel_id = await config.guild(interaction.guild).tickets_channel()
        tickets_channel = interaction.guild.get_channel(tickets_channel_id)
        
        embed = discord.Embed(
            title="<a:speechbubble:1380892653847314534> Créer un ticket de soutien",
            description=(
                f"<a:boost:1380882468621520916> **Pour créer un ticket de soutien :**\n\n"
                f"1. <a:Animated_Arrow_Blue:1380888378953961472> Rendez-vous dans {tickets_channel.mention if tickets_channel else 'le canal tickets'}\n"
                f"2. <a:FallingPetals:1380882470060425267> Cliquez sur le bouton approprié pour créer un ticket\n"
                f"3. <a:speechbubble:1380892653847314534> Expliquez comment vous souhaitez soutenir Radiant Order\n\n"
                f"<a:whitecrown:1380899677297315880> **Types de soutien acceptés :**\n"
                f"• Contributions financières\n"
                f"• Services professionnels (dev, design, marketing)\n"
                f"• Partenariats\n"
                f"• Promotion et publicité\n"
                f"• Ressources ou matériel\n"
                f"• Toute autre idée créative !\n\n"
                f"<a:agooglebell:1380895257541083300> L'équipe vous répondra rapidement dans votre ticket privé."
            ),
            color=0x2ECC71,
            timestamp=datetime.datetime.now()
        )
        
        embed.set_footer(text="Radiant Order - Création de ticket")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Soutiens(commands.Cog):
    """<a:boost:1380882468621520916> Système de soutien pour Radiant Order"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=456789123)
        
        default_guild = {
            "soutiens_channel": 1380560556389568682,
            "wica_id": 257152912776495104,
            "tickets_channel": 1380560533102530560
        }
        
        self.config.register_guild(**default_guild)

    async def cog_load(self):
        """Réenregistrer la vue persistante au démarrage"""
        self.bot.add_view(SoutienContactView())

    @commands.group(name="soutiens")
    @checks.admin_or_permissions(manage_guild=True)
    async def soutiens_settings(self, ctx):
        """<a:boost:1380882468621520916> Gestion du système de soutien"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @soutiens_settings.command(name="setup")
    async def setup_soutiens(self, ctx):
        """<a:FallingPetals:1380882470060425267> Configurer le message de soutien"""
        soutiens_channel_id = await self.config.guild(ctx.guild).soutiens_channel()
        soutiens_channel = ctx.guild.get_channel(soutiens_channel_id)
        
        if not soutiens_channel:
            return await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Le canal de soutiens n'est pas configuré ou n'existe pas."
            )
        
        # Nettoyer le canal avant d'envoyer le nouveau message
        try:
            await soutiens_channel.purge(limit=None)
        except discord.Forbidden:
            await ctx.send(
                "<a:Warning:1380884984595742790> Je n'ai pas les permissions pour nettoyer le canal. Le message sera envoyé sans nettoyage."
            )
        except Exception as e:
            await ctx.send(
                f"<a:uncheck_ravena:1380884331534483629> Erreur lors du nettoyage : {str(e)}"
            )
        
        # Récupérer Wicaebeth
        wica_id = await self.config.guild(ctx.guild).wica_id()
        wica = ctx.guild.get_member(wica_id)
        
        # Créer l'embed principal
        embed = discord.Embed(
            title="<a:boost:1380882468621520916> Soutenir Radiant Order",
            description=(
                "**Vous souhaitez aider notre communauté à grandir ?**\n\n"
                f"<a:FallingPetals:1380882470060425267> **Radiant Order** est une communauté en constante évolution, "
                f"et votre soutien peut faire la différence !\n\n"
                f"<a:speechbubble:1380892653847314534> **Pourquoi nous soutenir ?**\n"
                f"• <a:agooglebell:1380895257541083300> Améliorer l'expérience de tous les membres\n"
                f"• <a:boost:1380882468621520916> Développer de nouvelles fonctionnalités\n"
                f"• <a:Animated_Arrow_Blue:1380888378953961472> Organiser plus d'événements\n"
                f"• <a:whitecrown:1380899677297315880> Maintenir un serveur de qualité\n\n"
                f"<a:Lightblueheartgif:1380882450439471165> **Comment nous soutenir ?**\n"
                f"• **Soutien financier** - Donations, abonnements\n"
                f"• **Services** - Développement, design, modération\n"
                f"• **Promotion** - Partage, recommandations\n"
                f"• **Contenu** - Création, streaming, guides\n"
                f"• **Partenariats** - Collaborations, échanges\n"
                f"• **Ressources** - Serveurs, outils, licences\n\n"
                f"<a:PinkLoading:1380886781062414356> **Utilisez les boutons ci-dessous pour nous contacter !**"
            ),
            color=0x9B59B6
        )
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Contact Direct",
            value=f"Contactez {wica.mention if wica else f'<@{wica_id}>'} directement",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Ticket Privé",
            value="Créez un ticket pour discuter en privé",
            inline=True
        )
        
        embed.add_field(
            name="<a:agooglebell:1380895257541083300> Reconnaissance",
            value="Tous les soutiens seront reconnus et appréciés !",
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Merci pour votre soutien !")
        
        # Créer la vue avec les boutons
        view = SoutienContactView()
        
        # Envoyer le message
        try:
            await soutiens_channel.send(embed=embed, view=view)
            await ctx.send(
                f"<a:check_ravena:1380884332708626493> Le système de soutien a été configuré dans {soutiens_channel.mention} !"
            )
        except discord.Forbidden:
            await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Je n'ai pas les permissions pour envoyer dans le canal de soutiens."
            )

    @soutiens_settings.command(name="channel")
    async def set_soutiens_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal de soutiens"""
        await self.config.guild(ctx.guild).soutiens_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal configuré",
            description=f"Le canal de soutiens est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @soutiens_settings.command(name="setwica")
    async def set_wica_id(self, ctx, user: discord.Member):
        """<a:whitecrown:1380899677297315880> Définir l'utilisateur contact (Wicaebeth)"""
        await self.config.guild(ctx.guild).wica_id.set(user.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Contact configuré",
            description=f"L'utilisateur contact est maintenant {user.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @soutiens_settings.command(name="tickets")
    async def set_tickets_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal tickets"""
        await self.config.guild(ctx.guild).tickets_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal tickets configuré",
            description=f"Le canal tickets est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @soutiens_settings.command(name="stats")
    async def soutiens_stats(self, ctx):
        """<a:speechbubble:1380892653847314534> Statistiques des interactions de soutien"""
        # Ici on pourrait ajouter un système de tracking des interactions
        embed = discord.Embed(
            title="<a:speechbubble:1380892653847314534> Statistiques du système de soutien",
            description=(
                "<a:boost:1380882468621520916> **Système actif et fonctionnel**\n\n"
                "Pour des statistiques détaillées, vous pouvez surveiller :\n"
                "• Les messages privés reçus par le contact\n"
                "• Les tickets créés avec le tag 'soutien'\n"
                "• L'activité dans le canal de soutiens"
            ),
            color=0x3498DB,
            timestamp=datetime.datetime.now()
        )
        await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        soutiens_channel_id = await self.config.guild(ctx.guild).soutiens_channel()
        wica_id = await self.config.guild(ctx.guild).wica_id()
        tickets_channel_id = await self.config.guild(ctx.guild).tickets_channel()
        
        soutiens_channel = ctx.guild.get_channel(soutiens_channel_id)
        wica_user = ctx.guild.get_member(wica_id)
        tickets_channel = ctx.guild.get_channel(tickets_channel_id)
        
        embed = discord.Embed(
            title="<a:boost:1380882468621520916> Configuration Système de Soutien",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal de soutiens",
            value=soutiens_channel.mention if soutiens_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal tickets",
            value=tickets_channel.mention if tickets_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Contact principal",
            value=wica_user.mention if wica_user else f"<@{wica_id}>",
            inline=True
        )
        
        embed.add_field(
            name="<a:FallingPetals:1380882470060425267> Fonctionnalités",
            value="• Bouton contact direct\n• Création de tickets\n• Messages informatifs",
            inline=False
        )
        
        embed.add_field(
            name="<a:agooglebell:1380895257541083300> Commandes disponibles",
            value=(
                "`!soutiens setup` - Configurer le message\n"
                "`!soutiens channel <#canal>` - Changer le canal\n"
                "`!soutiens setwica <@user>` - Changer le contact\n"
                "`!soutiens tickets <#canal>` - Changer le canal tickets\n"
                "`!soutiens stats` - Voir les statistiques"
            ),
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Système de soutien")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Soutiens(bot))

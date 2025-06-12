import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
import asyncio

class PPRulesView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="J'accepte les règles PP", style=discord.ButtonStyle.success, emoji="<a:check_ravena:1380884332708626493>", custom_id="pp_rules_accept")
    async def accept_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Récupérer le rôle des règles PP
        rules_role_id = await self.cog.config.guild(interaction.guild).rules_role()
        rules_role = interaction.guild.get_role(rules_role_id)
        
        if not rules_role:
            return await interaction.response.send_message(
                "❌ Rôle des règles PP non configuré.", ephemeral=True
            )
        
        # Vérifier si l'utilisateur a déjà le rôle
        if rules_role in interaction.user.roles:
            embed = discord.Embed(
                title="ℹ️ Déjà validé",
                description="Vous avez déjà accepté les règles des parties personnalisées !",
                color=discord.Color.blue()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Ajouter le rôle
        try:
            await interaction.user.add_roles(rules_role, reason="Acceptation des règles PP")
            
            embed = discord.Embed(
                title="✅ Règles acceptées !",
                description="Vous avez maintenant accès aux parties personnalisées !\n"
                           "Vous pouvez rejoindre les salons dédiés aux PP.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Radiant Order - Parties Personnalisées")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Je n'ai pas les permissions pour vous donner ce rôle.", ephemeral=True
            )

    @discord.ui.button(label="Notifications PP", style=discord.ButtonStyle.primary, custom_id="pp_notifs", emoji="<a:agooglebell:1380895257541083300>")
    async def toggle_notifications(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Récupérer le rôle des notifications PP
        notifs_role_id = await self.cog.config.guild(interaction.guild).notifs_role()
        notifs_role = interaction.guild.get_role(notifs_role_id)
        
        if not notifs_role:
            return await interaction.response.send_message(
                "❌ Rôle des notifications PP non configuré.", ephemeral=True
            )
        
        # Toggle du rôle
        try:
            if notifs_role in interaction.user.roles:
                # Retirer le rôle
                await interaction.user.remove_roles(notifs_role, reason="Désactivation des notifications PP")
                
                embed = discord.Embed(
                    title="🔕 Notifications désactivées",
                    description="Vous ne recevrez plus de notifications pour les parties personnalisées.",
                    color=discord.Color.orange()
                )
            else:
                # Ajouter le rôle
                await interaction.user.add_roles(notifs_role, reason="Activation des notifications PP")
                
                embed = discord.Embed(
                    title="🔔 Notifications activées !",
                    description="Vous recevrez maintenant les notifications des parties personnalisées !",
                    color=discord.Color.blue()
                )
            
            embed.set_footer(text="Radiant Order - Notifications PP")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Je n'ai pas les permissions pour gérer ce rôle.", ephemeral=True
            )

class ReglementPP(commands.Cog):
    """<a:INFINITYBYP:1380887933325676706> Système de règlement des parties personnalisées"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321456)
        
        default_guild = {
            "rules_channel": 1380560604376596500,
            "rules_role": 1380615723692326992,
            "notifs_role": 1380616851427557406
        }
        
        self.config.register_guild(**default_guild)
        
        # Vue persistante
        self.rules_view = PPRulesView(self)

    async def cog_load(self):
        """Ajouter la vue persistante au bot"""
        self.bot.add_view(self.rules_view)

    @commands.group(name="reglementpp")
    @checks.admin_or_permissions(manage_guild=True)
    async def reglement_pp(self, ctx):
        """<a:INFINITYBYP:1380887933325676706> Gestion du règlement des parties personnalisées"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @reglement_pp.command(name="setup")
    async def setup_rules(self, ctx):
        """<a:maruloader:1380888045259329569> Déployer le règlement des parties personnalisées"""
        channel_id = await self.config.guild(ctx.guild).rules_channel()
        channel = ctx.guild.get_channel(channel_id)
        
        if not channel:
            return await ctx.send("❌ Channel du règlement PP non configuré.")
        
        # Message de début
        setup_embed = discord.Embed(
            title="<a:maruloader:1380888045259329569> Déploiement du règlement PP en cours...",
            description="Nettoyage et configuration du salon...",
            color=discord.Color.orange()
        )
        setup_message = await ctx.send(embed=setup_embed)
        
        try:
            # Nettoyer le channel
            setup_embed.description = f"<a:maruloader:1380888045259329569> Nettoyage du salon {channel.mention}..."
            await setup_message.edit(embed=setup_embed)
            
            # Supprimer tous les messages
            try:
                await channel.purge(limit=None, check=lambda m: True)
            except discord.Forbidden:
                # Si on ne peut pas purge, supprimer un par un
                async for message in channel.history(limit=None):
                    try:
                        await message.delete()
                    except:
                        continue
            
            # Message d'introduction
            setup_embed.description = f"<a:maruloader:1380888045259329569> Envoi du règlement dans {channel.mention}..."
            await setup_message.edit(embed=setup_embed)
            
            intro_embed = discord.Embed(
                title="<a:INFINITYBYP:1380887933325676706> Règlement des Parties Personnalisées",
                description="**Bienvenue dans l'univers des PP de Radiant Order !**\n\n"
                           "Les parties personnalisées sont un espace de jeu convivial où tous les niveaux se mélangent.\n"
                           "Respectez ces règles pour que tout le monde passe un bon moment ! <a:PinkLoading:1380886781062414356>",
                color=0x5865F2,  # Couleur Discord bleu
                timestamp=datetime.datetime.now()
            )
            intro_embed.set_thumbnail(url="https://logoeps.com/wp-content/uploads/2021/06/valorant-vector-logo.png")
            intro_embed.set_footer(text="Radiant Order - Parties Personnalisées", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            
            await channel.send(embed=intro_embed)
            
            # En jeu
            ingame_embed = discord.Embed(
                title="<a:PinkLoading:1380886781062414356> Règles en Jeu",
                color=0xED4245  # Couleur rouge pour les règles strictes
            )
            
            ingame_embed.add_field(
                name="<a:WhiteBalisong:1380892882516443287> Limites d'Armes (par équipe)",
                value="• **1 Odin** maximum\n"
                      "• **1 Judge** maximum\n"
                      "• **1 Operator** maximum\n"
                      "*(Ultimatum Chamber exclu)*",
                inline=True
            )
            
            ingame_embed.add_field(
                name="<a:GummyDragonMicrophone:1380884049375002624> Communication",
                value="• Chat vocal autorisé avant chaque manche\n"
                      "• Pas d'abus de communication\n"
                      "• Restez fair-play !",
                inline=True
            )
            
            ingame_embed.add_field(
                name="<a:Warning:1380884984595742790> Interdictions",
                value="• **Instalock interdit**\n"
                      "• Pas de trashtalk\n"
                      "• Comportements toxiques = sanction\n"
                      "• **Smurf interdit** (ne mentez pas)\n"
                      "• Absence non justifiée = sanction",
                inline=False
            )
            
            # Envoyer avec les boutons directement après les règles en jeu
            await channel.send(embed=ingame_embed, view=self.rules_view)
            
            # Message de succès final
            success_embed = discord.Embed(
                title="✅ Règlement PP déployé avec succès !",
                description=f"Le salon {channel.mention} a été nettoyé et le règlement des parties personnalisées a été configuré !",
                color=discord.Color.green()
            )
            success_embed.add_field(
                name="<a:INFINITYBYP:1380887933325676706> Déployé dans",
                value=channel.mention,
                inline=True
            )
            success_embed.add_field(
                name="🎯 Fonctionnalités",
                value="• Acceptation des règles\n• Notifications PP\n• Accès aux salons",
                inline=True
            )
            success_embed.set_footer(text="Configuration terminée - Radiant Order")
            
            await setup_message.edit(embed=success_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erreur lors du déploiement",
                description=f"Une erreur s'est produite :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await setup_message.edit(embed=error_embed)

    @reglement_pp.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """📺 Définir le channel du règlement PP"""
        await self.config.guild(ctx.guild).rules_channel.set(channel.id)
        
        embed = discord.Embed(
            title="✅ Channel configuré",
            description=f"Le channel du règlement PP est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @reglement_pp.command(name="rulesrole")
    async def set_rules_role(self, ctx, role: discord.Role):
        """👑 Définir le rôle des règles PP"""
        await self.config.guild(ctx.guild).rules_role.set(role.id)
        
        embed = discord.Embed(
            title="✅ Rôle des règles configuré",
            description=f"Le rôle des règles PP est maintenant {role.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @reglement_pp.command(name="notifsrole")
    async def set_notifs_role(self, ctx, role: discord.Role):
        """🔔 Définir le rôle des notifications PP"""
        await self.config.guild(ctx.guild).notifs_role.set(role.id)
        
        embed = discord.Embed(
            title="✅ Rôle des notifications configuré",
            description=f"Le rôle des notifications PP est maintenant {role.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        guild_config = self.config.guild(ctx.guild)
        
        channel_id = await guild_config.rules_channel()
        rules_role_id = await guild_config.rules_role()
        notifs_role_id = await guild_config.notifs_role()
        
        channel = ctx.guild.get_channel(channel_id)
        rules_role = ctx.guild.get_role(rules_role_id)
        notifs_role = ctx.guild.get_role(notifs_role_id)
        
        embed = discord.Embed(
            title="⚙️ Configuration Règlement PP",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="📺 Channel",
            value=channel.mention if channel else f"Introuvable ({channel_id})",
            inline=True
        )
        
        embed.add_field(
            name="👑 Rôle Règles",
            value=rules_role.mention if rules_role else f"Introuvable ({rules_role_id})",
            inline=True
        )
        
        embed.add_field(
            name="🔔 Rôle Notifications",
            value=notifs_role.mention if notifs_role else f"Introuvable ({notifs_role_id})",
            inline=True
        )
        
        embed.add_field(
            name="🛠️ Commandes",
            value="`!reglementpp setup` - Déployer le règlement\n"
                  "`!reglementpp channel` - Changer le channel\n"
                  "`!reglementpp rulesrole` - Définir le rôle règles\n"
                  "`!reglementpp notifsrole` - Définir le rôle notifications",
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Règlement PP")
        
        await ctx.send(embed=embed)

    @reglement_pp.command(name="stats")
    async def show_stats(self, ctx):
        """📊 Statistiques des rôles PP"""
        guild_config = self.config.guild(ctx.guild)
        
        rules_role_id = await guild_config.rules_role()
        notifs_role_id = await guild_config.notifs_role()
        
        rules_role = ctx.guild.get_role(rules_role_id)
        notifs_role = ctx.guild.get_role(notifs_role_id)
        
        embed = discord.Embed(
            title="📊 Statistiques Parties Personnalisées",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        if rules_role:
            embed.add_field(
                name="👑 Règles Acceptées",
                value=f"{len(rules_role.members)} membres",
                inline=True
            )
        
        if notifs_role:
            embed.add_field(
                name="🔔 Notifications Activées",
                value=f"{len(notifs_role.members)} membres",
                inline=True
            )
        
        if rules_role and notifs_role:
            # Calculer le pourcentage
            total_rules = len(rules_role.members)
            total_notifs = len(notifs_role.members)
            if total_rules > 0:
                percentage = round((total_notifs / total_rules) * 100, 1)
                embed.add_field(
                    name="📈 Taux de Notifications",
                    value=f"{percentage}% des joueurs PP",
                    inline=True
                )
        
        embed.set_footer(text="Radiant Order - Statistiques PP")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReglementPP(bot))

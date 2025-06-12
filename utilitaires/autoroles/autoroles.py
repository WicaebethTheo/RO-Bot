import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
import asyncio

class ValorantRanksView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Unrated", style=discord.ButtonStyle.secondary, custom_id="rank_unrated", emoji="⚪")
    async def unrated(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Unrated")

    @discord.ui.button(label="Iron", style=discord.ButtonStyle.secondary, custom_id="rank_iron", emoji="<:Fer:1380653184246218924>")
    async def iron(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Iron")

    @discord.ui.button(label="Bronze", style=discord.ButtonStyle.secondary, custom_id="rank_bronze", emoji="<:Bronze:1380653187073052692>")
    async def bronze(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Bronze")

    @discord.ui.button(label="Silver", style=discord.ButtonStyle.secondary, custom_id="rank_silver", emoji="<:Argent:1380653207805497394>")
    async def silver(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Silver")

    @discord.ui.button(label="Gold", style=discord.ButtonStyle.secondary, custom_id="rank_gold", emoji="<:Or:1380653189984161802>")
    async def gold(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Gold")

class ValorantRanksView2(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Platinum", style=discord.ButtonStyle.primary, custom_id="rank_platinum", emoji="<:Platine:1380653202957144264>")
    async def platinum(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Platinum")

    @discord.ui.button(label="Diamond", style=discord.ButtonStyle.primary, custom_id="rank_diamond", emoji="<:Diamant:1380653188478271638>")
    async def diamond(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Diamond")

    @discord.ui.button(label="Ascendant", style=discord.ButtonStyle.primary, custom_id="rank_ascendant", emoji="<:Ascendant:1380653185663893586>")
    async def ascendant(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Ascendant")

    @discord.ui.button(label="Immortal", style=discord.ButtonStyle.danger, custom_id="rank_immortal", emoji="<:Immortel:1380653192525905980>")
    async def immortal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Immortal")

    @discord.ui.button(label="Radiant", style=discord.ButtonStyle.danger, custom_id="rank_radiant", emoji="<:Radiant:1380653206207467580>")
    async def radiant(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.toggle_role(interaction, "Radiant")

class AutoRoles(commands.Cog):
    """<a:FallingPetals:1380882470060425267> Système d'auto-rôles pour les rangs Valorant"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321123)
        
        default_guild = {
            "autoroles_channel": 1380560529810002073,
            "rank_roles": {
                "Unrated": None,  # Pas d'ID fourni
                "Iron": 1380572318602104932,     # Fer
                "Bronze": 1380572089295044749,   # Bronze
                "Silver": 1380571873435320350,   # Argent
                "Gold": 1380571721672953856,     # Or
                "Platinum": 1380571586326822923, # Platine
                "Diamond": 1380571473873473666,  # Diamant
                "Ascendant": 1380571196386443366, # Ascendant
                "Immortal": 1380570565995266069, # Immortel
                "Radiant": 1380570718231724112   # Radiant
            }
        }
        
        self.config.register_guild(**default_guild)
        
        # Vues persistantes
        self.ranks_view_1 = ValorantRanksView(self)
        self.ranks_view_2 = ValorantRanksView2(self)

    async def cog_load(self):
        """Ajouter les vues persistantes au bot"""
        self.bot.add_view(self.ranks_view_1)
        self.bot.add_view(self.ranks_view_2)

    async def toggle_role(self, interaction, role_name):
        """Ajouter ou retirer un rôle"""
        guild = interaction.guild
        user = interaction.user
        
        # Vérification spéciale pour le rang Radiant
        if role_name == "Radiant":
            radiant_embed = discord.Embed(
                title="<:Radiant:1380653206207467580> Rang Radiant",
                description="**Le rang Radiant nécessite une vérification !**\n\n"
                           "<a:CanYouHelp_By_Frogverbal:1380889107323949106> **Créez un ticket de support** pour prouver votre rang Radiant\n"
                           "<a:Animated_Arrow_Blue:1380888378953961472> **Préparez vos screenshots** de votre rang en jeu\n"
                           "<a:check_ravena:1380884332708626493> **Notre équipe vérifiera** votre niveau avant attribution\n\n"
                           "<a:boost:1380882468621520916> Le rang Radiant est réservé aux joueurs d'élite !",
                color=0xFF6B9D  # Couleur rose/rouge pour Radiant
            )
            radiant_embed.add_field(
                name="<a:INFINITYBYP:1380887933325676706> Procédure",
                value="1. Allez dans <#1380560533102530560>\n"
                      "2. Cliquez sur **<a:CanYouHelp_By_Frogverbal:1380889107323949106> Créer un ticket Support**\n"
                      "3. Fournissez vos preuves de rang Radiant\n"
                      "4. Attendez la validation du staff",
                inline=False
            )
            radiant_embed.set_footer(text="Radiant Order - Vérification Radiant")
            radiant_embed.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/1/1a/Radiant_Rank.png/revision/latest?cb=20200623203621")
            
            return await interaction.response.send_message(embed=radiant_embed, ephemeral=True)
        
        # Récupérer la configuration des rôles
        rank_roles = await self.config.guild(guild).rank_roles()
        
        # Déterminer le type de rôle et récupérer l'ID
        if role_name in rank_roles:
            role_id = rank_roles[role_name]
            role_type = "rang"
        else:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur",
                description="Rôle non configuré.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        if not role_id:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Rôle non configuré",
                description=f"Le rôle **{role_name}** n'est pas encore configuré. Contactez un administrateur.",
                color=discord.Color.orange()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        role = guild.get_role(role_id)
        if not role:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Rôle introuvable",
                description=f"Le rôle **{role_name}** n'existe plus sur le serveur.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        try:
            if role in user.roles:
                # Retirer le rôle
                await user.remove_roles(role, reason="Auto-rôles: retrait de rôle")
                
                embed = discord.Embed(
                    title="<a:PinkLoading:1380886781062414356> Rôle retiré",
                    description=f"Le rôle **{role.name}** a été retiré !",
                    color=discord.Color.orange()
                )
                embed.set_footer(text="Radiant Order - Auto-rôles")
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            else:
                # Gestion spéciale pour les rangs (exclusifs)
                if role_type == "rang":
                    # Retirer tous les autres rangs
                    ranks_to_remove = []
                    for rank_name, rank_id in rank_roles.items():
                        if rank_id and rank_name != role_name:
                            rank_role = guild.get_role(rank_id)
                            if rank_role and rank_role in user.roles:
                                ranks_to_remove.append(rank_role)
                    
                    if ranks_to_remove:
                        await user.remove_roles(*ranks_to_remove, reason="Auto-rôles: changement de rang")
                
                # Ajouter le nouveau rôle
                await user.add_roles(role, reason="Auto-rôles: ajout de rôle")
                
                # Message de confirmation personnalisé
                if role_type == "rang":
                    embed = discord.Embed(
                        title="<a:FallingPetals:1380882470060425267> Rang mis à jour !",
                        description=f"Votre rang Valorant est maintenant **{role.name}** !\n"
                                   f"Bon jeu sur Radiant Order ! <a:boost:1380882468621520916>",
                        color=role.color if role.color != discord.Color.default() else discord.Color.green()
                    )
                    embed.set_thumbnail(url="https://media.valorant-api.com/ranks/icons/iron.png")
                
                embed.set_footer(text="Radiant Order - Auto-rôles")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur de permissions",
                description="Je n'ai pas les permissions pour gérer ce rôle.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Erreur",
                description=f"Une erreur s'est produite :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @commands.group(name="autoroles")
    @checks.admin_or_permissions(manage_roles=True)
    async def autoroles(self, ctx):
        """<a:FallingPetals:1380882470060425267> Gestion du système d'auto-rôles"""
        pass

    @autoroles.command(name="setup")
    async def setup_autoroles(self, ctx):
        """<a:boost:1380882468621520916> Configurer les messages d'auto-rôles"""
        channel_id = await self.config.guild(ctx.guild).autoroles_channel()
        channel = ctx.guild.get_channel(channel_id)
        
        if not channel:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Channel d'auto-rôles non configuré.")
        
        # Clear le channel avant d'envoyer les nouveaux messages
        try:
            await ctx.send("<a:maruloader:1380888045259329569> Nettoyage du channel en cours...")
            
            # Supprimer tous les messages du channel
            async for message in channel.history(limit=None):
                try:
                    await message.delete()
                    await asyncio.sleep(0.5)  # Éviter le rate limit
                except:
                    pass
            
            await ctx.send("<a:check_ravena:1380884332708626493> Channel nettoyé ! Envoi des nouveaux messages...")
            
        except discord.Forbidden:
            await ctx.send("<a:Warning:1380884984595742790> Impossible de nettoyer le channel, permissions insuffisantes. Envoi des messages...")
        except Exception as e:
            await ctx.send(f"<a:Warning:1380884984595742790> Erreur lors du nettoyage: {str(e)}. Envoi des messages...")
        
        # Message d'introduction
        intro_embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Auto-Rôles Radiant Order",
            description="**Bienvenue dans le système d'auto-rôles !**\n\n"
                       "Sélectionnez votre rang Valorant en cliquant sur les boutons ci-dessous :\n\n"
                       "<a:boost:1380882468621520916> **Rangs Valorant** - Indiquez votre niveau de jeu\n\n"
                       "<a:check_ravena:1380884332708626493> Les rangs sont exclusifs (un seul à la fois)\n"
                       "<a:PinkLoading:1380886781062414356> Cliquez à nouveau pour retirer un rôle",
            color=discord.Color.blue()
        )
        intro_embed.set_footer(text="Radiant Order - Sélection de rôles")
        intro_embed.set_thumbnail(url="https://logoeps.com/wp-content/uploads/2021/06/valorant-vector-logo.png")
        
        await channel.send(embed=intro_embed)
        
        # Message rangs bas
        ranks_low_embed = discord.Embed(
            title="<a:boost:1380882468621520916> Rangs Valorant - Niveaux Débutants",
            description="**Sélectionnez votre rang actuel :**\n\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> **Unrated** - Pas encore classé\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Fer:1380653184246218924> **Iron** - Fer (débutant)\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Bronze:1380653187073052692> **Bronze** - Bronze\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Argent:1380653207805497394> **Silver** - Argent\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Or:1380653189984161802> **Gold** - Or",
            color=0x8B4513  # Couleur bronze
        )
        ranks_low_embed.set_footer(text="Cliquez sur un bouton pour sélectionner votre rang")
        
        await channel.send(embed=ranks_low_embed, view=self.ranks_view_1)
        
        # Message rangs élevés
        ranks_high_embed = discord.Embed(
            title="<a:Lightblueheartgif:1380882450439471165> Rangs Valorant - Niveaux Avancés",
            description="**Rangs pour les joueurs expérimentés :**\n\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Platine:1380653202957144264> **Platinum** - Platine\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Diamant:1380653188478271638> **Diamond** - Diamant\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Ascendant:1380653185663893586> **Ascendant** - Ascendant\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Immortel:1380653192525905980> **Immortal** - Immortel\n"
                       "<a:Animated_Arrow_Blue:1380888378953961472> <:Radiant:1380653206207467580> **Radiant** - Radiant (élite)",
            color=0x00CED1  # Couleur turquoise
        )
        ranks_high_embed.set_footer(text="Réservé aux joueurs de haut niveau")
        
        await channel.send(embed=ranks_high_embed, view=self.ranks_view_2)
        
        success_embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Auto-rôles configurés !",
            description=f"Les messages d'auto-rôles ont été envoyés dans {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=success_embed)

    @autoroles.command(name="setrole")
    async def set_role(self, ctx, role_type: str, role_name: str, role: discord.Role):
        """<a:Animated_Arrow_Blue:1380888378953961472> Configurer un rôle (rank role_name @role)"""
        if role_type.lower() == "rank":
            rank_roles = await self.config.guild(ctx.guild).rank_roles()
            if role_name in rank_roles:
                rank_roles[role_name] = role.id
                await self.config.guild(ctx.guild).rank_roles.set(rank_roles)
                
                embed = discord.Embed(
                    title="<a:check_ravena:1380884332708626493> Rôle de rang configuré",
                    description=f"Le rang **{role_name}** est maintenant lié au rôle {role.mention}.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                available_ranks = ", ".join(rank_roles.keys())
                await ctx.send(f"<a:uncheck_ravena:1380884331534483629> Rang invalide. Rangs disponibles : {available_ranks}")
        
        else:
            await ctx.send("<a:uncheck_ravena:1380884331534483629> Type invalide. Utilisez 'rank'.")

    @autoroles.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le channel d'auto-rôles"""
        await self.config.guild(ctx.guild).autoroles_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Channel configuré",
            description=f"Le channel d'auto-rôles est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @autoroles.command(name="config")
    async def show_config(self, ctx):
        """<a:INFINITYBYP:1380887933325676706> Afficher la configuration actuelle"""
        channel_id = await self.config.guild(ctx.guild).autoroles_channel()
        rank_roles = await self.config.guild(ctx.guild).rank_roles()
        
        channel = ctx.guild.get_channel(channel_id)
        
        embed = discord.Embed(
            title="<a:maruloader:1380888045259329569> Configuration Auto-Rôles",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Channel",
            value=channel.mention if channel else f"Introuvable ({channel_id})",
            inline=False
        )
        
        # Rangs configurés
        rank_config = ""
        for rank, role_id in rank_roles.items():
            if role_id:
                role = ctx.guild.get_role(role_id)
                rank_config += f"<a:Animated_Arrow_Blue:1380888378953961472> **{rank}**: {role.mention if role else 'Introuvable'}\n"
            else:
                rank_config += f"<a:Animated_Arrow_Blue:1380888378953961472> **{rank}**: *Non configuré*\n"
        
        embed.add_field(
            name="<a:boost:1380882468621520916> Rangs Valorant",
            value=rank_config if rank_config else "*Aucun configuré*",
            inline=True
        )
        
        await ctx.send(embed=embed)

    @autoroles.command(name="stats")
    async def show_stats(self, ctx):
        """<a:PinkLoading:1380886781062414356> Statistiques des rôles"""
        rank_roles = await self.config.guild(ctx.guild).rank_roles()
        
        embed = discord.Embed(
            title="<a:PinkLoading:1380886781062414356> Statistiques des Auto-Rôles",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        # Stats des rangs
        rank_stats = ""
        total_ranked = 0
        for rank, role_id in rank_roles.items():
            if role_id:
                role = ctx.guild.get_role(role_id)
                if role:
                    count = len(role.members)
                    total_ranked += count
                    rank_stats += f"<a:Animated_Arrow_Blue:1380888378953961472> **{rank}**: {count} membres\n"
        
        embed.add_field(
            name="<a:boost:1380882468621520916> Répartition des Rangs",
            value=rank_stats + f"\n**Total classés**: {total_ranked}" if rank_stats else "*Aucune donnée*",
            inline=True
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoRoles(bot)) 
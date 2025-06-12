import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import asyncio
import datetime

class AccepterReglementView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)  # Le bouton reste actif indéfiniment
        self.cog = cog
        
    @discord.ui.button(label="J'accepte le règlement", style=discord.ButtonStyle.success, emoji="<a:check_ravena:1380884332708626493>", custom_id="accepter_reglement")
    async def accepter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Réagit quand un utilisateur clique sur le bouton d'acceptation"""
        await self.cog.handle_reglement_accept(interaction)

class Reglement(commands.Cog):
    """<a:INFINITYBYP:1380887933325676706> Système de règlement stylé pour serveur gaming Discord <a:check_ravena:1380884332708626493>"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=156465489412, force_registration=True)
        
        default_guild = {
            "reglement": {
                "introduction": "\n\nPour garantir une expérience de jeu agréable pour tous, respectez les règles suivantes.\n\n<a:Warning:1380884984595742790> Tout manquement peut entraîner des sanctions.",
                "sections": {
                    "1": {
                        "titre": "<a:Lightblueheartgif:1380882450439471165> Respect",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Pas d'insultes, harcèlement ou discrimination\n<a:Animated_Arrow_Blue:1380888378953961472> Débats autorisés dans le respect\n<a:Animated_Arrow_Blue:1380888378953961472> Pas de spam ou flood\n<a:Animated_Arrow_Blue:1380888378953961472> Esprit sportif obligatoire"
                    },
                    "2": {
                        "titre": "<a:uncheck_ravena:1380884331534483629> Contenus interdits",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Contenu NSFW strictement interdit\n<a:Animated_Arrow_Blue:1380888378953961472> Pas de promotion de cheats ou hacks\n<a:Animated_Arrow_Blue:1380888378953961472> Évitez les sujets sensibles (politique, religion)\n<a:Animated_Arrow_Blue:1380888378953961472> Pas de contenu choquant"
                    },
                    "3": {
                        "titre": "<a:speechbubble:1380892653847314534> Organisation",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Utilisez les bons salons\n<a:Animated_Arrow_Blue:1380888378953961472> Volume raisonnable en vocal\n<a:Animated_Arrow_Blue:1380888378953961472> Pseudos et avatars appropriés\n<a:Animated_Arrow_Blue:1380888378953961472> Respectez l'organisation du serveur"
                    },
                    "4": {
                        "titre": "<a:Anouncements_Animated:1380895055694528542> Publicité",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Publicité pour autres serveurs interdite\n<a:Animated_Arrow_Blue:1380888378953961472> Autopromotion dans les salons dédiés uniquement\n<a:Animated_Arrow_Blue:1380888378953961472> Pas de vente en dehors des zones prévues"
                    },
                    "5": {
                        "titre": "<a:FallingPetals:1380882470060425267> Gaming",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Fair-play obligatoire, pas de triche\n<a:Animated_Arrow_Blue:1380888378953961472> Évitez le rage-quit\n<a:Animated_Arrow_Blue:1380888378953961472> Entraide encouragée\n<a:Animated_Arrow_Blue:1380888378953961472> Respectez les stratégies d'équipe"
                    },
                    "6": {
                        "titre": "<a:CanYouHelp_By_Frogverbal:1380889107323949106> Staff",
                        "contenu": "<a:Animated_Arrow_Blue:1380888378953961472> Respectez les décisions du staff\n<a:Animated_Arrow_Blue:1380888378953961472> Problème ? Créez un ticket\n<a:Animated_Arrow_Blue:1380888378953961472> Pas de contournement des sanctions"
                    }
                },
                "conclusion": "\n\nEn acceptant ce règlement, vous vous engagez à respecter ces règles.\n\nL'équipe de modération peut modifier ce règlement à tout moment.\n\n**Good luck, have fun !** <a:FallingPetals:1380882470060425267>",
            },
            "reglement_channel_id": 1380560525871550502,  # Canal par défaut configuré
            "reglement_message_id": None,
            "role_acceptation_id": None,
            "logs_channel_id": None,
            "derniere_maj": None,
        }
        
        self.config.register_guild(**default_guild)
        self.accept_view = AccepterReglementView(self)
        
    async def handle_reglement_accept(self, interaction):
        """Traite l'interaction lorsqu'un utilisateur accepte le règlement"""
        guild = interaction.guild
        guild_config = self.config.guild(guild)
        role_id = await guild_config.role_acceptation_id()
        logs_id = await guild_config.logs_channel_id()
        
        if not role_id:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Configuration Manquante",
                description="Aucun rôle n'est configuré pour l'acceptation du règlement.",
                color=discord.Color.orange()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
        role = guild.get_role(role_id)
        if not role:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur de Rôle",
                description="Le rôle configuré est introuvable. Veuillez contacter un administrateur.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
        # Attribuer le rôle
        try:
            await interaction.user.add_roles(role, reason="<a:check_ravena:1380884332708626493> Acceptation du règlement Radiant Order")
            
            success_embed = discord.Embed(
                title="<a:FallingPetals:1380882470060425267> Bienvenue dans Radiant Order !",
                description=f"<a:check_ravena:1380884332708626493> **{interaction.user.mention}** a accepté le règlement !\n\n<a:FallingPetals:1380882470060425267> Vous avez maintenant accès au serveur.\n<a:boost:1380882468621520916> Que les meilleurs gagnent !",
                color=discord.Color.gold()
            )
            success_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            success_embed.add_field(
                name="<a:Animated_Arrow_Blue:1380888378953961472> Prochaines étapes",
                value="<a:Animated_Arrow_Blue:1380888378953961472> Découvrez les salons\n<a:Animated_Arrow_Blue:1380888378953961472> Présentez-vous\n<a:Animated_Arrow_Blue:1380888378953961472> Rejoignez les parties !",
                inline=False
            )
            success_embed.set_footer(text="Radiant Order - Where Legends Are Born", icon_url=guild.icon.url if guild.icon else None)
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
            # Envoyer un log stylé
            if logs_id:
                logs_channel = guild.get_channel(logs_id)
                if logs_channel:
                    log_embed = discord.Embed(
                        title="<a:check_ravena:1380884332708626493> Nouveau membre accepté !",
                        description=f"<a:FallingPetals:1380882470060425267> {interaction.user.mention} vient de rejoindre **Radiant Order** !",
                        color=discord.Color.green(),
                        timestamp=datetime.datetime.now()
                    )
                    log_embed.set_author(name=f"{interaction.user.display_name} ({interaction.user.name})", icon_url=interaction.user.display_avatar.url)
                    log_embed.add_field(name="<a:INFINITYBYP:1380887933325676706> ID Utilisateur", value=f"`{interaction.user.id}`", inline=True)
                    log_embed.add_field(name="<a:PinkLoading:1380886781062414356> Compte créé le", value=f"<t:{int(interaction.user.created_at.timestamp())}:F>", inline=True)
                    log_embed.add_field(name="<a:boost:1380882468621520916> Membres totaux", value=f"{len(role.members)} gamers", inline=True)
                    log_embed.set_footer(text="Radiant Order Logs", icon_url=guild.icon.url if guild.icon else None)
                    await logs_channel.send(embed=log_embed)
                    
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Permission Refusée",
                description="Je n'ai pas la permission d'attribuer ce rôle. Veuillez contacter un administrateur.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Erreur Système",
                description=f"Une erreur inattendue s'est produite:\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    def cog_unload(self):
        """Nettoyage lors du déchargement du cog"""
        if hasattr(self, 'accept_view') and self.accept_view:
            self.accept_view.stop()

    @commands.group(name="reglement")
    async def reglement(self, ctx):
        """<a:check_ravena:1380884332708626493> Commandes liées au règlement de Radiant Order"""
        pass

    @reglement.command(name="afficher")
    async def afficher_reglement(self, ctx):
        """<a:INFINITYBYP:1380887933325676706> Affiche le règlement complet du serveur"""
        reglement_data = await self.config.guild(ctx.guild).reglement()
        
        embeds = []
        
        # Embed d'introduction stylé
        intro_embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> RÈGLEMENT RADIANT ORDER <a:check_ravena:1380884332708626493>",
            description=reglement_data["introduction"],
            color=discord.Color.from_rgb(255, 215, 0)  # Gold
        )
        intro_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        intro_embed.set_footer(text=f"🎮 Serveur {ctx.guild.name} • Where Legends Are Born", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embeds.append(intro_embed)
        
        # Embeds pour chaque section avec couleurs alternées
        colors = [discord.Color.red(), discord.Color.blue(), discord.Color.green(), 
                 discord.Color.purple(), discord.Color.orange(), discord.Color.magenta()]
        
        for i, (num, section) in enumerate(reglement_data["sections"].items()):
            section_embed = discord.Embed(
                title=f"{section['titre']}",
                description=section["contenu"],
                color=colors[i % len(colors)]
            )
            section_embed.set_footer(text=f"Section {num} • Radiant Order", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            embeds.append(section_embed)
        
        # Embed de conclusion stylé
        conclusion_embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> ACCEPTATION & CONCLUSION",
            description=reglement_data["conclusion"],
            color=discord.Color.from_rgb(255, 215, 0)  # Gold
        )
        
        derniere_maj = await self.config.guild(ctx.guild).derniere_maj()
        if derniere_maj:
            conclusion_embed.set_footer(text=f"⚡ Dernière mise à jour: {derniere_maj} • Radiant Order", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        else:
            conclusion_embed.set_footer(text="⚡ Radiant Order - Where Legends Are Born", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            
        embeds.append(conclusion_embed)
        
        await menu(ctx, embeds, DEFAULT_CONTROLS)
        
    @reglement.command(name="section")
    async def afficher_section(self, ctx, numero: str):
        """Affiche une section spécifique du règlement
        
        Exemple: !reglement section 2
        """
        reglement_data = await self.config.guild(ctx.guild).reglement()
        
        if numero not in reglement_data["sections"]:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Cette section n'existe pas dans le règlement.")
        
        section = reglement_data["sections"][numero]
        
        embed = discord.Embed(
            title=f"Section {numero}: {section['titre']}",
            description=section["contenu"],
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Règlement de {ctx.guild.name}")
        
        await ctx.send(embed=embed)
        
    @reglement.command(name="recherche")
    async def recherche_reglement(self, ctx, *, terme: str):
        """Recherche un terme dans le règlement
        
        Exemple: !reglement recherche spam
        """
        reglement_data = await self.config.guild(ctx.guild).reglement()
        resultats = []
        
        # Recherche dans l'introduction
        if terme.lower() in reglement_data["introduction"].lower():
            resultats.append(("Introduction", reglement_data["introduction"]))
            
        # Recherche dans les sections
        for num, section in reglement_data["sections"].items():
            if terme.lower() in section["titre"].lower() or terme.lower() in section["contenu"].lower():
                resultats.append((f"Section {num}: {section['titre']}", section["contenu"]))
                
        # Recherche dans la conclusion
        if terme.lower() in reglement_data["conclusion"].lower():
            resultats.append(("Conclusion", reglement_data["conclusion"]))
            
        if not resultats:
            return await ctx.send(f"<a:uncheck_ravena:1380884331534483629> Aucun résultat trouvé pour '{terme}'.")
            
        embeds = []
        for titre, contenu in resultats:
            embed = discord.Embed(
                title=titre,
                description=contenu,
                color=discord.Color.green()
            )
            # On surligne le terme recherché
            embed.set_footer(text=f"Recherche: '{terme}'")
            embeds.append(embed)
            
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @checks.admin_or_permissions(manage_guild=True)
    @reglement.command(name="configurer")
    async def configurer_reglement(self, ctx):
        """Configure les paramètres du règlement (Admin uniquement)"""
        # Configuration interactive du règlement
        await ctx.send("<a:maruloader:1380888045259329569> **Configuration du système de règlement**\n"
                       "Veuillez répondre aux questions suivantes pour configurer le règlement.\n"
                       "Vous pouvez répondre `annuler` à tout moment pour annuler le processus.")

        # Fonction vérification réponse
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Canal du règlement
        await ctx.send("<a:INFINITYBYP:1380887933325676706> Dans quel canal voulez-vous publier le règlement ? Mentionnez le canal ou indiquez son ID.")
        try:
            reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
            if reponse.content.lower() == "annuler":
                return await ctx.send("<a:uncheck_ravena:1380884331534483629> Configuration annulée.")
                
            # Extraction du canal
            if reponse.channel_mentions:
                channel = reponse.channel_mentions[0]
            else:
                try:
                    channel_id = int(reponse.content.strip())
                    channel = ctx.guild.get_channel(channel_id)
                    if not channel:
                        return await ctx.send("<a:uncheck_ravena:1380884331534483629> Canal introuvable. Configuration annulée.")
                except ValueError:
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Canal invalide. Configuration annulée.")
                    
            await self.config.guild(ctx.guild).reglement_channel_id.set(channel.id)
            
            # Rôle d'acceptation
            await ctx.send("<a:CanYouHelp_By_Frogverbal:1380889107323949106> Quel rôle souhaitez-vous attribuer aux membres qui acceptent le règlement ? "
                           "Mentionnez le rôle ou indiquez son ID. Répondez `aucun` si vous ne voulez pas utiliser cette fonction.")
            reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
            if reponse.content.lower() == "annuler":
                return await ctx.send("<a:uncheck_ravena:1380884331534483629> Configuration annulée.")
                
            if reponse.content.lower() != "aucun":
                # Extraction du rôle
                if reponse.role_mentions:
                    role = reponse.role_mentions[0]
                    await self.config.guild(ctx.guild).role_acceptation_id.set(role.id)
                else:
                    try:
                        role_id = int(reponse.content.strip())
                        role = ctx.guild.get_role(role_id)
                        if not role:
                            await ctx.send("<a:Warning:1380884984595742790> Rôle introuvable. La fonction d'acceptation sera désactivée.")
                            await self.config.guild(ctx.guild).role_acceptation_id.set(None)
                        else:
                            await self.config.guild(ctx.guild).role_acceptation_id.set(role.id)
                    except ValueError:
                        await ctx.send("<a:Warning:1380884984595742790> ID de rôle invalide. La fonction d'acceptation sera désactivée.")
                        await self.config.guild(ctx.guild).role_acceptation_id.set(None)
            else:
                await self.config.guild(ctx.guild).role_acceptation_id.set(None)
                
            # Canal de logs
            await ctx.send("<a:agooglebell:1380895257541083300> Dans quel canal voulez-vous envoyer les logs d'acceptation du règlement ? "
                           "Mentionnez le canal ou indiquez son ID. Répondez `aucun` si vous ne voulez pas utiliser cette fonction.")
            reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
            if reponse.content.lower() == "annuler":
                return await ctx.send("<a:uncheck_ravena:1380884331534483629> Configuration annulée.")
                
            if reponse.content.lower() != "aucun":
                # Extraction du canal
                if reponse.channel_mentions:
                    logs_channel = reponse.channel_mentions[0]
                    await self.config.guild(ctx.guild).logs_channel_id.set(logs_channel.id)
                else:
                    try:
                        channel_id = int(reponse.content.strip())
                        logs_channel = ctx.guild.get_channel(channel_id)
                        if not logs_channel:
                            await ctx.send("<a:Warning:1380884984595742790> Canal de logs introuvable. La fonction de logs sera désactivée.")
                            await self.config.guild(ctx.guild).logs_channel_id.set(None)
                        else:
                            await self.config.guild(ctx.guild).logs_channel_id.set(logs_channel.id)
                    except ValueError:
                        await ctx.send("<a:Warning:1380884984595742790> ID de canal invalide. La fonction de logs sera désactivée.")
                        await self.config.guild(ctx.guild).logs_channel_id.set(None)
            else:
                await self.config.guild(ctx.guild).logs_channel_id.set(None)
                
            await ctx.send("<a:check_ravena:1380884332708626493> Configuration de base terminée! Utilisez `!reglement modifier` pour modifier le contenu du règlement.")
            
        except asyncio.TimeoutError:
            await ctx.send("<a:uncheck_ravena:1380884331534483629> Temps écoulé. Configuration annulée.")

    @checks.admin_or_permissions(manage_guild=True)
    @reglement.command(name="modifier")
    async def modifier_reglement(self, ctx):
        """Modifie le contenu du règlement (Admin uniquement)"""
        reglement_data = await self.config.guild(ctx.guild).reglement()
        
        await ctx.send("<a:INFINITYBYP:1380887933325676706> **Modification du règlement**\n"
                       "Que souhaitez-vous modifier ?\n"
                       "1️⃣ Introduction\n"
                       "2️⃣ Ajouter une section\n"
                       "3️⃣ Modifier une section existante\n"
                       "4️⃣ Supprimer une section\n"
                       "5️⃣ Conclusion\n"
                       "<a:uncheck_ravena:1380884331534483629> Annuler")
                       
        # Fonction de vérification
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        # Attente de la réponse
        try:
            reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
            if reponse.content.lower() == "annuler" or reponse.content == "❌":
                return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                
            choix = reponse.content
            
            # Introduction
            if choix == "1" or choix == "1️⃣":
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Veuillez entrer la nouvelle introduction:")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                    
                reglement_data["introduction"] = reponse.content
                await self.config.guild(ctx.guild).reglement.set(reglement_data)
                await ctx.send("<a:check_ravena:1380884332708626493> Introduction modifiée avec succès!")
                
            # Ajouter section
            elif choix == "2" or choix == "2️⃣":
                # Déterminer le numéro de section
                section_nums = [int(k) for k in reglement_data["sections"].keys() if k.isdigit()]
                next_section = str(max(section_nums) + 1 if section_nums else 1)
                
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Création de la section {next_section}")
                
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Entrez le titre de cette section:")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Création annulée.")
                    
                titre = reponse.content
                
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Entrez le contenu de cette section:")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Création annulée.")
                    
                contenu = reponse.content
                
                # Ajout de la section
                reglement_data["sections"][next_section] = {
                    "titre": titre,
                    "contenu": contenu
                }
                
                await self.config.guild(ctx.guild).reglement.set(reglement_data)
                await ctx.send("<a:check_ravena:1380884332708626493> Section {next_section} ajoutée avec succès!")
                
            # Modifier section
            elif choix == "3" or choix == "3️⃣":
                # Afficher les sections disponibles
                sections = "\n".join([f"{num}. {section['titre']}" for num, section in reglement_data["sections"].items()])
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Quelle section souhaitez-vous modifier ?\n{sections}")
                
                reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                    
                num_section = reponse.content
                if num_section not in reglement_data["sections"]:
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Section introuvable. Modification annulée.")
                    
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Modification de la section {num_section}: {reglement_data['sections'][num_section]['titre']}")
                
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Entrez le nouveau titre (ou `garder` pour conserver l'actuel):")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                    
                if reponse.content.lower() != "garder":
                    reglement_data["sections"][num_section]["titre"] = reponse.content
                
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Entrez le nouveau contenu (ou `garder` pour conserver l'actuel):")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                    
                if reponse.content.lower() != "garder":
                    reglement_data["sections"][num_section]["contenu"] = reponse.content
                
                await self.config.guild(ctx.guild).reglement.set(reglement_data)
                await ctx.send("<a:check_ravena:1380884332708626493> Section {num_section} modifiée avec succès!")
                
            # Supprimer section
            elif choix == "4" or choix == "4️⃣":
                # Afficher les sections disponibles
                sections = "\n".join([f"{num}. {section['titre']}" for num, section in reglement_data["sections"].items()])
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Quelle section souhaitez-vous supprimer ?\n{sections}")
                
                reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Suppression annulée.")
                    
                num_section = reponse.content
                if num_section not in reglement_data["sections"]:
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Section introuvable. Suppression annulée.")
                    
                # Confirmation
                await ctx.send("<a:Warning:1380884984595742790> Êtes-vous sûr de vouloir supprimer la section {num_section}: {reglement_data['sections'][num_section]['titre']} ? (oui/non)")
                
                reponse = await self.bot.wait_for("message", check=check, timeout=60.0)
                if reponse.content.lower() != "oui":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Suppression annulée.")
                    
                # Suppression
                del reglement_data["sections"][num_section]
                
                await self.config.guild(ctx.guild).reglement.set(reglement_data)
                await ctx.send("<a:check_ravena:1380884332708626493> Section {num_section} supprimée avec succès!")
                
            # Conclusion
            elif choix == "5" or choix == "5️⃣":
                await ctx.send("<a:INFINITYBYP:1380887933325676706> Veuillez entrer la nouvelle conclusion:")
                reponse = await self.bot.wait_for("message", check=check, timeout=300.0)
                if reponse.content.lower() == "annuler":
                    return await ctx.send("<a:uncheck_ravena:1380884331534483629> Modification annulée.")
                    
                reglement_data["conclusion"] = reponse.content
                await self.config.guild(ctx.guild).reglement.set(reglement_data)
                await ctx.send("<a:check_ravena:1380884332708626493> Conclusion modifiée avec succès!")
            
            else:
                await ctx.send("<a:uncheck_ravena:1380884331534483629> Option invalide. Modification annulée.")
                return
                
            # Mise à jour de la date
            await self.config.guild(ctx.guild).derniere_maj.set(datetime.datetime.now().strftime("%d/%m/%Y"))
                
        except asyncio.TimeoutError:
            await ctx.send("<a:uncheck_ravena:1380884331534483629> Temps écoulé. Modification annulée.")

    @checks.admin_or_permissions(manage_guild=True)
    @reglement.command(name="publier")
    async def publier_reglement(self, ctx):
        """<a:boost:1380882468621520916> Publie ou met à jour le règlement dans le canal configuré (Admin uniquement)"""
        reglement_data = await self.config.guild(ctx.guild).reglement()
        channel_id = await self.config.guild(ctx.guild).reglement_channel_id()
        role_id = await self.config.guild(ctx.guild).role_acceptation_id()
        message_id = await self.config.guild(ctx.guild).reglement_message_id()
        
        if not channel_id:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Configuration Manquante",
                description="Aucun canal n'a été configuré pour le règlement.\nUtilisez `!reglement configurer` d'abord.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=error_embed)
            
        channel = ctx.guild.get_channel(channel_id)
        if not channel:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Canal Introuvable",
                description="Le canal configuré est introuvable.\nVeuillez reconfigurer le règlement.",
                color=discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
            
        # Nettoyage du salon
        loading_embed = discord.Embed(
            title="<a:maruloader:1380888045259329569> Nettoyage en cours...",
            description="Préparation du salon pour le nouveau règlement.",
            color=discord.Color.blue()
        )
        loading_msg = await ctx.send(embed=loading_embed)
        
        try:
            await channel.purge(limit=100)
            
            success_embed = discord.Embed(
                title="<a:check_ravena:1380884332708626493> Salon Nettoyé",
                description="Prêt pour la publication du règlement !",
                color=discord.Color.green()
            )
            await loading_msg.edit(embed=success_embed)
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Permission Refusée",
                description="Je n'ai pas la permission de supprimer des messages dans ce salon.",
                color=discord.Color.red()
            )
            await loading_msg.edit(embed=error_embed)
            return
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Erreur",
                description=f"Erreur lors du nettoyage :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await loading_msg.edit(embed=error_embed)
            return
            
        # Création du règlement stylé
        try:
            # Embed principal ultra stylé
            main_embed = discord.Embed(
                title="<a:check_ravena:1380884332708626493> RÈGLEMENT OFFICIEL <a:check_ravena:1380884332708626493>",
                description=reglement_data["introduction"],
                color=discord.Color.from_rgb(255, 215, 0)
            )
            main_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
            
            # Ajouter les sections sans emojis supplémentaires
            for num, section in reglement_data["sections"].items():
                main_embed.add_field(
                    name=f"**{section['titre']}**",
                    value=section["contenu"][:1024],
                    inline=False
                )
            
            # Embed de conclusion avec bouton
            conclusion_embed = discord.Embed(
                title="<a:FallingPetals:1380882470060425267> REJOIGNEZ L'ÉLITE DE RADIANT ORDER !",
                description=reglement_data["conclusion"],
                color=discord.Color.from_rgb(255, 215, 0)
            )
            
            derniere_maj = await self.config.guild(ctx.guild).derniere_maj()
            footer_text = f"⚡ Dernière mise à jour: {derniere_maj} • Radiant Order" if derniere_maj else "⚡ Radiant Order - Where Legends Are Born"
            conclusion_embed.set_footer(text=footer_text, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            
            # Publication
            await channel.send(embed=main_embed)
            
            if role_id:
                message = await channel.send(embed=conclusion_embed, view=self.accept_view)
            else:
                message = await channel.send(embed=conclusion_embed)
                
            await self.config.guild(ctx.guild).reglement_message_id.set(message.id)
            
            final_embed = discord.Embed(
                title="<a:boost:1380882468621520916> Publication Réussie !",
                description=f"Règlement publié avec style dans {channel.mention} !",
                color=discord.Color.green()
            )
            await loading_msg.edit(embed=final_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Erreur de Publication",
                description=f"```{str(e)}```",
                color=discord.Color.red()
            )
            await loading_msg.edit(embed=error_embed)

    @checks.admin_or_permissions(manage_guild=True)
    @reglement.command(name="reboot")
    async def reboot_reglement(self, ctx):
        """Réinitialise le règlement aux valeurs par défaut (Admin uniquement)"""
        # Demande de confirmation
        await ctx.send("<a:Warning:1380884984595742790> **ATTENTION** <a:Warning:1380884984595742790>\nCette commande va réinitialiser l'intégralité du règlement aux valeurs par défaut.\n"
                      "Toutes vos modifications seront perdues.\n\n"
                      "Tapez `confirmer` pour continuer ou toute autre réponse pour annuler.")
                      
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        try:
            reponse = await self.bot.wait_for("message", check=check, timeout=30.0)
            if reponse.content.lower() != "confirmer":
                return await ctx.send("<a:uncheck_ravena:1380884331534483629> Réinitialisation annulée.")
                
            # Réinitialiser les données
            await self.config.guild(ctx.guild).clear()
            await ctx.send("<a:check_ravena:1380884332708626493> Le règlement a été réinitialisé aux valeurs par défaut.")
            
        except asyncio.TimeoutError:
            await ctx.send("<a:uncheck_ravena:1380884331534483629> Temps écoulé. Réinitialisation annulée.")

    @reglement.command(name="stats")
    @checks.admin_or_permissions(manage_guild=True)
    async def stats_reglement(self, ctx):
        """Affiche les statistiques du règlement (Admin uniquement)"""
        guild_config = self.config.guild(ctx.guild)
        reglement_data = await guild_config.reglement()
        channel_id = await guild_config.reglement_channel_id()
        role_id = await guild_config.role_acceptation_id()
        logs_id = await guild_config.logs_channel_id()
        message_id = await guild_config.reglement_message_id()
        derniere_maj = await guild_config.derniere_maj()
        
        embed = discord.Embed(
            title="<a:PinkLoading:1380886781062414356> Statistiques du règlement",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        # Informations générales
        embed.add_field(
            name="<a:INFINITYBYP:1380887933325676706> Contenu",
            value=f"Sections: {len(reglement_data['sections'])}\nDernière mise à jour: {derniere_maj or 'Jamais'}", 
            inline=False
        )
        
        # Informations de configuration
        channel = ctx.guild.get_channel(channel_id) if channel_id else None
        role = ctx.guild.get_role(role_id) if role_id else None
        logs_channel = ctx.guild.get_channel(logs_id) if logs_id else None
        
        embed.add_field(
            name="<a:maruloader:1380888045259329569> Configuration",
            value=f"Canal de publication: {channel.mention if channel else 'Non configuré'}\nRôle d'acceptation: {role.mention if role else 'Non configuré'}\nCanal de logs: {logs_channel.mention if logs_channel else 'Non configuré'}\nMessage ID: {message_id or 'Non publié'}",
            inline=False
        )
        
        # Stats du rôle
        if role:
            membres_avec_role = len(role.members)
            membres_totaux = ctx.guild.member_count
            pourcentage = (membres_avec_role / membres_totaux) * 100 if membres_totaux > 0 else 0
            
            embed.add_field(
                name="<a:boost:1380882468621520916> Acceptation",
                value=f"Membres ayant accepté: {membres_avec_role}/{membres_totaux} ({pourcentage:.1f}%)",
                inline=False
            )
            
        await ctx.send(embed=embed)

    @checks.admin_or_permissions(manage_guild=True)
    @reglement.command(name="setrole")
    async def set_acceptance_role(self, ctx, role: discord.Role):
        """Configure rapidement le rôle d'acceptation du règlement"""
        await self.config.guild(ctx.guild).role_acceptation_id.set(role.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Rôle configuré !",
            description=f"Le rôle d'acceptation est maintenant : {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def cog_load(self):
        """Ajouter les vues persistantes au bot après le redémarrage"""
        self.bot.add_view(self.accept_view)

async def setup(bot):
    await bot.add_cog(Reglement(bot))


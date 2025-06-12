import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
import asyncio
from discord.ui import Button, View, Modal, TextInput

def has_suggestions_role():
    """Check personnalisé pour le rôle de gestion des suggestions ou Wicaebeth"""
    async def predicate(ctx):
        # Vérifier si c'est Wicaebeth (accès spécial)
        if ctx.author.id == 257152912776495104:
            return True
        
        required_role_ids = [1381220960597839882, 1381222157929025626]
        
        for role_id in required_role_ids:
            required_role = ctx.guild.get_role(role_id)
            if required_role and required_role in ctx.author.roles:
                return True
        
        return False
    
    return commands.check(predicate)

class SuggestionModal(Modal):
    def __init__(self, cog):
        super().__init__(title="Nouvelle Suggestion - Radiant Order")
        self.cog = cog

    suggestion_title = TextInput(
        label="Titre de ta suggestion",
        placeholder="Ex: Nouveau mode de jeu, amélioration du serveur...",
        min_length=5,
        max_length=100,
        required=True
    )

    suggestion_description = TextInput(
        label="Description détaillée",
        placeholder="Explique ta suggestion en détail et pourquoi elle serait bénéfique...",
        style=discord.TextStyle.long,
        min_length=20,
        max_length=1000,
        required=True
    )

    suggestion_reason = TextInput(
        label="Pourquoi cette suggestion ?",
        placeholder="Quel problème cela résoudrait-il ? Quels avantages ?",
        style=discord.TextStyle.long,
        min_length=10,
        max_length=500,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        # Récupérer la configuration
        suggestions_channel_id = await self.cog.config.guild(interaction.guild).suggestions_channel()
        suggestions_channel = interaction.guild.get_channel(suggestions_channel_id)
        
        if not suggestions_channel:
            return await interaction.followup.send(
                "<a:uncheck_ravena:1380884331534483629> Le canal de suggestions n'est pas configuré.",
                ephemeral=True
            )
        
        # Créer un ID unique pour la suggestion
        suggestion_id = await self.cog.get_next_suggestion_id(interaction.guild)
        
        # Créer l'embed de suggestion
        embed = discord.Embed(
            title=f"<a:FallingPetals:1380882470060425267> Suggestion #{suggestion_id}",
            description=f"**{self.suggestion_title.value}**",
            color=0x3498DB,  # Bleu
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Description",
            value=self.suggestion_description.value,
            inline=False
        )
        
        embed.add_field(
            name="<a:Animated_Arrow_Blue:1380888378953961472> Justification",
            value=self.suggestion_reason.value,
            inline=False
        )
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Auteur",
            value=f"{interaction.user.mention}",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Statut",
            value="<a:PinkLoading:1380886781062414356> En attente",
            inline=True
        )
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Radiant Order - Système de suggestions")
        
        # Créer la vue avec les boutons de vote
        view = SuggestionVoteView(suggestion_id, self.cog)
        
        # Envoyer la suggestion
        try:
            suggestion_message = await suggestions_channel.send(embed=embed, view=view)
            
            # Sauvegarder les données de la suggestion
            await self.cog.save_suggestion_data(
                interaction.guild,
                suggestion_id,
                {
                    "title": self.suggestion_title.value,
                    "description": self.suggestion_description.value,
                    "reason": self.suggestion_reason.value,
                    "author_id": interaction.user.id,
                    "message_id": suggestion_message.id,
                    "status": "pending",
                    "upvotes": [],
                    "downvotes": [],
                    "created_at": datetime.datetime.now().isoformat()
                }
            )
            
            # Confirmation à l'utilisateur
            await interaction.followup.send(
                f"<a:check_ravena:1380884332708626493> Ta suggestion **#{suggestion_id}** a été envoyée avec succès !\n"
                f"<a:Animated_Arrow_Blue:1380888378953961472> Elle sera examinée par l'équipe de modération.\n"
                f"<a:boost:1380882468621520916> Les membres peuvent maintenant voter pour ta suggestion !",
                ephemeral=True
            )
            
        except discord.Forbidden:
            await interaction.followup.send(
                "<a:uncheck_ravena:1380884331534483629> Je n'ai pas les permissions pour envoyer dans le canal de suggestions.",
                ephemeral=True
            )

class SuggestionVoteView(View):
    def __init__(self, suggestion_id: int, cog):
        super().__init__(timeout=None)
        self.suggestion_id = suggestion_id
        self.cog = cog
        
        # Définir un custom_id unique pour la persistance
        self.upvote_button.custom_id = f"suggestion_upvote_{suggestion_id}"
        self.downvote_button.custom_id = f"suggestion_downvote_{suggestion_id}"

    @discord.ui.button(label="0", style=discord.ButtonStyle.success, emoji="<a:check_ravena:1380884332708626493>")
    async def upvote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_vote(interaction, "upvote")

    @discord.ui.button(label="0", style=discord.ButtonStyle.danger, emoji="<a:uncheck_ravena:1380884331534483629>")
    async def downvote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_vote(interaction, "downvote")

    async def handle_vote(self, interaction: discord.Interaction, vote_type: str):
        # Récupérer les données de la suggestion
        suggestion_data = await self.cog.get_suggestion_data(interaction.guild, self.suggestion_id)
        
        if not suggestion_data:
            return await interaction.response.send_message(
                "<a:uncheck_ravena:1380884331534483629> Cette suggestion n'existe plus.",
                ephemeral=True
            )
        
        user_id = interaction.user.id
        upvotes = suggestion_data.get("upvotes", [])
        downvotes = suggestion_data.get("downvotes", [])
        
        # Vérifier si l'utilisateur a déjà voté
        if vote_type == "upvote":
            if user_id in upvotes:
                return await interaction.response.send_message(
                    "<a:Warning:1380884984595742790> Tu as déjà voté positivement pour cette suggestion !",
                    ephemeral=True
                )
            
            # Retirer le downvote si présent et ajouter upvote
            if user_id in downvotes:
                downvotes.remove(user_id)
            upvotes.append(user_id)
            
        else:  # downvote
            if user_id in downvotes:
                return await interaction.response.send_message(
                    "<a:Warning:1380884984595742790> Tu as déjà voté négativement pour cette suggestion !",
                    ephemeral=True
                )
            
            # Retirer l'upvote si présent et ajouter downvote
            if user_id in upvotes:
                upvotes.remove(user_id)
            downvotes.append(user_id)
        
        # Sauvegarder les votes mis à jour
        suggestion_data["upvotes"] = upvotes
        suggestion_data["downvotes"] = downvotes
        await self.cog.save_suggestion_data(interaction.guild, self.suggestion_id, suggestion_data)
        
        # Mettre à jour les labels des boutons
        self.upvote_button.label = str(len(upvotes))
        self.downvote_button.label = str(len(downvotes))
        
        await interaction.response.edit_message(view=self)
        
        vote_emoji = "<a:check_ravena:1380884332708626493>" if vote_type == "upvote" else "<a:uncheck_ravena:1380884331534483629>"
        await interaction.followup.send(
            f"{vote_emoji} Ton vote a été enregistré pour la suggestion **#{self.suggestion_id}** !",
            ephemeral=True
        )

class SuggestionsSubmitView(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(
        label="Soumettre une suggestion",
        style=discord.ButtonStyle.primary,
        emoji="<a:FallingPetals:1380882470060425267>",
        custom_id="submit_suggestion"
    )
    async def submit_suggestion(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SuggestionModal(self.cog)
        await interaction.response.send_modal(modal)

class Suggestions(commands.Cog):
    """<a:FallingPetals:1380882470060425267> Système de suggestions pour Radiant Order"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321)
        
        default_guild = {
            "suggestions_channel": 1380560571874934896,
            "next_suggestion_id": 1,
            "suggestions_data": {}
        }
        
        self.config.register_guild(**default_guild)

    async def cog_load(self):
        """Réenregistrer les vues persistantes au démarrage"""
        self.bot.add_view(SuggestionsSubmitView(self))
        
        # Réenregistrer les vues de vote pour toutes les suggestions existantes
        for guild in self.bot.guilds:
            suggestions_data = await self.config.guild(guild).suggestions_data()
            for suggestion_id in suggestions_data.keys():
                view = SuggestionVoteView(int(suggestion_id), self)
                self.bot.add_view(view)

    async def get_next_suggestion_id(self, guild: discord.Guild) -> int:
        """Obtenir le prochain ID de suggestion"""
        current_id = await self.config.guild(guild).next_suggestion_id()
        await self.config.guild(guild).next_suggestion_id.set(current_id + 1)
        return current_id

    async def save_suggestion_data(self, guild: discord.Guild, suggestion_id: int, data: dict):
        """Sauvegarder les données d'une suggestion"""
        async with self.config.guild(guild).suggestions_data() as suggestions:
            suggestions[str(suggestion_id)] = data

    async def get_suggestion_data(self, guild: discord.Guild, suggestion_id: int) -> dict:
        """Récupérer les données d'une suggestion"""
        suggestions = await self.config.guild(guild).suggestions_data()
        return suggestions.get(str(suggestion_id))

    @commands.group(name="suggestions")
    @has_suggestions_role()
    async def suggestions_settings(self, ctx):
        """<a:boost:1380882468621520916> Gestion du système de suggestions"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @suggestions_settings.command(name="setup")
    async def setup_suggestions(self, ctx):
        """<a:FallingPetals:1380882470060425267> Configurer le message de suggestions"""
        suggestions_channel_id = await self.config.guild(ctx.guild).suggestions_channel()
        suggestions_channel = ctx.guild.get_channel(suggestions_channel_id)
        
        if not suggestions_channel:
            return await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Le canal de suggestions n'est pas configuré ou n'existe pas."
            )
        
        # Créer l'embed principal
        embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Suggestions Radiant Order",
            description=(
                "**Aide-nous à améliorer le serveur !**\n\n"
                "<a:speechbubble:1380892653847314534> Tu as une idée pour améliorer Radiant Order ?\n"
                "<a:boost:1380882468621520916> Une suggestion de nouveau mode de jeu ?\n"
                "<a:Animated_Arrow_Blue:1380888378953961472> Une amélioration pour la communauté ?\n\n"
                "**Clique sur le bouton ci-dessous pour soumettre ta suggestion !**\n\n"
                "<a:whitecrown:1380899677297315880> **Règles pour les suggestions :**\n"
                "• Sois respectueux et constructif\n"
                "• Explique clairement ton idée\n"
                "• Justifie pourquoi ce serait bénéfique\n"
                "• Une suggestion = un clic sur le bouton\n\n"
                "<a:agooglebell:1380895257541083300> Les membres peuvent voter pour tes suggestions !\n"
                "<a:PinkLoading:1380886781062414356> L'équipe examinera chaque suggestion."
            ),
            color=0x9B59B6
        )
        
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text="Radiant Order • Système de suggestions")
        
        # Créer la vue avec le bouton
        view = SuggestionsSubmitView(self)
        
        # Envoyer le message
        try:
            await suggestions_channel.send(embed=embed, view=view)
            await ctx.send(
                f"<a:check_ravena:1380884332708626493> Le système de suggestions a été configuré dans {suggestions_channel.mention} !"
            )
        except discord.Forbidden:
            await ctx.send(
                "<a:uncheck_ravena:1380884331534483629> Je n'ai pas les permissions pour envoyer dans le canal de suggestions."
            )

    @suggestions_settings.command(name="channel")
    async def set_suggestions_channel(self, ctx, channel: discord.TextChannel):
        """<a:speechbubble:1380892653847314534> Définir le canal de suggestions"""
        await self.config.guild(ctx.guild).suggestions_channel.set(channel.id)
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Canal configuré",
            description=f"Le canal de suggestions est maintenant {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @suggestions_settings.command(name="approve")
    async def approve_suggestion(self, ctx, suggestion_id: int, *, reason: str = None):
        """<a:check_ravena:1380884332708626493> Approuver une suggestion"""
        await self.update_suggestion_status(ctx, suggestion_id, "approved", reason)

    @suggestions_settings.command(name="reject")
    async def reject_suggestion(self, ctx, suggestion_id: int, *, reason: str = None):
        """<a:uncheck_ravena:1380884331534483629> Rejeter une suggestion"""
        await self.update_suggestion_status(ctx, suggestion_id, "rejected", reason)

    async def update_suggestion_status(self, ctx, suggestion_id: int, status: str, reason: str = None):
        """Mettre à jour le statut d'une suggestion"""
        suggestion_data = await self.get_suggestion_data(ctx.guild, suggestion_id)
        
        if not suggestion_data:
            return await ctx.send(
                f"<a:uncheck_ravena:1380884331534483629> La suggestion **#{suggestion_id}** n'existe pas."
            )
        
        # Mettre à jour le statut
        suggestion_data["status"] = status
        suggestion_data["reviewed_by"] = ctx.author.id
        suggestion_data["review_reason"] = reason
        suggestion_data["reviewed_at"] = datetime.datetime.now().isoformat()
        
        await self.save_suggestion_data(ctx.guild, suggestion_id, suggestion_data)
        
        # Récupérer le message de suggestion
        suggestions_channel_id = await self.config.guild(ctx.guild).suggestions_channel()
        suggestions_channel = ctx.guild.get_channel(suggestions_channel_id)
        
        if suggestions_channel:
            try:
                message = await suggestions_channel.fetch_message(suggestion_data["message_id"])
                embed = message.embeds[0]
                
                # Mettre à jour le statut dans l'embed
                status_emoji = "<a:check_ravena:1380884332708626493>" if status == "approved" else "<a:uncheck_ravena:1380884331534483629>"
                status_text = "Approuvée" if status == "approved" else "Rejetée"
                embed.color = 0x2ECC71 if status == "approved" else 0xE74C3C
                
                # Mettre à jour le champ statut
                for i, field in enumerate(embed.fields):
                    if "Statut" in field.name:
                        embed.set_field_at(i, name="<a:speechbubble:1380892653847314534> Statut", 
                                         value=f"{status_emoji} {status_text}", inline=True)
                        break
                
                # Ajouter le champ de révision
                embed.add_field(
                    name=f"<a:whitecrown:1380899677297315880> Révisé par",
                    value=f"{ctx.author.mention}",
                    inline=True
                )
                
                if reason:
                    embed.add_field(
                        name="<a:speechbubble:1380892653847314534> Raison",
                        value=reason,
                        inline=False
                    )
                
                await message.edit(embed=embed)
                
            except discord.NotFound:
                pass
        
        # Confirmation
        status_emoji = "<a:check_ravena:1380884332708626493>" if status == "approved" else "<a:uncheck_ravena:1380884331534483629>"
        status_text = "approuvée" if status == "approved" else "rejetée"
        
        await ctx.send(
            f"{status_emoji} La suggestion **#{suggestion_id}** a été **{status_text}** !"
        )

    @suggestions_settings.command(name="list")
    async def list_suggestions(self, ctx, status: str = "all"):
        """<a:speechbubble:1380892653847314534> Lister les suggestions (pending/approved/rejected/all)"""
        suggestions_data = await self.config.guild(ctx.guild).suggestions_data()
        
        if not suggestions_data:
            return await ctx.send("<a:Warning:1380884984595742790> Aucune suggestion n'a été soumise.")
        
        filtered_suggestions = []
        
        for suggestion_id, data in suggestions_data.items():
            if status == "all" or data.get("status", "pending") == status:
                filtered_suggestions.append((int(suggestion_id), data))
        
        if not filtered_suggestions:
            return await ctx.send(f"<a:Warning:1380884984595742790> Aucune suggestion avec le statut **{status}**.")
        
        # Trier par ID
        filtered_suggestions.sort(key=lambda x: x[0])
        
        # Créer l'embed
        embed = discord.Embed(
            title=f"<a:speechbubble:1380892653847314534> Suggestions - Statut: {status}",
            color=0x3498DB
        )
        
        description = ""
        for suggestion_id, data in filtered_suggestions[:10]:  # Limiter à 10
            status_emoji = {
                "pending": "<a:PinkLoading:1380886781062414356>",
                "approved": "<a:check_ravena:1380884332708626493>",
                "rejected": "<a:uncheck_ravena:1380884331534483629>"
            }.get(data.get("status", "pending"), "<a:PinkLoading:1380886781062414356>")
            
            author = ctx.guild.get_member(data["author_id"])
            author_name = author.display_name if author else "Utilisateur inconnu"
            
            description += f"{status_emoji} **#{suggestion_id}** - {data['title'][:50]}...\n"
            description += f"   *Par {author_name}*\n\n"
        
        embed.description = description
        embed.set_footer(text=f"Total: {len(filtered_suggestions)} suggestions")
        
        await ctx.send(embed=embed)

    @suggestions_settings.error
    async def suggestions_error(self, ctx, error):
        """Gestionnaire d'erreur pour les commandes de suggestions"""
        if isinstance(error, commands.CheckFailure):
            required_role_ids = [1381220960597839882, 1381222157929025626]
            required_roles = []
            
            for role_id in required_role_ids:
                role = ctx.guild.get_role(role_id)
                if role:
                    required_roles.append(role.mention)
                else:
                    required_roles.append(f"Rôle ID: {role_id}")
            
            roles_text = " ou ".join(required_roles) if required_roles else "Rôles requis introuvables"
            
            embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Accès refusé",
                description=f"Tu dois avoir l'un de ces rôles pour utiliser cette commande :\n{roles_text}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        suggestions_channel_id = await self.config.guild(ctx.guild).suggestions_channel()
        suggestions_channel = ctx.guild.get_channel(suggestions_channel_id)
        next_id = await self.config.guild(ctx.guild).next_suggestion_id()
        suggestions_data = await self.config.guild(ctx.guild).suggestions_data()
        
        embed = discord.Embed(
            title="<a:boost:1380882468621520916> Configuration Suggestions",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Canal de suggestions",
            value=suggestions_channel.mention if suggestions_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="<a:FallingPetals:1380882470060425267> Prochain ID",
            value=f"#{next_id}",
            inline=True
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Total suggestions",
            value=f"{len(suggestions_data)} suggestions",
            inline=True
        )
        
        # Compter par statut
        pending = sum(1 for data in suggestions_data.values() if data.get("status", "pending") == "pending")
        approved = sum(1 for data in suggestions_data.values() if data.get("status") == "approved")
        rejected = sum(1 for data in suggestions_data.values() if data.get("status") == "rejected")
        
        embed.add_field(
            name="<a:PinkLoading:1380886781062414356> En attente",
            value=f"{pending}",
            inline=True
        )
        
        embed.add_field(
            name="<a:check_ravena:1380884332708626493> Approuvées",
            value=f"{approved}",
            inline=True
        )
        
        embed.add_field(
            name="<a:uncheck_ravena:1380884331534483629> Rejetées",
            value=f"{rejected}",
            inline=True
        )
        
        # Afficher le rôle requis
        required_role_ids = [1381220960597839882, 1381222157929025626]
        required_roles = []
        
        for role_id in required_role_ids:
            role = ctx.guild.get_role(role_id)
            if role:
                required_roles.append(role.mention)
            else:
                required_roles.append(f"Rôle ID: {role_id}")
        
        roles_text = "\n".join(required_roles) if required_roles else "Rôles introuvables"
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> Rôles autorisés",
            value=roles_text,
            inline=False
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> Commandes disponibles",
            value=(
                "`!suggestions setup` - Configurer le message\n"
                "`!suggestions list [status]` - Lister les suggestions\n"
                "`!suggestions approve <ID>` - Approuver\n"
                "`!suggestions reject <ID>` - Rejeter"
            ),
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Système de suggestions")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))

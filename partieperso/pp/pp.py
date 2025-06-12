from redbot.core import commands
import discord
import asyncio
from discord.ui import Button, View, Modal, TextInput

class JoinVoiceButton(Button):
    def __init__(self, channel_id: int):
        super().__init__(
            style=discord.ButtonStyle.success,
            label="Rejoindre la préparation",
            emoji="<a:sound:1380899668434747463>"
        )
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.channel_id)
        if channel:
            try:
                await interaction.response.send_message(f"Clique sur le salon pour le rejoindre: {channel.mention}", ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message("Une erreur est survenue.", ephemeral=True)
        else:
            await interaction.response.send_message("Le salon vocal n'a pas été trouvé.", ephemeral=True)

class RankSelectionView(View):
    def __init__(self, cog, ctx, current_voice_channel, pp_type, base_color):
        super().__init__(timeout=60)
        self.cog = cog
        self.ctx = ctx
        self.current_voice_channel = current_voice_channel
        self.pp_type = pp_type
        self.base_color = base_color

    @discord.ui.button(label="Tous", style=discord.ButtonStyle.secondary, emoji="🌟")
    async def all_ranks_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Tous")

    @discord.ui.button(label="Iron", style=discord.ButtonStyle.secondary, emoji="<:Fer:1380653184246218924>")
    async def iron_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Iron")

    @discord.ui.button(label="Bronze", style=discord.ButtonStyle.secondary, emoji="<:Bronze:1380653187073052692>")
    async def bronze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Bronze")

    @discord.ui.button(label="Silver", style=discord.ButtonStyle.secondary, emoji="<:Argent:1380653207805497394>")
    async def silver_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Silver")

    @discord.ui.button(label="Gold", style=discord.ButtonStyle.secondary, emoji="<:Or:1380653189984161802>")
    async def gold_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Gold")

    @discord.ui.button(label="Platinum", style=discord.ButtonStyle.primary, emoji="<:Platine:1380653202957144264>", row=1)
    async def platinum_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Platinum")

    @discord.ui.button(label="Diamond", style=discord.ButtonStyle.primary, emoji="<:Diamant:1380653188478271638>", row=1)
    async def diamond_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Diamond")

    @discord.ui.button(label="Ascendant", style=discord.ButtonStyle.primary, emoji="<:Ascendant:1380653185663893586>", row=1)
    async def ascendant_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Ascendant")

    @discord.ui.button(label="Immortal", style=discord.ButtonStyle.danger, emoji="<:Immortel:1380653192525905980>", row=1)
    async def immortal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Immortal")

    @discord.ui.button(label="Radiant", style=discord.ButtonStyle.danger, emoji="<:Radiant:1380653206207467580>", row=1)
    async def radiant_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le rang.", ephemeral=True)
        
        await interaction.response.defer()
        await self.show_notification_selection(interaction, "Radiant")

    async def show_notification_selection(self, interaction, selected_rank):
        # Créer l'embed pour la sélection des notifications
        notif_embed = discord.Embed(
            title=f"<a:agooglebell:1380895257541083300> Qui veux-tu notifier pour ta PP {self.pp_type} ?",
            description=(
                "**<a:agooglebell:1380895257541083300> Notifs PP Générales** - Tous ceux qui ont activé les notifications PP\n"
                "**<a:WhiteBalisong:1380892882516443287> Seulement PP Tryhard** - Uniquement les fans de compétitif\n"
                "**<a:Lightblueheartgif:1380882450439471165> Seulement PP Chill** - Uniquement les joueurs détente\n"
                "**<a:boost:1380882468621520916> Les Deux Types** - PP Chill + PP Tryhard\n\n"
                "<a:PinkLoading:1380886781062414356> Tu as 60 secondes pour choisir."
            ),
            color=self.base_color
        )
        
        avatar_url = self.ctx.author.avatar.url if self.ctx.author.avatar else self.ctx.author.default_avatar.url
        notif_embed.set_thumbnail(url=avatar_url)
        notif_embed.set_footer(text=f"PP {self.pp_type} - Rang {selected_rank} - Sélection des notifications")
        
        # Créer la vue de sélection des notifications avec le rang sélectionné
        notif_view = NotificationSelectionView(self.cog, self.ctx, self.current_voice_channel, self.pp_type, self.base_color, selected_rank)
        
        # Modifier le message existant
        try:
            await interaction.edit_original_response(embed=notif_embed, view=notif_view)
            notif_view.message = await interaction.original_response()
        except:
            # Si l'édition échoue, créer un nouveau message
            notif_message = await interaction.followup.send(embed=notif_embed, view=notif_view)
            notif_view.message = notif_message

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        try:
            await self.message.edit(content="<a:PinkLoading:1380886781062414356> Temps écoulé pour la sélection du rang.", view=self)
        except:
            pass

class PartyCodeModal(Modal):
    def __init__(self, cog, ctx, current_voice_channel, pp_type, role_ids, color, selected_rank):
        super().__init__(title=f"Code de partie - PP {pp_type}")
        self.cog = cog
        self.ctx = ctx
        self.current_voice_channel = current_voice_channel
        self.pp_type = pp_type
        self.role_ids = role_ids  # Liste des IDs de rôles à ping
        self.color = color
        self.selected_rank = selected_rank

    party_code = TextInput(
        label="Code de partie Valorant",
        placeholder="Ex: SPIKE12",
        min_length=3,
        max_length=20,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Récupérer les canaux
        target_channel = self.cog.bot.get_channel(self.cog.pp_channel_id)
        org_channel = self.cog.bot.get_channel(self.cog.org_channel_id)
        
        if not target_channel:
            return await interaction.followup.send("<a:uncheck_ravena:1380884331534483629> Erreur de configuration du canal.", ephemeral=True)
        
        # Récupérer les rôles à ping
        roles_to_ping = []
        for role_id in self.role_ids:
            role = interaction.guild.get_role(role_id)
            if role:
                roles_to_ping.append(role)
        
        if not roles_to_ping:
            return await interaction.followup.send("<a:uncheck_ravena:1380884331534483629> Aucun rôle valide trouvé pour les notifications.", ephemeral=True)
        
        # Créer l'embed pour l'annonce PP
        embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Nouvelle PP",
            description=(
                "Mode → 5vs5\n"
                f"Type → {self.pp_type}\n"
                f"Ranks → {self.selected_rank}\n"
                "Map → Roulette\n"
                f"Staff → {self.ctx.author.mention} <a:whitecrown:1380899677297315880>"
            ),
            color=self.color
        )
        
        # Ajouter l'avatar de l'auteur
        avatar_url = self.ctx.author.avatar.url if self.ctx.author.avatar else self.ctx.author.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        
        # Ajouter le footer correspondant au salon vocal
        embed.set_footer(text=self.cog.prep_channels[self.current_voice_channel])
        
        # Créer le bouton et la vue pour rejoindre
        view = View(timeout=None)
        join_button = JoinVoiceButton(self.current_voice_channel)
        view.add_item(join_button)
        
        # Créer le contenu avec mentions des rôles
        role_mentions = " ".join([role.mention for role in roles_to_ping])
        
        # Envoyer le message dans le canal principal
        await target_channel.send(
            content=role_mentions,
            embed=embed,
            view=view,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )
        
        # Envoyer le message d'organisation si le canal existe
        if org_channel:
            voice_channel = interaction.guild.get_channel(self.current_voice_channel)
            voice_channel_name = voice_channel.name if voice_channel else "Salon inconnu"
            
            org_embed = discord.Embed(
                title="<a:PinkKey:1380899678622711808> Code de Partie",
                description=(
                    f"**<a:whitecrown:1380899677297315880> Organisateur:** {self.ctx.author.mention}\n"
                    f"**<a:sound:1380899668434747463> Salon:** {voice_channel_name}\n"
                    f"**<a:boost:1380882468621520916> Rang:** {self.selected_rank}\n"
                    f"**<a:PinkKey:1380899678622711808> Code:** `{self.party_code.value}`"
                ),
                color=self.color,
                timestamp=discord.utils.utcnow()
            )
            
            org_embed.set_footer(text="Radiant Order")
            
            await org_channel.send(embed=org_embed)
        
        # Confirmation
        notified_count = len(roles_to_ping)
        
        # Calculer le nombre total de personnes notifiées
        total_people_notified = 0
        for role in roles_to_ping:
            total_people_notified += len(role.members)
        
        await interaction.followup.send(
            f"<a:check_ravena:1380884332708626493> PP {self.pp_type} annoncée avec succès !\n"
            f"<a:boost:1380882468621520916> Rang requis: {self.selected_rank}\n"
            f"<a:PinkKey:1380899678622711808> Code de partie: `{self.party_code.value}`\n"
            f"<a:agooglebell:1380895257541083300> {notified_count} rôle(s) notifié(s)\n"
            f"<a:Animated_Arrow_Blue:1380888378953961472> {total_people_notified} personne(s) notifiée(s)", 
            ephemeral=True
        )

class NotificationSelectionView(View):
    def __init__(self, cog, ctx, current_voice_channel, pp_type, base_color, selected_rank):
        super().__init__(timeout=60)
        self.cog = cog
        self.ctx = ctx
        self.current_voice_channel = current_voice_channel
        self.pp_type = pp_type
        self.base_color = base_color
        self.selected_rank = selected_rank

    @discord.ui.button(label="🔔 Notifs PP Générales", style=discord.ButtonStyle.primary, emoji="<a:agooglebell:1380895257541083300>")
    async def notify_all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir les notifications.", ephemeral=True)
        
        # Notifier le rôle général notifications PP
        modal = PartyCodeModal(self.cog, self.ctx, self.current_voice_channel, self.pp_type, [1380616851427557406], self.base_color, self.selected_rank)
        await interaction.response.send_modal(modal)
        
        try:
            await interaction.delete_original_response()
        except:
            pass

    @discord.ui.button(label="Seulement PP Tryhard", style=discord.ButtonStyle.danger, emoji="<a:WhiteBalisong:1380892882516443287>")
    async def notify_tryhard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir les notifications.", ephemeral=True)
        
        # Notifier seulement les PP Tryhard
        modal = PartyCodeModal(self.cog, self.ctx, self.current_voice_channel, self.pp_type, [1380618268922089655], self.base_color, self.selected_rank)
        await interaction.response.send_modal(modal)
        
        try:
            await interaction.delete_original_response()
        except:
            pass

    @discord.ui.button(label="Seulement PP Chill", style=discord.ButtonStyle.success, emoji="<a:Lightblueheartgif:1380882450439471165>")
    async def notify_chill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir les notifications.", ephemeral=True)
        
        # Notifier seulement les PP Chill
        modal = PartyCodeModal(self.cog, self.ctx, self.current_voice_channel, self.pp_type, [1380618244976672788], self.base_color, self.selected_rank)
        await interaction.response.send_modal(modal)
        
        try:
            await interaction.delete_original_response()
        except:
            pass

    @discord.ui.button(label="Les Deux Types", style=discord.ButtonStyle.secondary, emoji="<a:boost:1380882468621520916>")
    async def notify_both_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir les notifications.", ephemeral=True)
        
        # Notifier les deux types (Chill + Tryhard)
        modal = PartyCodeModal(self.cog, self.ctx, self.current_voice_channel, self.pp_type, [1380618244976672788, 1380618268922089655], self.base_color, self.selected_rank)
        await interaction.response.send_modal(modal)
        
        try:
            await interaction.delete_original_response()
        except:
            pass

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        try:
            await self.message.edit(content="<a:PinkLoading:1380886781062414356> Temps écoulé pour la sélection des notifications.", view=self)
        except:
            pass

class PPTypeSelectionView(View):
    def __init__(self, cog, ctx, current_voice_channel):
        super().__init__(timeout=60)  # 60 secondes pour choisir
        self.cog = cog
        self.ctx = ctx
        self.current_voice_channel = current_voice_channel

    @discord.ui.button(label="PP Tryhard", style=discord.ButtonStyle.danger, emoji="<a:WhiteBalisong:1380892882516443287>")
    async def tryhard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le type de PP.", ephemeral=True)
        
        await interaction.response.defer()
        
        # Passer à la sélection du rang
        await self.show_rank_selection(interaction, "Tryhard", 0xE74C3C)

    @discord.ui.button(label="PP Chill", style=discord.ButtonStyle.success, emoji="<a:Lightblueheartgif:1380882450439471165>")
    async def chill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("<a:uncheck_ravena:1380884331534483629> Seul l'organisateur peut choisir le type de PP.", ephemeral=True)
        
        await interaction.response.defer()
        
        # Passer à la sélection du rang
        await self.show_rank_selection(interaction, "Chill", 0x3498DB)

    async def show_rank_selection(self, interaction, pp_type, color):
        # Créer l'embed pour la sélection du rang
        rank_embed = discord.Embed(
            title=f"<a:boost:1380882468621520916> Quel rang requis pour ta PP {pp_type} ?",
            description=(
                "**Sélectionne le rang minimum requis pour participer :**\n\n"
                "🌟 **Tous** - Ouvert à tous les rangs\n"
                "<:Fer:1380653184246218924> **Iron** - <:Bronze:1380653187073052692> **Bronze** - <:Argent:1380653207805497394> **Silver** - <:Or:1380653189984161802> **Gold**\n"
                "<:Platine:1380653202957144264> **Platinum** - <:Diamant:1380653188478271638> **Diamond** - <:Ascendant:1380653185663893586> **Ascendant** - <:Immortel:1380653192525905980> **Immortal** - <:Radiant:1380653206207467580> **Radiant**\n\n"
                "<a:PinkLoading:1380886781062414356> Tu as 60 secondes pour choisir."
            ),
            color=color
        )
        
        avatar_url = self.ctx.author.avatar.url if self.ctx.author.avatar else self.ctx.author.default_avatar.url
        rank_embed.set_thumbnail(url=avatar_url)
        rank_embed.set_footer(text=f"PP {pp_type} - Sélection du rang")
        
        # Créer la vue de sélection du rang
        rank_view = RankSelectionView(self.cog, self.ctx, self.current_voice_channel, pp_type, color)
        
        # Modifier le message existant
        try:
            await interaction.edit_original_response(embed=rank_embed, view=rank_view)
            rank_view.message = await interaction.original_response()
        except:
            # Si l'édition échoue, créer un nouveau message
            rank_message = await interaction.followup.send(embed=rank_embed, view=rank_view)
            rank_view.message = rank_message

    async def on_timeout(self):
        # Désactiver tous les boutons en cas de timeout
        for item in self.children:
            item.disabled = True
        
        try:
            await self.message.edit(content="<a:PinkLoading:1380886781062414356> Temps écoulé pour la sélection du type de PP.", view=self)
        except:
            pass

class PartiesPersonnalisees(commands.Cog):
    """Cog pour gérer les parties personnalisées"""

    def __init__(self, bot):
        self.bot = bot
        self.pp_channel_id = 1380560601004118036  # Channel principal des PP
        self.org_channel_id = 1380560611028635700  # Channel d'organisation
        self.pp_role_id = 1380615723692326992
        # Mapping des salons vocaux de préparation
        self.prep_channels = {
            1380560625654304829: "🔊 Préparation n°1",
            1380615433303883999: "🔊 Préparation n°2",
            1380615512161255425: "🔊 Préparation n°3",
            1380617021359915190: "🔊 Préparation n°4"
        }

    def has_required_role():
        async def predicate(ctx):
            # Liste des IDs des utilisateurs autorisés
            authorized_user_ids = [
                257152912776495104,  # Wicaebeth
                # Ajoutez ici les autres IDs d'utilisateurs autorisés
            ]
            
            # Vérifier si l'utilisateur est dans la liste des autorisés
            if ctx.author.id in authorized_user_ids:
                return True
            
            # Liste des IDs des rôles autorisés (rôles staff)
            authorized_role_ids = [
                1380562058461839400,  # Administrateur
                1380562966575059116,  # Responsables
                1380575934410915911,  # Assistants Responsable
                1380563626846322819,  # Modérateurs
                1380564333242613821,  # Helper
                1380574085708513340,  # Staff Interne
                1380574650689388695,  # Développeur
                1380575272511869060   # Amis
            ]
            
            # Vérifier si l'utilisateur a l'un des rôles autorisés
            for role_id in authorized_role_ids:
                role = ctx.guild.get_role(role_id)
                if role and role in ctx.author.roles:
                    return True
                    
            raise commands.CheckFailure("Tu n'as pas les rôles requis ou n'es pas autorisé à utiliser cette commande.")
            return False
        return commands.check(predicate)

    @commands.command(name="pp")
    @has_required_role()
    async def partie_personnalisee(self, ctx):
        """Annonce une partie personnalisée avec sélection du type, notifications et code de partie"""
        # Supprimer la commande de l'utilisateur
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass
        
        # Vérifier si l'utilisateur est dans un salon vocal
        if not ctx.author.voice or not ctx.author.voice.channel:
            error_msg = await ctx.send("<a:Warning:1380884984595742790> Tu dois être dans un salon vocal de préparation pour lancer une PP !")
            await asyncio.sleep(10)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            return

        # Vérifier si l'utilisateur est dans un salon de préparation valide
        current_voice_channel = ctx.author.voice.channel.id
        if current_voice_channel not in self.prep_channels:
            error_msg = await ctx.send("<a:Warning:1380884984595742790> Tu dois être dans un salon de préparation valide pour lancer une PP !")
            await asyncio.sleep(10)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            return
        
        # Vérifier si le canal cible existe
        target_channel = self.bot.get_channel(self.pp_channel_id)
        if not target_channel:
            error_msg = await ctx.send("<a:Warning:1380884984595742790> Le canal des parties personnalisées n'a pas été trouvé.")
            await asyncio.sleep(10)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            return
        
        # Créer l'embed de sélection du type
        selection_embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Quel type de PP veux-tu organiser ?",
            description=(
                "**<a:WhiteBalisong:1380892882516443287> PP Tryhard** - Pour les joueurs compétitifs qui veulent se donner à fond\n"
                "**<a:Lightblueheartgif:1380882450439471165> PP Chill** - Pour s'amuser et passer un bon moment détendu\n\n"
                "<a:PinkLoading:1380886781062414356> Tu as 60 secondes pour choisir.\n"
                "<a:speechbubble:1380892653847314534> Ensuite tu choisiras qui notifier et saisiras le code de partie."
            ),
            color=0x9B59B6
        )
        
        # Ajouter l'avatar de l'organisateur
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        selection_embed.set_thumbnail(url=avatar_url)
        selection_embed.set_footer(text=f"Organisateur: {ctx.author.display_name}")
        
        # Créer la vue de sélection
        view = PPTypeSelectionView(self, ctx, current_voice_channel)
        
        # Envoyer le message de sélection
        if ctx.channel.id != self.pp_channel_id:
            # Si pas dans le bon canal, envoyer la sélection dans le canal actuel
            selection_message = await ctx.send(embed=selection_embed, view=view)
        else:
            # Si dans le bon canal, envoyer directement
            selection_message = await ctx.send(embed=selection_embed, view=view)
        
        view.message = selection_message

    @partie_personnalisee.error
    async def partie_personnalisee_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            error_msg = await ctx.send("<a:uncheck_ravena:1380884331534483629> Tu n'es pas autorisé à utiliser cette commande.")
            await asyncio.sleep(5)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

async def setup(bot):
    await bot.add_cog(PartiesPersonnalisees(bot))

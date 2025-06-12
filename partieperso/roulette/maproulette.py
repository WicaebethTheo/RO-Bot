from redbot.core import commands
import discord
import asyncio
import random

class AcceptButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="Accepter la map", emoji="<a:check_ravena:1380884332708626493>", custom_id="accept_map")
        
    async def callback(self, interaction: discord.Interaction):
        view: MapVoteView = self.view
        await view.process_vote(interaction, True)

class RejectButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="Refuser la map", emoji="<a:uncheck_ravena:1380884331534483629>", custom_id="reject_map")
        
    async def callback(self, interaction: discord.Interaction):
        view: MapVoteView = self.view
        await view.process_vote(interaction, False)

class MapVoteView(discord.ui.View):
    def __init__(self, parent, map_choice, min_votes_required, timeout, author_name=None, author_avatar=None, guild_icon=None):
        super().__init__(timeout=timeout)
        self.parent = parent
        self.map_choice = map_choice
        self.min_votes_required = min_votes_required
        self.accept_voters = set()
        self.reject_voters = set()
        self.all_voters = set()  # Ensemble pour suivre tous les utilisateurs qui ont voté
        self.message = None
        self.ended = False
        self.author_name = author_name
        self.author_avatar = author_avatar
        self.guild_icon = guild_icon
        
        # Ajouter les boutons
        self.add_item(AcceptButton())
        self.add_item(RejectButton())
    
    async def process_vote(self, interaction: discord.Interaction, is_accept: bool):
        if self.ended:
            await interaction.response.send_message("Le vote est terminé.", ephemeral=True)
            return
            
        user_id = interaction.user.id
        
        # Vérifier si l'utilisateur a déjà voté
        if user_id in self.all_voters:
            await interaction.response.send_message("Vous avez déjà voté et ne pouvez pas changer votre vote.", ephemeral=True)
            return
        
        # Enregistrer le vote
        self.all_voters.add(user_id)
        
        if is_accept:
            self.accept_voters.add(user_id)
        else:
            self.reject_voters.add(user_id)
        
        # Mettre à jour l'affichage
        accept_count = len(self.accept_voters)
        reject_count = len(self.reject_voters)
        
        embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Roulette MAP",
            description=(
                f"MAP → {self.map_choice['name']}\n\n"
                f"<a:check_ravena:1380884332708626493> Accepter cette map: **{accept_count}** votes\n"
                f"<a:uncheck_ravena:1380884331534483629> Refuser et relancer: **{reject_count}** votes\n\n"
                f"Minimum {self.min_votes_required} votes nécessaires pour accepter ou refuser.\n\n"
                f"<a:Warning:1380884984595742790> Attention: Vous ne pouvez voter qu'une seule fois!"
            ),
            color=0x00B0F4
        )
        embed.set_image(url=self.map_choice['image'])
        remaining = max(0, (self.timeout - (asyncio.get_event_loop().time() - self.start_time)))
        
        # Conserver le design original avec l'auteur et l'icône du serveur
        if self.author_name and self.author_avatar:
            embed.set_footer(text=f"Temps restant: {int(remaining)} secondes | Roulette lancée par {self.author_name}", icon_url=self.author_avatar)
        else:
            embed.set_footer(text=f"Temps restant: {int(remaining)} secondes")
        
        if self.guild_icon:
            embed.set_thumbnail(url=self.guild_icon)
        
        await interaction.response.defer(ephemeral=True)
        
        # Message de confirmation avec le choix fait
        vote_type = "ACCEPTER" if is_accept else "REFUSER"
        await interaction.followup.send(f"Votre vote pour {vote_type} la map a été enregistré! Vous ne pouvez plus changer votre vote.", ephemeral=True)
        
        # Mettre à jour le message
        await self.message.edit(embed=embed)
        
        # Vérifier si on a atteint le seuil de votes
        if accept_count >= self.min_votes_required or reject_count >= self.min_votes_required:
            self.ended = True
            self.stop()
            
            # Gérer la fin du vote directement ici
            if accept_count >= self.min_votes_required:
                # La map est acceptée
                result_embed = discord.Embed(
                    title="<a:FallingPetals:1380882470060425267> Roulette MAP",
                    description=(
                        f"MAP → {self.map_choice['name']}\n\n"
                        f"**MAP ACCEPTÉE** avec {accept_count} votes pour et {reject_count} votes contre."
                    ),
                    color=0x2ECC71  # Vert
                )
                result_embed.set_image(url=self.map_choice['image'])
                # Utiliser None à la place de la vue pour désactiver les boutons
                await self.message.edit(embed=result_embed, view=None)
                
            elif reject_count >= self.min_votes_required:
                # La map est refusée, relancer la roulette
                result_embed = discord.Embed(
                    title="<a:FallingPetals:1380882470060425267> Roulette MAP",
                    description=(
                        f"MAP → {self.map_choice['name']}\n\n"
                        f"**MAP REFUSÉE** avec {reject_count} votes contre et {accept_count} votes pour.\n\n"
                        f"Relance de la roulette..."
                    ),
                    color=0xE74C3C  # Rouge
                )
                result_embed.set_image(url=self.map_choice['image'])
                # Utiliser None à la place de la vue pour désactiver les boutons
                await self.message.edit(embed=result_embed, view=None)
                await asyncio.sleep(3)  # Pause dramatique
                await self.message.delete()
                
                # Relancer la roulette
                try:
                    await self.parent.roulette(self.parent.last_context)
                except Exception as e:
                    error_embed = discord.Embed(
                        title="❌ Erreur",
                        description="Une erreur s'est produite lors de la relance de la roulette.",
                        color=0xFF0000
                    )
                    await self.parent.last_context.send(embed=error_embed)
                    print(f"Erreur lors de la relance de la roulette: {e}")
    
    async def on_timeout(self):
        self.ended = True
        # S'assurer que les boutons sont désactivés après le timeout
        try:
            if self.message:
                # Récupérer le dernier embed
                current_embed = self.message.embeds[0]
                # Mettre à jour le footer pour indiquer que le temps est écoulé, mais conserver l'auteur
                if self.author_name and self.author_avatar:
                    current_embed.set_footer(text=f"Temps écoulé! Le vote est terminé. | Roulette lancée par {self.author_name}", icon_url=self.author_avatar)
                else:
                    current_embed.set_footer(text="Temps écoulé! Le vote est terminé.")
                # Désactiver les boutons en mettant view=None
                await self.message.edit(embed=current_embed, view=None)
        except Exception as e:
            print(f"Erreur lors de la désactivation des boutons après timeout: {e}")
    
    async def start(self, channel):
        embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Roulette MAP",
            description=(
                f"MAP → {self.map_choice['name']}\n\n"
                f"<a:check_ravena:1380884332708626493> Accepter cette map: **0** votes\n"
                f"<a:uncheck_ravena:1380884331534483629> Refuser et relancer: **0** votes\n\n"
                f"Minimum {self.min_votes_required} votes nécessaires pour accepter ou refuser.\n\n"
                f"<a:Warning:1380884984595742790> Attention: Vous ne pouvez voter qu'une seule fois!"
            ),
            color=0x00B0F4
        )
        embed.set_image(url=self.map_choice['image'])
        
        # Appliquer le design cohérent dès le début
        if self.author_name and self.author_avatar:
            embed.set_footer(text=f"Temps restant: {int(self.timeout)} secondes | Roulette lancée par {self.author_name}", icon_url=self.author_avatar)
        else:
            embed.set_footer(text=f"Temps restant: {int(self.timeout)} secondes")
        
        if self.guild_icon:
            embed.set_thumbnail(url=self.guild_icon)
        
        self.message = await channel.send(embed=embed, view=self)
        self.start_time = asyncio.get_event_loop().time()
        return self.message

class MapRoulette(commands.Cog):
    """Cog pour la roulette de maps Valorant"""

    def __init__(self, bot):
        self.bot = bot
        self.roulette_channel_id = 1380560607383912511
        self.maps = [
            {"name": "ASCENT", "image": "https://beebom.com/wp-content/uploads/2023/09/Ascent-Valorant-Cover.jpg"},
            {"name": "BIND", "image": "https://static.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png"},
            {"name": "BREEZE", "image": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/b79528c1c15525072a138c2648be78a4b7fa3fd9-1920x1080.jpg?auto=format&fit=fill&q=80&w=956"},
            {"name": "FRACTURE", "image": "https://static.wikia.nocookie.net/valorant/images/f/fc/Loading_Screen_Fracture.png"},
            {"name": "HAVEN", "image": "https://files.bo3.gg/uploads/image/64582/image/webp-aaaa475629b10d73cbe5de879e7033c2.webp"},
            {"name": "ICEBOX", "image": "https://www.mandatory.gg/wp-content/uploads/mandatory-news-valorant-retrait-icebox-avril-2023.jpg"},
            {"name": "LOTUS", "image": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/df5c6e7629733f801b7059f7d0ed8d286cbdbc1e-1920x1080.jpg?auto=format&fit=fill&q=80&w=956"},
            {"name": "PEARL", "image": "https://www.pcgamesn.com/wp-content/sites/pcgamesn/2022/09/valorant-map-pearl-players-divided.jpg"},
            {"name": "SPLIT", "image": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/fe3ff195d072643e1cc1e07801152d2e2ab96cd6-1920x1080.jpg"},
            {"name": "SUNSET", "image": "https://cdn.ome.lt/C8HZ7SYxtIeBVR8RAcn5tTtfhc8=/970x360/smart/uploads/conteudo/fotos/sunset-valorant-novo-mapa.jpg"},
            {"name": "ABYSS", "image": "https://static.wikia.nocookie.net/valorant/images/6/61/Loading_Screen_Abyss.png"}
        ]
        self.loading_emojis = ["<a:PinkLoading:1380886781062414356>", "<a:PinkLoading:1380886781062414356>", "<a:PinkLoading:1380886781062414356>"]
        self.min_votes_required = 6
        self.vote_timeout = 60.0  # secondes
        self.current_map = None
        self.last_context = None

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

    @commands.command(name="roulette")
    @has_required_role()
    async def roulette(self, ctx):
        """Choisit aléatoirement une map avec système de vote en groupe"""
        # Sauvegarder le contexte pour la relance
        self.last_context = ctx
        
        # Supprimer la commande de l'utilisateur
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

        # Vérifier si la commande est utilisée dans le bon canal
        target_channel = self.bot.get_channel(self.roulette_channel_id)
        if not target_channel:
            error_msg = await ctx.send("<a:Warning:1380884984595742790> Le canal de la roulette n'a pas été trouvé.")
            await asyncio.sleep(10)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            return
        
        # Récupérer le nom d'affichage de l'auteur et le logo du serveur
        author_name = ctx.author.display_name
        author_avatar = ctx.author.display_avatar.url
        guild_icon = ctx.guild.icon.url if ctx.guild.icon else None
        
        # Créer l'embed de chargement initial
        loading_embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Roulette MAP",
            description="Tirage de la map en cours...",
            color=0x00B0F4
        )
        loading_embed.set_image(url="https://i.imgur.com/jhEvEJJ.gif")
        loading_embed.set_footer(text=f"Roulette lancée par {author_name}", icon_url=author_avatar)
        if guild_icon:
            loading_embed.set_thumbnail(url=guild_icon)
        
        # Envoyer le message initial dans le canal cible
        loading_message = await target_channel.send(content=ctx.author.mention, embed=loading_embed)
        
        # Si la commande n'a pas été utilisée dans le bon canal, envoyer une confirmation
        if ctx.channel.id != self.roulette_channel_id:
            confirm_msg = await ctx.send("<a:check_ravena:1380884332708626493> Roulette lancée dans le canal approprié !")
            await asyncio.sleep(5)
            try:
                await confirm_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
        
        # Animation avancée avec les cartes qui défilent
        animation_steps = [
            {"text": "<a:PinkLoading:1380886781062414356> Recherche des maps disponibles...", "color": 0x3498DB},
            {"text": "<a:PinkLoading:1380886781062414356> Mélange des maps...", "color": 0x9B59B6},
            {"text": "<a:PinkLoading:1380886781062414356> Tirage au sort...", "color": 0xE91E63},
            {"text": "<a:PinkLoading:1380886781062414356> Analyse des statistiques...", "color": 0x2ECC71},
            {"text": "<a:PinkLoading:1380886781062414356> Préparation du résultat...", "color": 0xF1C40F},
        ]
        
        # Afficher les maps qui "défilent" pendant l'animation
        random_maps = random.sample(self.maps, min(6, len(self.maps)))
        
        for i, step in enumerate(animation_steps):
            loading_embed.description = step["text"]
            loading_embed.color = step["color"]
            
            # Changer l'image pour montrer différentes maps pendant le "défilement"
            if i < len(random_maps):
                loading_embed.set_image(url=random_maps[i]["image"])
                loading_embed.set_footer(text=f"Sélection en cours... | Lancée par {author_name}", icon_url=author_avatar)
            
            await loading_message.edit(embed=loading_embed)
            await asyncio.sleep(1.2)  # Durée légèrement plus longue pour avoir le temps de voir l'image
        
        # Effet de "ralentissement" sur les dernières maps
        slowing_maps = random.sample(self.maps, 3)  # Prendre 3 maps au hasard 
        
        for i, map_data in enumerate(slowing_maps):
            loading_embed.description = "<a:PinkLoading:1380886781062414356> Finalisation du choix..."
            loading_embed.color = 0xFF9500
            loading_embed.set_image(url=map_data["image"])
            loading_embed.set_footer(text=f"Presque terminé... | Lancée par {author_name}", icon_url=author_avatar)
            
            await loading_message.edit(embed=loading_embed)
            # Augmenter progressivement le délai pour l'effet de ralentissement
            await asyncio.sleep(0.8 + (i * 0.4))
        
        # Choisir une map aléatoire pour le résultat final
        map_choice = random.choice(self.maps)
        self.current_map = map_choice  # Sauvegarder la map actuelle
        
        # Supprimer le message d'animation (sans la fenêtre de compte à rebours)
        await loading_message.delete()
        
        # Créer et démarrer la vue de vote
        vote_view = MapVoteView(self, map_choice, self.min_votes_required, self.vote_timeout, author_name, author_avatar, guild_icon)
        vote_message = await vote_view.start(target_channel)
        
        # Attendre que le vote soit terminé
        try:
            await asyncio.wait_for(vote_view.wait(), timeout=self.vote_timeout + 1)
        except asyncio.TimeoutError:
            # En cas de timeout, s'assurer que le vote est marqué comme terminé
            vote_view.ended = True
            # Gérer le timeout manuellement
            accept_count = len(vote_view.accept_voters)
            reject_count = len(vote_view.reject_voters)
            
            # Pas assez de votes, garder la map par défaut
            result_embed = discord.Embed(
                title="<a:FallingPetals:1380882470060425267> Roulette MAP",
                description=(
                    f"MAP → {map_choice['name']}\n\n"
                    f"<a:Warning:1380884984595742790> **TEMPS ÉCOULÉ**\n"
                    f"Votes: {accept_count} pour, {reject_count} contre.\n"
                    f"Pas assez de votes ({self.min_votes_required} nécessaires), la map est gardée par défaut."
                ),
                color=0xF1C40F  # Jaune
            )
            result_embed.set_image(url=map_choice['image'])
            result_embed.set_footer(text=f"Roulette lancée par {author_name}", icon_url=author_avatar)
            if guild_icon:
                result_embed.set_thumbnail(url=guild_icon)
            # Utiliser None à la place de la vue pour désactiver les boutons
            await vote_message.edit(embed=result_embed, view=None)

    @roulette.error
    async def roulette_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            error_msg = await ctx.send("❌ Tu n'as pas le rôle requis pour utiliser cette commande.")
            await asyncio.sleep(5)
            try:
                await error_msg.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

    async def handle_vote_end(self, accept_count: int, reject_count: int):
        """Gère la fin du vote et détermine l'action à prendre"""
        # Cette méthode n'est plus nécessaire car la logique est maintenant dans process_vote
        # Mais on la garde pour éviter les erreurs
        pass

async def setup(bot):
    await bot.add_cog(MapRoulette(bot))

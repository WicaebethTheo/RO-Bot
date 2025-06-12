import discord
from redbot.core import commands, Config
import asyncio

class DisponibiliteView(discord.ui.View):
    """Vue avec boutons pour les disponibilités"""
    
    def __init__(self, bot):
        super().__init__(timeout=None)  # Pas de timeout pour que les boutons restent actifs
        self.responses = {}
        self.bot = bot
        self.message = None  # Référence au message pour le mettre à jour
    
    def update_embed(self):
        """Met à jour l'embed avec les statistiques"""
        if not self.message:
            return None
            
        # Compter les disponibilités par jour
        stats = {"Mercredi": [], "Jeudi": [], "Vendredi": []}
        
        for user_id, data in self.responses.items():
            for jour in data["jours"]:
                if jour in stats:
                    stats[jour].append(data["nom"])
        
        # Créer l'embed mis à jour
        embed = discord.Embed(
            title="<a:Anouncements_Animated:1380895055694528542> **Réunion Communautaire** <a:Anouncements_Animated:1380895055694528542>",
            description="<a:agooglebell:1380895257541083300> **Salutations, chers membres de notre communauté !** <a:agooglebell:1380895257541083300>",
            color=0x7289DA
        )
        
        embed.add_field(
            name="<a:speechbubble:1380892653847314534> **Objet de la réunion**",
            value=(
                "Nous organisons une réunion pour discuter de **l'avenir de notre communauté** "
                "et définir les **rôles de chacun** dans cette belle aventure collective."
            ),
            inline=False
        )
        
        embed.add_field(
            name="<a:Animated_Arrow_Blue:1380888378953961472> **Vos disponibilités**",
            value=(
                "Cliquez sur les boutons ci-dessous pour indiquer vos disponibilités :\n\n"
                "<a:check_ravena:1380884332708626493> **Mercredi**\n"
                "<a:check_ravena:1380884332708626493> **Jeudi**\n"
                "<a:check_ravena:1380884332708626493> **Vendredi**"
            ),
            inline=False
        )
        
        # Ajouter les statistiques
        stats_text = ""
        for jour, personnes in stats.items():
            count = len(personnes)
            if count > 0:
                personnes_str = ", ".join(personnes[:5])  # Limite à 5 noms
                if count > 5:
                    personnes_str += f" (+{count-5} autres)"
                stats_text += f"**{jour}** : {count} personne(s)\n└ {personnes_str}\n\n"
            else:
                stats_text += f"**{jour}** : 0 personne\n\n"
        
        embed.add_field(
            name="<a:maruloader:1380888045259329569> **Disponibilités actuelles**",
            value=stats_text or "Aucune réponse pour le moment",
            inline=False
        )
        
        embed.add_field(
            name="<a:whitecrown:1380899677297315880> **Votre participation compte**",
            value="Votre présence et vos idées sont précieuses pour façonner notre avenir ensemble !",
            inline=False
        )
        
        embed.set_footer(
            text="Des bisous, l'équipe"
        )
        
        # Ajouter les émojis cœurs à la fin
        embed.add_field(
            name="",
            value="<a:Lightblueheartgif:1380882450439471165> <a:Lightpinkgothheartgif:1380882449126527037> <a:Whitegothheartgif:1380882447507390474>",
            inline=False
        )
        
        return embed
    
    async def update_message(self):
        """Met à jour le message avec les nouvelles statistiques"""
        if self.message:
            try:
                embed = self.update_embed()
                if embed:
                    await self.message.edit(embed=embed, view=self)
            except:
                pass  # Ignore les erreurs de mise à jour
    
    @discord.ui.button(
        label="Mercredi", 
        emoji="<a:check_ravena:1380884332708626493>",
        style=discord.ButtonStyle.success,
        custom_id="mercredi"
    )
    async def mercredi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id not in self.responses:
            self.responses[user_id] = {"nom": interaction.user.display_name, "jours": []}
        
        if "Mercredi" in self.responses[user_id]["jours"]:
            self.responses[user_id]["jours"].remove("Mercredi")
            await interaction.response.send_message(
                f"<a:uncheck_ravena:1380884331534483629> Tu as retiré ta disponibilité pour **Mercredi**", 
                ephemeral=True
            )
        else:
            self.responses[user_id]["jours"].append("Mercredi")
            await interaction.response.send_message(
                f"<a:check_ravena:1380884332708626493> Tu es maintenant disponible pour **Mercredi** !", 
                ephemeral=True
            )
        
        # Mettre à jour le message
        await self.update_message()
    
    @discord.ui.button(
        label="Jeudi", 
        emoji="<a:check_ravena:1380884332708626493>",
        style=discord.ButtonStyle.primary,
        custom_id="jeudi"
    )
    async def jeudi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id not in self.responses:
            self.responses[user_id] = {"nom": interaction.user.display_name, "jours": []}
        
        if "Jeudi" in self.responses[user_id]["jours"]:
            self.responses[user_id]["jours"].remove("Jeudi")
            await interaction.response.send_message(
                f"<a:uncheck_ravena:1380884331534483629> Tu as retiré ta disponibilité pour **Jeudi**", 
                ephemeral=True
            )
        else:
            self.responses[user_id]["jours"].append("Jeudi")
            await interaction.response.send_message(
                f"<a:check_ravena:1380884332708626493> Tu es maintenant disponible pour **Jeudi** !", 
                ephemeral=True
            )
        
        # Mettre à jour le message
        await self.update_message()
    
    @discord.ui.button(
        label="Vendredi", 
        emoji="<a:check_ravena:1380884332708626493>",
        style=discord.ButtonStyle.secondary,
        custom_id="vendredi"
    )
    async def vendredi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id not in self.responses:
            self.responses[user_id] = {"nom": interaction.user.display_name, "jours": []}
        
        if "Vendredi" in self.responses[user_id]["jours"]:
            self.responses[user_id]["jours"].remove("Vendredi")
            await interaction.response.send_message(
                f"<a:uncheck_ravena:1380884331534483629> Tu as retiré ta disponibilité pour **Vendredi**", 
                ephemeral=True
            )
        else:
            self.responses[user_id]["jours"].append("Vendredi")
            await interaction.response.send_message(
                f"<a:check_ravena:1380884332708626493> Tu es maintenant disponible pour **Vendredi** !", 
                ephemeral=True
            )
        
        # Mettre à jour le message
        await self.update_message()

class Annonce(commands.Cog):
    """Cog pour envoyer des annonces élégantes avec boutons interactifs"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.active_polls = {}  # Stockage des sondages actifs
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reunion(self, ctx, channel_id: int = None):
        """Envoie une annonce élégante pour la réunion communautaire avec boutons et comptage
        
        Usage: [p]reunion [channel_id]
        Si aucun channel_id n'est fourni, utilise le canal actuel
        """
        
        # Utiliser le canal spécifié ou le canal actuel
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send(f"❌ Canal avec l'ID {channel_id} introuvable")
                return
        else:
            channel = ctx.channel
        
        try:
            # Créer la vue avec les boutons
            view = DisponibiliteView(self.bot)
            
            # Message élégant avec embed et émojis animés
            embed = view.update_embed()
            
            # Envoyer le message avec les boutons
            message = await channel.send(embed=embed, view=view)
            
            # Associer le message à la vue pour les mises à jour
            view.message = message
            
            # Stocker le sondage actif
            self.active_polls[message.id] = view
            
            # Confirmation
            if channel != ctx.channel:
                await ctx.send(f"✅ Annonce avec comptage envoyée dans {channel.mention} avec succès !")
            else:
                # Si c'est dans le même canal, on supprime la commande pour garder propre
                try:
                    await ctx.message.delete()
                except:
                    pass
                    
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'envoi de l'annonce : {e}")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reunion_stats(self, ctx, message_id: int = None):
        """Affiche les statistiques détaillées d'un sondage de réunion
        
        Usage: [p]reunion_stats [message_id]
        Si aucun message_id, affiche les sondages actifs
        """
        
        if not message_id:
            # Afficher la liste des sondages actifs
            if not self.active_polls:
                await ctx.send("❌ Aucun sondage de réunion actif")
                return
            
            embed = discord.Embed(
                title="<a:maruloader:1380888045259329569> **Sondages Actifs**",
                color=0x7289DA
            )
            
            for msg_id, view in self.active_polls.items():
                total_votes = len(view.responses)
                embed.add_field(
                    name=f"Message ID: {msg_id}",
                    value=f"**{total_votes}** personne(s) ont voté",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            return
        
        # Afficher les stats d'un sondage spécifique
        if message_id not in self.active_polls:
            await ctx.send(f"❌ Aucun sondage actif trouvé avec l'ID {message_id}")
            return
        
        view = self.active_polls[message_id]
        
        # Compter les disponibilités par jour
        stats = {"Mercredi": [], "Jeudi": [], "Vendredi": []}
        
        for user_id, data in view.responses.items():
            for jour in data["jours"]:
                if jour in stats:
                    stats[jour].append(data["nom"])
        
        embed = discord.Embed(
            title="<a:PinkLoading:1380886781062414356> **Statistiques Détaillées**",
            color=0x7289DA
        )
        
        for jour, personnes in stats.items():
            count = len(personnes)
            if count > 0:
                personnes_list = "\n".join([f"• {nom}" for nom in personnes])
                embed.add_field(
                    name=f"**{jour}** ({count} personne(s))",
                    value=personnes_list,
                    inline=True
                )
            else:
                embed.add_field(
                    name=f"**{jour}** (0 personne)",
                    value="*Aucune disponibilité*",
                    inline=True
                )
        
        # Ajouter le jour le plus populaire
        max_jour = max(stats.keys(), key=lambda x: len(stats[x]))
        max_count = len(stats[max_jour])
        
        if max_count > 0:
            embed.add_field(
                name="<a:whitecrown:1380899677297315880> **Jour le plus populaire**",
                value=f"**{max_jour}** avec **{max_count}** personne(s)",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reunion_simple(self, ctx, channel_id: int = None):
        """Version simple de l'annonce sans embed mais avec émojis animés et boutons
        
        Usage: [p]reunion_simple [channel_id]
        """
        
        # Utiliser le canal spécifié ou le canal actuel
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send(f"❌ Canal avec l'ID {channel_id} introuvable")
                return
        else:
            channel = ctx.channel
        
        message_text = f"""
<a:Anouncements_Animated:1380895055694528542> **RÉUNION COMMUNAUTAIRE** <a:Anouncements_Animated:1380895055694528542>

<a:agooglebell:1380895257541083300> **Salutations, chers membres de notre communauté !** <a:agooglebell:1380895257541083300>

<a:speechbubble:1380892653847314534> J'aimerais que nous nous réunissions pour parler de **l'avenir** de notre communauté et des **rôles de chacun** dans cette belle aventure collective.

<a:Animated_Arrow_Blue:1380888378953961472> **Cliquez sur les boutons ci-dessous** pour indiquer vos disponibilités :

<a:whitecrown:1380899677297315880> Votre participation compte énormément pour façonner notre avenir ensemble !

*Des bisous, l'équipe* <a:Lightblueheartgif:1380882450439471165> <a:Lightpinkgothheartgif:1380882449126527037> <a:Whitegothheartgif:1380882447507390474>
"""
        
        try:
            # Créer la vue avec les boutons (sans mise à jour automatique pour la version simple)
            view = DisponibiliteView(self.bot)
            
            # Envoyer le message avec les boutons
            message = await channel.send(message_text, view=view)
            
            # Confirmation
            if channel != ctx.channel:
                await ctx.send(f"✅ Annonce simple avec boutons envoyée dans {channel.mention} avec succès !")
            else:
                try:
                    await ctx.message.delete()
                except:
                    pass
                    
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'envoi de l'annonce : {e}")

async def setup(bot):
    """Fonction requise pour charger le cog dans RedBot"""
    await bot.add_cog(Annonce(bot))

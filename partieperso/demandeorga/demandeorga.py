import discord
from redbot.core import commands, Config
import asyncio
from datetime import datetime, timedelta

class DemandeOrgaButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label="Appeler les helpers",
            emoji="<a:agooglebell:1380895257541083300>",
            custom_id="demande_orga_button"
        )
        
    async def callback(self, interaction: discord.Interaction):
        # IDs des salons de préparation autorisés
        preparation_channels = [
            1380560625654304829,  # 🎤 〔🎮〕Préparation 1
            1380615433303883999,  # 🎤 〔🎮〕Préparation 2
            1380615512161255425,  # 🎤 〔🎮〕Préparation 3
            1380617021359915190   # 🎤 〔🎮〕Préparation 4
        ]
        
        # IDs des rôles privilégiés (peuvent utiliser sans limitation)
        privileged_roles = [
            1380562058461839400,  # Administrateur
            1380562966575059116,  # Responsables
            1380575934410915911,  # Assistants Responsable
            1380563626846322819,  # Modérateurs
            1380564333242613821   # Helper
        ]
        
        # Vérifier si l'utilisateur a un rôle privilégié
        has_privileged_role = False
        for role_id in privileged_roles:
            role = interaction.guild.get_role(role_id)
            if role and role in interaction.user.roles:
                has_privileged_role = True
                break
        
        # Vérifier si l'utilisateur est dans un salon vocal de préparation
        user_voice_channel = None
        if interaction.user.voice and interaction.user.voice.channel:
            user_voice_channel = interaction.user.voice.channel.id
        
        if user_voice_channel not in preparation_channels:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Accès refusé",
                description="Vous devez être dans un salon de préparation pour demander de l'aide !",
                color=0xFF0000
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        # ID du rôle Helper
        helper_role_id = 1380564333242613821
        helper_role = interaction.guild.get_role(helper_role_id)
        
        if not helper_role:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur",
                description="Le rôle Helper n'a pas été trouvé.",
                color=0xFF0000
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        # Trouver les helpers en ligne
        online_helpers = []
        for member in helper_role.members:
            if member.status != discord.Status.offline:
                online_helpers.append(member)
        
        # Obtenir le nom du salon vocal
        voice_channel = interaction.guild.get_channel(user_voice_channel)
        voice_channel_name = voice_channel.name if voice_channel else "Salon inconnu"
        
        if online_helpers:
            # Créer la liste des mentions
            helper_mentions = " ".join([helper.mention for helper in online_helpers])
            
            # Message différent selon le statut de l'utilisateur
            limitation_text = ""
            if has_privileged_role:
                limitation_text = "<a:whitecrown:1380899677297315880> *(Vous avez un rôle privilégié - aucune limitation d'utilisation)*"
            else:
                limitation_text = "**Note :** Ce bouton ne peut être utilisé que toutes les 10 minutes pour éviter le spam.\n<a:whitecrown:1380899677297315880> *(Certains rôles privilégiés peuvent l'utiliser sans limitation)*"
            
            # Embed pour la demande d'aide
            request_embed = discord.Embed(
                title="<a:agooglebell:1380895257541083300> Assistance Helpers",
                description=f"**{interaction.user.display_name}** a besoin d'assistance dans **{voice_channel_name}** !\n\n"
                           f"<a:whitecrown:1380899677297315880> **Demandeur :** {interaction.user.mention}\n"
                           f"<a:sound:1380899668434747463> **Salon :** {voice_channel_name}\n"
                           f"<a:boost:1380882468621520916> **Helpers en ligne :** {len(online_helpers)}\n\n"
                           f"{limitation_text}",
                color=0x00B0F4,
                timestamp=datetime.now()
            )
            request_embed.set_footer(text="Demande d'assistance", icon_url=interaction.user.display_avatar.url)
            
            # Envoyer la demande
            await interaction.response.send_message(
                content=f"{helper_mentions}",
                embed=request_embed
            )
            
            # Message de confirmation pour l'utilisateur
            confirmation_text = f"Les helpers en ligne ({len(online_helpers)}) ont été notifiés de votre demande d'assistance."
            if has_privileged_role:
                confirmation_text += f"\n<a:whitecrown:1380899677297315880> **Statut privilégié** : Vous pouvez utiliser ce bouton sans limitation."
            
            success_embed = discord.Embed(
                title="<a:check_ravena:1380884332708626493> Demande envoyée !",
                description=confirmation_text,
                color=0x00FF00
            )
            await interaction.followup.send(embed=success_embed, ephemeral=True)
            
        else:
            # Aucun helper en ligne
            no_helper_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Aucun helper disponible",
                description="Aucun helper n'est actuellement en ligne. Veuillez réessayer plus tard.",
                color=0xFFA500
            )
            await interaction.response.send_message(embed=no_helper_embed, ephemeral=True)

class DemandeOrgaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DemandeOrgaButton())

class DemandeOrga(commands.Cog):
    """<a:agooglebell:1380895257541083300> Système de demande d'assistance pour l'organisation"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=234567890)
        default_guild = {
            "demande_channel_id": 1380560617676603402,
            "message_id": None
        }
        self.config.register_guild(**default_guild)

    async def cog_load(self):
        """Ajouter la vue persistante au bot"""
        try:
            self.bot.add_view(DemandeOrgaView())
            print("DemandeOrga: Vue persistante ajoutée avec succès")
        except Exception as e:
            print(f"DemandeOrga: Erreur lors de l'ajout de la vue persistante: {e}")

    @commands.command(name="setup_demande")
    @commands.has_permissions(manage_guild=True)
    async def setup_demande_orga(self, ctx):
        """Configurer le système de demande d'assistance"""
        
        # Récupérer le canal cible depuis la config
        demande_channel_id = await self.config.guild(ctx.guild).demande_channel_id()
        target_channel = self.bot.get_channel(demande_channel_id)
        
        if not target_channel:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Le canal de demande d'orga n'a pas été trouvé.")
        
        # Supprimer l'ancien message s'il existe
        old_message_id = await self.config.guild(ctx.guild).message_id()
        if old_message_id:
            try:
                old_message = await target_channel.fetch_message(old_message_id)
                await old_message.delete()
            except (discord.NotFound, discord.HTTPException):
                pass
        
        # Créer l'embed principal
        main_embed = discord.Embed(
            title="<a:agooglebell:1380895257541083300> Assistance Helpers",
            description="**Besoin d'aide pour organiser une partie ou un événement ?**\n\n"
                       "Utilisez le bouton ci-dessous pour appeler les helpers actuellement en ligne.\n\n"
                       "<a:Warning:1380884984595742790> **Note :** Ce bouton ne peut être utilisé que toutes les 10 minutes pour éviter le spam.\n"
                       "<a:whitecrown:1380899677297315880> *(Les rôles staff peuvent l'utiliser sans limitation)*\n\n"
                       "<a:boost:1380882468621520916> Les helpers en ligne seront mentionnés",
            color=0x00B0F4
        )
        main_embed.add_field(
            name="<a:speechbubble:1380892653847314534> Conditions d'utilisation",
            value="• Vous devez être dans un salon de préparation",
            inline=False
        )
        main_embed.set_footer(text="Radiant Order - Système d'assistance")
        
        # Ajouter le logo du serveur en thumbnail
        if ctx.guild.icon:
            main_embed.set_thumbnail(url=ctx.guild.icon.url)
        
        # Envoyer le message avec le bouton
        try:
            main_message = await target_channel.send(embed=main_embed, view=DemandeOrgaView())
            
            # Sauvegarder l'ID du message dans la config
            await self.config.guild(ctx.guild).message_id.set(main_message.id)
            
            success_embed = discord.Embed(
                title="<a:check_ravena:1380884332708626493> Système configuré !",
                description=f"Le système de demande d'assistance a été configuré dans {target_channel.mention}.\n"
                           f"Message ID: `{main_message.id}`",
                color=0x00FF00
            )
            await ctx.send(embed=success_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur de configuration",
                description=f"Une erreur s'est produite : {str(e)}",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)

    @commands.command(name="fix_demande")
    @commands.has_permissions(manage_guild=True)
    async def fix_demande_view(self, ctx):
        """Réparer la vue persistante si elle ne fonctionne plus"""
        
        # Récupérer les informations de la config
        demande_channel_id = await self.config.guild(ctx.guild).demande_channel_id()
        message_id = await self.config.guild(ctx.guild).message_id()
        
        if not message_id:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Aucun message de demande configuré. Utilisez `setup_demande` d'abord.")
        
        target_channel = self.bot.get_channel(demande_channel_id)
        if not target_channel:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Canal de demande introuvable.")
        
        try:
            # Récupérer le message existant
            message = await target_channel.fetch_message(message_id)
            
            # Réappliquer la vue
            await message.edit(view=DemandeOrgaView())
            
            success_embed = discord.Embed(
                title="<a:check_ravena:1380884332708626493> Vue réparée !",
                description="La vue persistante a été réappliquée au message existant.",
                color=0x00FF00
            )
            await ctx.send(embed=success_embed)
            
        except discord.NotFound:
            # Le message n'existe plus, en créer un nouveau
            await ctx.invoke(self.setup_demande_orga)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="<a:uncheck_ravena:1380884331534483629> Erreur",
                description=f"Impossible de réparer la vue : {str(e)}",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)

    @setup_demande_orga.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("<a:uncheck_ravena:1380884331534483629> Vous n'avez pas les permissions pour utiliser cette commande.")

    @commands.command(name="clean_demande")
    @commands.has_permissions(manage_messages=True)
    async def clean_demande_manual(self, ctx):
        """Nettoyer manuellement le canal de demande d'assistance"""
        
        demande_channel_id = await self.config.guild(ctx.guild).demande_channel_id()
        target_channel = self.bot.get_channel(demande_channel_id)
        
        if not target_channel:
            return await ctx.send("<a:uncheck_ravena:1380884331534483629> Le canal de demande d'orga n'a pas été trouvé.")
        
        # Confirmation
        confirm_embed = discord.Embed(
            title="<a:Warning:1380884984595742790> Confirmation requise",
            description="Êtes-vous sûr de vouloir nettoyer le canal de demande d'assistance ?\n"
                       "Cette action supprimera tous les messages sauf les messages du bot.",
            color=0xFFA500
        )
        
        confirm_message = await ctx.send(embed=confirm_embed)
        await confirm_message.add_reaction("✅")
        await confirm_message.add_reaction("❌")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirm_message.id
        
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            
            if str(reaction.emoji) == "✅":
                # Procéder au nettoyage
                try:
                    loading_embed = discord.Embed(
                        title="<a:PinkLoading:1380886781062414356> Nettoyage en cours...",
                        description="Suppression des messages utilisateurs en cours...",
                        color=0x3498DB
                    )
                    await confirm_message.edit(embed=loading_embed)
                    
                    # Récupérer l'ID du message principal à préserver
                    main_message_id = await self.config.guild(ctx.guild).message_id()
                    
                    messages_deleted = 0
                    async for message in target_channel.history(limit=None):
                        # Ne supprimer que les messages des utilisateurs (pas du bot) et préserver le message principal
                        if not message.author.bot and message.id != main_message_id:
                            try:
                                await message.delete()
                                messages_deleted += 1
                                await asyncio.sleep(0.5)  # Éviter le rate limit
                            except (discord.NotFound, discord.Forbidden):
                                pass
                    
                    success_embed = discord.Embed(
                        title="<a:check_ravena:1380884332708626493> Nettoyage terminé !",
                        description=f"**{messages_deleted}** messages d'utilisateurs ont été supprimés du canal de demande d'assistance.\n"
                                   f"Les messages du bot ont été préservés.",
                        color=0x00FF00
                    )
                    await confirm_message.edit(embed=success_embed)
                    
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        title="<a:uncheck_ravena:1380884331534483629> Erreur",
                        description="Permissions insuffisantes pour nettoyer le canal.",
                        color=0xFF0000
                    )
                    await confirm_message.edit(embed=error_embed)
            else:
                cancel_embed = discord.Embed(
                    title="<a:uncheck_ravena:1380884331534483629> Annulé",
                    description="Le nettoyage a été annulé.",
                    color=0xFF0000
                )
                await confirm_message.edit(embed=cancel_embed)
                
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="<a:Warning:1380884984595742790> Temps écoulé",
                description="La confirmation a expiré. Nettoyage annulé.",
                color=0xFFA500
            )
            await confirm_message.edit(embed=timeout_embed)

async def setup(bot):
    await bot.add_cog(DemandeOrga(bot))

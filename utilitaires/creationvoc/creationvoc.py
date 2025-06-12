import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import asyncio
import datetime

class VoiceControlView(discord.ui.View):
    def __init__(self, cog, owner_id, voice_channel):
        super().__init__(timeout=None)
        self.cog = cog
        self.owner_id = owner_id
        self.voice_channel = voice_channel

    @discord.ui.button(label="🔒 Rendre Privé", style=discord.ButtonStyle.danger, custom_id="voice_private")
    async def make_private(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        # Récupérer le guild depuis le voice channel
        guild = self.voice_channel.guild
        
        # Définir les permissions pour rendre privé
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            interaction.user: discord.PermissionOverwrite(connect=True, manage_channels=True)
        }
        
        await self.voice_channel.edit(overwrites=overwrites)
        
        embed = discord.Embed(
            title="🔒 Salon rendu privé",
            description="Seules les personnes invitées peuvent rejoindre.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🔓 Rendre Public", style=discord.ButtonStyle.success, custom_id="voice_public")
    async def make_public(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        # Récupérer le guild depuis le voice channel
        guild = self.voice_channel.guild
        
        # Rendre public
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=True),
            interaction.user: discord.PermissionOverwrite(connect=True, manage_channels=True)
        }
        
        await self.voice_channel.edit(overwrites=overwrites)
        
        embed = discord.Embed(
            title="🔓 Salon rendu public",
            description="Tout le monde peut rejoindre.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="👥 Limite de Membres", style=discord.ButtonStyle.primary, custom_id="voice_limit")
    async def set_limit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        modal = LimitModal(self.voice_channel)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="✅ Whitelist", style=discord.ButtonStyle.secondary, custom_id="voice_whitelist")
    async def add_whitelist(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        modal = WhitelistModal(self.voice_channel)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="❌ Blacklist", style=discord.ButtonStyle.danger, custom_id="voice_blacklist")
    async def add_blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        modal = BlacklistModal(self.voice_channel)
        await interaction.response.send_modal(modal)

class VoiceControlView2(discord.ui.View):
    def __init__(self, cog, owner_id, voice_channel):
        super().__init__(timeout=None)
        self.cog = cog
        self.owner_id = owner_id
        self.voice_channel = voice_channel

    @discord.ui.button(label="📋 Voir Whitelist", style=discord.ButtonStyle.secondary, custom_id="view_whitelist")
    async def view_whitelist(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        # Récupérer les utilisateurs avec permission connect=True
        whitelist = []
        for user, overwrite in self.voice_channel.overwrites.items():
            if isinstance(user, discord.Member) and overwrite.connect is True:
                whitelist.append(user.mention)
        
        if not whitelist:
            content = "Aucun utilisateur en whitelist"
        else:
            content = "\n".join(whitelist)
        
        embed = discord.Embed(
            title="📋 Whitelist",
            description=content,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🚫 Voir Blacklist", style=discord.ButtonStyle.danger, custom_id="view_blacklist")
    async def view_blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Seul le créateur du salon peut utiliser ceci.", ephemeral=True)
        
        # Récupérer les utilisateurs avec permission connect=False
        blacklist = []
        for user, overwrite in self.voice_channel.overwrites.items():
            if isinstance(user, discord.Member) and overwrite.connect is False:
                blacklist.append(user.mention)
        
        if not blacklist:
            content = "Aucun utilisateur en blacklist"
        else:
            content = "\n".join(blacklist)
        
        embed = discord.Embed(
            title="🚫 Blacklist",
            description=content,
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class LimitModal(discord.ui.Modal):
    def __init__(self, voice_channel):
        super().__init__(title="Définir une limite de membres")
        self.voice_channel = voice_channel

    limit = discord.ui.TextInput(
        label="Nombre maximum de membres",
        placeholder="Entre 0 (illimité) et 99",
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            limit_value = int(self.limit.value)
            if limit_value < 0 or limit_value > 99:
                raise ValueError
            
            await self.voice_channel.edit(user_limit=limit_value)
            
            if limit_value == 0:
                message = "Limite supprimée (illimité)"
            else:
                message = f"Limite fixée à {limit_value} membres"
            
            embed = discord.Embed(
                title="👥 Limite modifiée",
                description=message,
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except ValueError:
            await interaction.response.send_message(
                "❌ Veuillez entrer un nombre entre 0 et 99.", 
                ephemeral=True
            )

class WhitelistModal(discord.ui.Modal):
    def __init__(self, voice_channel):
        super().__init__(title="Ajouter à la whitelist")
        self.voice_channel = voice_channel

    user_input = discord.ui.TextInput(
        label="Utilisateur à autoriser",
        placeholder="@utilisateur ou ID",
        min_length=1,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        user_text = self.user_input.value.strip()
        
        # Récupérer le guild depuis le voice channel
        guild = self.voice_channel.guild
        
        # Extraire l'ID si c'est une mention
        if user_text.startswith('<@') and user_text.endswith('>'):
            user_id = user_text[2:-1]
            if user_id.startswith('!'):
                user_id = user_id[1:]
        else:
            user_id = user_text
        
        try:
            user = guild.get_member(int(user_id))
            if not user:
                return await interaction.response.send_message(
                    "❌ Utilisateur non trouvé.", ephemeral=True
                )
            
            # Ajouter à la whitelist
            overwrite = self.voice_channel.overwrites_for(user)
            overwrite.connect = True
            await self.voice_channel.set_permissions(user, overwrite=overwrite)
            
            embed = discord.Embed(
                title="✅ Utilisateur ajouté à la whitelist",
                description=f"{user.mention} peut maintenant rejoindre le salon.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except ValueError:
            await interaction.response.send_message(
                "❌ ID utilisateur invalide.", ephemeral=True
            )

class BlacklistModal(discord.ui.Modal):
    def __init__(self, voice_channel):
        super().__init__(title="Ajouter à la blacklist")
        self.voice_channel = voice_channel

    user_input = discord.ui.TextInput(
        label="Utilisateur à bannir",
        placeholder="@utilisateur ou ID",
        min_length=1,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        user_text = self.user_input.value.strip()
        
        # Récupérer le guild depuis le voice channel
        guild = self.voice_channel.guild
        
        # Extraire l'ID si c'est une mention
        if user_text.startswith('<@') and user_text.endswith('>'):
            user_id = user_text[2:-1]
            if user_id.startswith('!'):
                user_id = user_id[1:]
        else:
            user_id = user_text
        
        try:
            user = guild.get_member(int(user_id))
            if not user:
                return await interaction.response.send_message(
                    "❌ Utilisateur non trouvé.", ephemeral=True
                )
            
            # Ajouter à la blacklist
            overwrite = self.voice_channel.overwrites_for(user)
            overwrite.connect = False
            await self.voice_channel.set_permissions(user, overwrite=overwrite)
            
            # Déconnecter l'utilisateur s'il est dans le salon
            if user.voice and user.voice.channel == self.voice_channel:
                await user.move_to(None)
            
            embed = discord.Embed(
                title="❌ Utilisateur ajouté à la blacklist",
                description=f"{user.mention} ne peut plus rejoindre le salon.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except ValueError:
            await interaction.response.send_message(
                "❌ ID utilisateur invalide.", ephemeral=True
            )

class CreationVoc(commands.Cog):
    """🎤 Système de création automatique de channels vocaux temporaires"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123987456)
        
        default_guild = {
            "trigger_channel": 1380582889514729615,
            "temp_channels": {},  # {channel_id: owner_id}
            "category_id": None
        }
        
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Détecte les changements de salon vocal"""
        if await self.bot.cog_disabled_in_guild(self, member.guild):
            return
        
        guild_config = self.config.guild(member.guild)
        trigger_channel_id = await guild_config.trigger_channel()
        temp_channels = await guild_config.temp_channels()
        
        # Quelqu'un rejoint le channel de création
        if after.channel and after.channel.id == trigger_channel_id:
            await self.create_temp_channel(member, after.channel)
        
        # Quelqu'un quitte un channel temporaire
        if before.channel and str(before.channel.id) in temp_channels:
            if len(before.channel.members) == 0:
                await self.delete_temp_channel(before.channel)

    async def create_temp_channel(self, member, trigger_channel):
        """Créer un channel vocal temporaire"""
        guild_config = self.config.guild(member.guild)
        
        # Trouver la catégorie du channel trigger
        category = trigger_channel.category
        
        # Créer le nouveau channel
        channel_name = f"🎤 {member.display_name}"
        
        overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(connect=True),
            member: discord.PermissionOverwrite(connect=True, manage_channels=True, move_members=True)
        }
        
        temp_channel = await member.guild.create_voice_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            position=trigger_channel.position + 1
        )
        
        # Enregistrer le channel temporaire
        async with guild_config.temp_channels() as temp_channels:
            temp_channels[str(temp_channel.id)] = member.id
        
        # Déplacer le membre dans le nouveau channel
        try:
            await member.move_to(temp_channel)
        except:
            pass  # Le membre a peut-être quitté
        
        # Envoyer le message de contrôle
        await self.send_control_message(member, temp_channel)

    async def send_control_message(self, member, voice_channel):
        """Envoyer le message avec les boutons de contrôle"""
        embed = discord.Embed(
            title="🎤 Contrôles du salon vocal",
            description=f"{member.mention}, bienvenue dans votre salon vocal personnalisé!\n\n"
                       f"Utilisez les boutons ci-dessous pour personnaliser votre salon:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🔒 Rendre Privé",
            value="Seules les personnes invitées peuvent rejoindre",
            inline=True
        )
        
        embed.add_field(
            name="🔓 Rendre Public", 
            value="Tout le monde peut rejoindre",
            inline=True
        )
        
        embed.add_field(
            name="👥 Limite de Membres",
            value="Définir un nombre maximum de participants",
            inline=True
        )
        
        embed.add_field(
            name="✅ Whitelist",
            value="Ajouter un utilisateur qui pourra rejoindre même si le salon est privé",
            inline=True
        )
        
        embed.add_field(
            name="❌ Blacklist",
            value="Empêcher un utilisateur de rejoindre et l'exclure s'il est déjà présent",
            inline=True
        )
        
        embed.add_field(
            name="📋 Voir listes",
            value="Afficher la liste des utilisateurs whitelistés/blacklistés",
            inline=True
        )
        
        embed.set_footer(
            text="Seul le créateur du salon peut utiliser ces contrôles."
        )
        
        try:
            # Envoyer directement dans le chat du channel vocal
            # Première ligne de boutons
            view1 = VoiceControlView(self, member.id, voice_channel)
            await voice_channel.send(embed=embed, view=view1)
            
            # Deuxième ligne de boutons
            view2 = VoiceControlView2(self, member.id, voice_channel)
            await voice_channel.send(view=view2)
            
        except Exception as e:
            # Si l'envoi échoue, essayer une seule fois
            try:
                view1 = VoiceControlView(self, member.id, voice_channel)
                await voice_channel.send(embed=embed, view=view1)
                
                view2 = VoiceControlView2(self, member.id, voice_channel)
                await voice_channel.send(view=view2)
            except:
                pass  # Si ça échoue complètement, on ignore

    async def delete_temp_channel(self, channel):
        """Supprimer un channel temporaire vide"""
        guild_config = self.config.guild(channel.guild)
        
        # Retirer de la liste des channels temporaires
        async with guild_config.temp_channels() as temp_channels:
            if str(channel.id) in temp_channels:
                del temp_channels[str(channel.id)]
        
        # Supprimer le channel
        try:
            await channel.delete(reason="Channel vocal temporaire vide")
        except:
            pass

    @commands.group(name="creationvoc")
    @checks.admin_or_permissions(manage_channels=True)
    async def creation_voc(self, ctx):
        """⚙️ Gestion du système de création vocale"""
        if ctx.invoked_subcommand is None:
            await self.show_config(ctx)

    @creation_voc.command(name="trigger")
    async def set_trigger(self, ctx, channel: discord.VoiceChannel):
        """🎯 Définir le channel vocal déclencheur"""
        await self.config.guild(ctx.guild).trigger_channel.set(channel.id)
        
        embed = discord.Embed(
            title="✅ Channel déclencheur configuré",
            description=f"Les utilisateurs qui rejoignent {channel.mention} créeront un salon temporaire.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @creation_voc.command(name="cleanup")
    async def cleanup_channels(self, ctx):
        """🧹 Nettoyer les channels temporaires vides"""
        guild_config = self.config.guild(ctx.guild)
        temp_channels = await guild_config.temp_channels()
        cleaned = 0
        
        for channel_id in list(temp_channels.keys()):
            channel = ctx.guild.get_channel(int(channel_id))
            if not channel or len(channel.members) == 0:
                if channel:
                    try:
                        await channel.delete(reason="Nettoyage automatique")
                        cleaned += 1
                    except:
                        pass
                
                # Retirer de la config
                async with guild_config.temp_channels() as temp_ch:
                    if channel_id in temp_ch:
                        del temp_ch[channel_id]
        
        embed = discord.Embed(
            title="🧹 Nettoyage terminé",
            description=f"{cleaned} channels temporaires supprimés.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def show_config(self, ctx):
        """Afficher la configuration actuelle"""
        guild_config = self.config.guild(ctx.guild)
        trigger_channel_id = await guild_config.trigger_channel()
        temp_channels = await guild_config.temp_channels()
        
        trigger_channel = ctx.guild.get_channel(trigger_channel_id)
        
        embed = discord.Embed(
            title="⚙️ Configuration Création Vocale",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="🎯 Channel déclencheur",
            value=trigger_channel.mention if trigger_channel else "Non configuré",
            inline=True
        )
        
        embed.add_field(
            name="📊 Channels temporaires actifs",
            value=f"{len(temp_channels)} channels",
            inline=True
        )
        
        embed.add_field(
            name="🛠️ Commandes",
            value="`!creationvoc trigger` - Définir le channel\n"
                  "`!creationvoc cleanup` - Nettoyer les channels vides",
            inline=False
        )
        
        embed.set_footer(text="Spike Rush - Création vocale automatique")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CreationVoc(bot)) 
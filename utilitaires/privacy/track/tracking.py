import discord
from redbot.core import commands, Config
from redbot.core.bot import Red
import datetime
import asyncio

class Tracking(commands.Cog):
    """<a:INFINITYBYP:1380887933325676706> Système de tracking automatique pour surveiller l'activité du serveur"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321)
        
        # Configuration avec les IDs des channels de tracking
        default_guild = {
            "target_guild_id": 1380282831347122267,  # Serveur à surveiller
            "channels": {
                "messages": 1380568606668099714,
                "images": 1380568610409283618,
                "deletes": 1380568614511575120,
                "voice": 1380568617464102923,
                "joins": 1380568620995707051,
                "edits": 1380568624418390207,
                "leaves": 1380568627673043124,
                "roles": 1380568631121023091,
                "bans": 1380568634979516576,
                "reactions": 1380568638251208918
            },
            "tracking_enabled": True
        }
        
        self.config.register_guild(**default_guild)

    def is_target_guild(self, guild_id):
        """Vérifie si c'est le serveur à surveiller"""
        return guild_id == 1380282831347122267

    async def send_to_channel(self, channel_key, embed):
        """Envoie un embed dans le bon channel de tracking"""
        try:
            # Récupérer l'ID du channel depuis la config
            channels = await self.config.guild_from_id(1380282831347122267).channels()
            channel_id = channels.get(channel_key)
            
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)
        except Exception as e:
            print(f"Erreur envoi tracking {channel_key}: {e}")

    # <a:speechbubble:1380892653847314534> MESSAGES
    @commands.Cog.listener()
    async def on_message(self, message):
        """Track les messages envoyés"""
        if message.author.bot or not self.is_target_guild(message.guild.id):
            return
        
        # Séparer images et messages normaux
        if message.attachments:
            # Track dans images
            embed = discord.Embed(
                title="<a:FallingPetals:1380882470060425267> Image/Fichier envoyé",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            embed.set_author(name=f"{message.author.display_name}", icon_url=message.author.display_avatar.url)
            embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=message.channel.mention, inline=True)
            embed.add_field(name="<a:whitecrown:1380899677297315880> Auteur", value=message.author.mention, inline=True)
            embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{message.id}`", inline=True)
            
            if message.content:
                embed.add_field(name="<a:speechbubble:1380892653847314534> Contenu", value=message.content[:1024], inline=False)
            
            # Lister les fichiers
            files_list = "\n".join([f"<a:boost:1380882468621520916> [{att.filename}]({att.url})" for att in message.attachments[:5]])
            embed.add_field(name="<a:INFINITYBYP:1380887933325676706> Fichiers", value=files_list, inline=False)
            
            await self.send_to_channel("images", embed)
        
        else:
            # Track dans messages
            embed = discord.Embed(
                title="<a:speechbubble:1380892653847314534> Message envoyé",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            embed.set_author(name=f"{message.author.display_name}", icon_url=message.author.display_avatar.url)
            embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=message.channel.mention, inline=True)
            embed.add_field(name="<a:whitecrown:1380899677297315880> Auteur", value=message.author.mention, inline=True)
            embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{message.id}`", inline=True)
            embed.add_field(name="<a:speechbubble:1380892653847314534> Contenu", value=message.content[:1024] if message.content else "*Pas de contenu*", inline=False)
            
            await self.send_to_channel("messages", embed)

    # <a:uncheck_ravena:1380884331534483629> SUPPRESSIONS
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Track les messages supprimés"""
        if message.author.bot or not self.is_target_guild(message.guild.id):
            return
        
        embed = discord.Embed(
            title="<a:uncheck_ravena:1380884331534483629> Message supprimé",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{message.author.display_name}", icon_url=message.author.display_avatar.url)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=message.channel.mention, inline=True)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Auteur", value=message.author.mention, inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{message.id}`", inline=True)
        embed.add_field(name="<a:sagecry_valorant:1380903620769222728> Contenu supprimé", value=message.content[:1024] if message.content else "*Pas de contenu*", inline=False)
        
        if message.attachments:
            files_list = "\n".join([f"<a:boost:1380882468621520916> {att.filename}" for att in message.attachments[:5]])
            embed.add_field(name="<a:INFINITYBYP:1380887933325676706> Fichiers supprimés", value=files_list, inline=False)
        
        await self.send_to_channel("deletes", embed)

    # <a:maruloader:1380888045259329569> MODIFICATIONS
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Track les messages modifiés"""
        if before.author.bot or not self.is_target_guild(before.guild.id):
            return
        
        # Ignorer si pas de changement de contenu
        if before.content == after.content:
            return
        
        embed = discord.Embed(
            title="<a:maruloader:1380888045259329569> Message modifié",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{after.author.display_name}", icon_url=after.author.display_avatar.url)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=after.channel.mention, inline=True)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Auteur", value=after.author.mention, inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{after.id}`", inline=True)
        embed.add_field(name="<a:Lightpinkgothheartgif:1380882449126527037> Avant", value=before.content[:512] if before.content else "*Pas de contenu*", inline=False)
        embed.add_field(name="<a:check_ravena:1380884332708626493> Après", value=after.content[:512] if after.content else "*Pas de contenu*", inline=False)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Lien", value=f"[Aller au message]({after.jump_url})", inline=False)
        
        await self.send_to_channel("edits", embed)

    # <a:FallingPetals:1380882470060425267> ARRIVÉES
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Track les arrivées de membres"""
        if not self.is_target_guild(member.guild.id):
            return
        
        embed = discord.Embed(
            title="<a:FallingPetals:1380882470060425267> Nouveau membre",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=member.mention, inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="<a:agooglebell:1380895257541083300> Compte créé", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=True)
        embed.add_field(name="<a:boost:1380882468621520916> Membres totaux", value=f"{member.guild.member_count}", inline=False)
        
        # Âge du compte
        account_age = datetime.datetime.now() - member.created_at.replace(tzinfo=None)
        if account_age.days < 7:
            embed.add_field(name="<a:Warning:1380884984595742790> Alerte", value=f"Compte récent ({account_age.days} jours)", inline=False)
        
        await self.send_to_channel("joins", embed)

    # <a:sagecry_valorant:1380903620769222728> DÉPARTS
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Track les départs de membres"""
        if not self.is_target_guild(member.guild.id):
            return
        
        embed = discord.Embed(
            title="<a:sagecry_valorant:1380903620769222728> Membre parti",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=f"{member.mention}\n({member.name}#{member.discriminator})", inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="<a:agooglebell:1380895257541083300> A rejoint le", value=f"<t:{int(member.joined_at.timestamp())}:F>" if member.joined_at else "Inconnu", inline=True)
        
        # Durée de présence
        if member.joined_at:
            duration = datetime.datetime.now() - member.joined_at.replace(tzinfo=None)
            embed.add_field(name="<a:PinkLoading:1380886781062414356> Durée sur le serveur", value=f"{duration.days} jours", inline=True)
        
        embed.add_field(name="<a:boost:1380882468621520916> Membres restants", value=f"{member.guild.member_count}", inline=True)
        
        # Lister les rôles
        if len(member.roles) > 1:
            roles = ", ".join([role.name for role in member.roles[1:][:10]])
            embed.add_field(name="<a:INFINITYBYP:1380887933325676706> Rôles", value=roles, inline=False)
        
        await self.send_to_channel("leaves", embed)

    # <a:GummyDragonMicrophone:1380884049375002624> VOCAL
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Track les événements vocaux"""
        if member.bot or not self.is_target_guild(member.guild.id):
            return
        
        embed = discord.Embed(
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
        
        # Connexion
        if before.channel is None and after.channel is not None:
            embed.title = "<a:GummyDragonMicrophone:1380884049375002624> Connexion vocale"
            embed.color = discord.Color.green()
            embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=member.mention, inline=True)
            embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=after.channel.mention, inline=True)
            embed.add_field(name="<a:boost:1380882468621520916> Membres", value=f"{len(after.channel.members)}", inline=True)
        
        # Déconnexion
        elif before.channel is not None and after.channel is None:
            embed.title = "<a:GummyDragonMicrophone:1380884049375002624> Déconnexion vocale"
            embed.color = discord.Color.red()
            embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=member.mention, inline=True)
            embed.add_field(name="<a:sagecry_valorant:1380903620769222728> Salon quitté", value=before.channel.mention, inline=True)
            embed.add_field(name="<a:boost:1380882468621520916> Membres restants", value=f"{len(before.channel.members)}", inline=True)
        
        # Changement de salon
        elif before.channel != after.channel:
            embed.title = "<a:GummyDragonMicrophone:1380884049375002624> Changement de salon vocal"
            embed.color = discord.Color.blue()
            embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=member.mention, inline=True)
            embed.add_field(name="<a:sagecry_valorant:1380903620769222728> Depuis", value=before.channel.mention if before.channel else "Aucun", inline=True)
            embed.add_field(name="<a:FallingPetals:1380882470060425267> Vers", value=after.channel.mention if after.channel else "Aucun", inline=True)
        
        # Mute/Unmute/Deafen
        elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:
            changes = []
            if before.self_mute != after.self_mute:
                changes.append(f"<a:sound:1380899668434747463> Mute: {'ON' if after.self_mute else 'OFF'}")
            if before.self_deaf != after.self_deaf:
                changes.append(f"<a:sound:1380899668434747463> Deafen: {'ON' if after.self_deaf else 'OFF'}")
            
            embed.title = "<a:GummyDragonMicrophone:1380884049375002624> Changement d'état vocal"
            embed.color = discord.Color.yellow()
            embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=member.mention, inline=True)
            embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=after.channel.mention if after.channel else "Aucun", inline=True)
            embed.add_field(name="<a:maruloader:1380888045259329569> Changements", value="\n".join(changes), inline=True)
        
        else:
            return  # Pas d'événement intéressant
        
        await self.send_to_channel("voice", embed)

    # <a:INFINITYBYP:1380887933325676706> RÔLES
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Track les changements de rôles"""
        if before.bot or not self.is_target_guild(before.guild.id):
            return
        
        # Vérifier les changements de rôles
        before_roles = set(before.roles)
        after_roles = set(after.roles)
        
        added_roles = after_roles - before_roles
        removed_roles = before_roles - after_roles
        
        if added_roles or removed_roles:
            embed = discord.Embed(
                title="<a:INFINITYBYP:1380887933325676706> Modification de rôles",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            embed.set_author(name=f"{after.display_name}", icon_url=after.display_avatar.url)
            embed.add_field(name="<a:whitecrown:1380899677297315880> Membre", value=after.mention, inline=True)
            embed.add_field(name="<a:PinkKey:1380899678622711808> ID", value=f"`{after.id}`", inline=True)
            
            if added_roles:
                roles_added = "\n".join([f"<a:check_ravena:1380884332708626493> **{role.name}** (`{role.id}`)" for role in added_roles])
                embed.add_field(name="<a:FallingPetals:1380882470060425267> Rôles ajoutés", value=roles_added, inline=False)
            
            if removed_roles:
                roles_removed = "\n".join([f"<a:uncheck_ravena:1380884331534483629> **{role.name}** (`{role.id}`)" for role in removed_roles])
                embed.add_field(name="<a:sagecry_valorant:1380903620769222728> Rôles retirés", value=roles_removed, inline=False)
            
            await self.send_to_channel("roles", embed)

    # <a:WhiteBalisong:1380892882516443287> BANS
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Track les bannissements"""
        if not self.is_target_guild(guild.id):
            return
        
        embed = discord.Embed(
            title="<a:WhiteBalisong:1380892882516443287> Membre banni",
            color=discord.Color.dark_red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Utilisateur", value=f"{user.mention}\n({user.name}#{user.discriminator})", inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="<a:agooglebell:1380895257541083300> Compte créé", value=f"<t:{int(user.created_at.timestamp())}:F>", inline=True)
        
        # Essayer de récupérer la raison du ban
        try:
            ban_info = await guild.fetch_ban(user)
            if ban_info.reason:
                embed.add_field(name="<a:speechbubble:1380892653847314534> Raison", value=ban_info.reason, inline=False)
        except:
            pass
        
        await self.send_to_channel("bans", embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Track les débannissements"""
        if not self.is_target_guild(guild.id):
            return
        
        embed = discord.Embed(
            title="<a:check_ravena:1380884332708626493> Membre débanni",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Utilisateur", value=f"{user.mention}\n({user.name}#{user.discriminator})", inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> ID", value=f"`{user.id}`", inline=True)
        
        await self.send_to_channel("bans", embed)

    # <a:Lightblueheartgif:1380882450439471165> RÉACTIONS
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Track les réactions ajoutées"""
        if user.bot or not self.is_target_guild(reaction.message.guild.id):
            return
        
        embed = discord.Embed(
            title="<a:Lightblueheartgif:1380882450439471165> Réaction ajoutée",
            color=discord.Color.yellow(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Utilisateur", value=user.mention, inline=True)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=reaction.message.channel.mention, inline=True)
        embed.add_field(name="<a:Lightblueheartgif:1380882450439471165> Réaction", value=str(reaction.emoji), inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{reaction.message.id}`", inline=True)
        embed.add_field(name="<a:speechbubble:1380892653847314534> Contenu du message", value=reaction.message.content[:512] if reaction.message.content else "*Pas de contenu*", inline=False)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Lien", value=f"[Aller au message]({reaction.message.jump_url})", inline=False)
        
        await self.send_to_channel("reactions", embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """Track les réactions supprimées"""
        if user.bot or not self.is_target_guild(reaction.message.guild.id):
            return
        
        embed = discord.Embed(
            title="<a:uncheck_ravena:1380884331534483629> Réaction supprimée",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        embed.add_field(name="<a:whitecrown:1380899677297315880> Utilisateur", value=user.mention, inline=True)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Salon", value=reaction.message.channel.mention, inline=True)
        embed.add_field(name="<a:Lightblueheartgif:1380882450439471165> Réaction", value=str(reaction.emoji), inline=True)
        embed.add_field(name="<a:PinkKey:1380899678622711808> Message ID", value=f"`{reaction.message.id}`", inline=True)
        embed.add_field(name="<a:Animated_Arrow_Blue:1380888378953961472> Lien", value=f"[Aller au message]({reaction.message.jump_url})", inline=False)
        
        await self.send_to_channel("reactions", embed)

    # COMMANDES DE GESTION
    @commands.group(name="tracking")
    @commands.admin_or_permissions(manage_guild=True)
    async def tracking(self, ctx):
        """<a:INFINITYBYP:1380887933325676706> Gestion du système de tracking"""
        pass

    @tracking.command(name="status")
    async def tracking_status(self, ctx):
        """<a:INFINITYBYP:1380887933325676706> Statut du système de tracking"""
        enabled = await self.config.guild(ctx.guild).tracking_enabled()
        target_guild = await self.config.guild(ctx.guild).target_guild_id()
        channels = await self.config.guild(ctx.guild).channels()
        
        embed = discord.Embed(
            title="<a:INFINITYBYP:1380887933325676706> Statut du Tracking",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="<a:PinkLoading:1380886781062414356> Tracking", value="<a:check_ravena:1380884332708626493> Activé" if enabled else "<a:uncheck_ravena:1380884331534483629> Désactivé", inline=True)
        embed.add_field(name="<a:boost:1380882468621520916> Serveur surveillé", value=f"`{target_guild}`", inline=True)
        embed.add_field(name="<a:agooglebell:1380895257541083300> Channels configurés", value=f"{len(channels)}/10", inline=True)
        
        # Liste des channels
        channel_status = ""
        for key, channel_id in channels.items():
            channel = ctx.guild.get_channel(channel_id)
            status = "<a:check_ravena:1380884332708626493>" if channel else "<a:uncheck_ravena:1380884331534483629>"
            channel_status += f"{status} {key}: `{channel_id}`\n"
        
        embed.add_field(name="<a:Anouncements_Animated:1380895055694528542> Channels", value=channel_status, inline=False)
        
        await ctx.send(embed=embed)

    @tracking.command(name="toggle")
    async def tracking_toggle(self, ctx):
        """<a:maruloader:1380888045259329569> Active/Désactive le tracking"""
        current = await self.config.guild(ctx.guild).tracking_enabled()
        new_state = not current
        await self.config.guild(ctx.guild).tracking_enabled.set(new_state)
        
        status = "activé" if new_state else "désactivé"
        status_emoji = "<a:check_ravena:1380884332708626493>" if new_state else "<a:uncheck_ravena:1380884331534483629>"
        embed = discord.Embed(
            title=f"{status_emoji} Tracking {status}",
            description=f"Le système de tracking a été **{status}**.",
            color=discord.Color.green() if new_state else discord.Color.red()
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tracking(bot))

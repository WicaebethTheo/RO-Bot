import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
import asyncio

class Utils(commands.Cog):
    """🔧 Utilitaires de scan de serveur pour récupérer les IDs des salons, rôles et emojis"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123987654)
        
        # Configuration avec les IDs des channels et serveur cible
        default_global = {
            "target_server_id": 1380282831347122267,
            "channels_output": 1380571973150838976,
            "roles_output": 1380571960362275047,
            "emojis_output": 1380572088410177657
        }
        
        self.config.register_global(**default_global)

    @commands.command(name="utils")
    @checks.admin_or_permissions(manage_guild=True)
    async def scan_server(self, ctx):
        """🔍 Scanner le serveur cible et publier les informations dans les channels dédiés"""
        
        # Récupérer la configuration
        target_server_id = await self.config.target_server_id()
        channels_output = await self.config.channels_output()
        roles_output = await self.config.roles_output()
        emojis_output = await self.config.emojis_output()
        
        # Récupérer le serveur cible
        target_guild = self.bot.get_guild(target_server_id)
        if not target_guild:
            error_embed = discord.Embed(
                title="❌ Erreur",
                description=f"Impossible de trouver le serveur avec l'ID `{target_server_id}`",
                color=discord.Color.red()
            )
            return await ctx.send(embed=error_embed)
        
        # Message de confirmation
        start_embed = discord.Embed(
            title="🔍 Scan en cours...",
            description=f"Analyse du serveur **{target_guild.name}**\n"
                       f"📊 Membres: {target_guild.member_count}\n"
                       f"📺 Salons: {len(target_guild.channels)}\n"
                       f"🏷️ Rôles: {len(target_guild.roles)}\n"
                       f"😀 Emojis: {len(target_guild.emojis)}",
            color=discord.Color.blue()
        )
        start_embed.set_thumbnail(url=target_guild.icon.url if target_guild.icon else None)
        await ctx.send(embed=start_embed)
        
        try:
            # Scanner et publier les salons
            await self.scan_channels(target_guild, channels_output)
            
            # Scanner et publier les rôles
            await self.scan_roles(target_guild, roles_output)
            
            # Scanner et publier les emojis
            await self.scan_emojis(target_guild, emojis_output)
            
            # Message de succès
            success_embed = discord.Embed(
                title="✅ Scan terminé !",
                description="Toutes les informations ont été publiées dans les channels dédiés.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            await ctx.send(embed=success_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="💥 Erreur lors du scan",
                description=f"Une erreur s'est produite :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)

    async def scan_channels(self, guild, output_channel_id):
        """Scanner et publier les salons avec leurs IDs"""
        output_channel = self.bot.get_channel(output_channel_id)
        if not output_channel:
            return
        
        # Créer l'embed principal
        main_embed = discord.Embed(
            title="📺 Salons du Serveur",
            description=f"**{guild.name}** - {len(guild.channels)} salons au total",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        main_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await output_channel.send(embed=main_embed)
        
        # Organiser les channels par catégorie et type
        categories = {}
        channels_without_category = []
        
        # Séparer les channels par catégorie
        for channel in guild.channels:
            if isinstance(channel, discord.CategoryChannel):
                if channel not in categories:
                    categories[channel] = []
            elif channel.category:
                if channel.category not in categories:
                    categories[channel.category] = []
                categories[channel.category].append(channel)
            else:
                channels_without_category.append(channel)
        
        # Publier les salons sans catégorie
        if channels_without_category:
            embed = discord.Embed(
                title="📁 Salons sans catégorie",
                color=0x99AAB5  # Couleur grise en hexadécimal
            )
            
            content = ""
            for channel in sorted(channels_without_category, key=lambda c: c.name.lower()):
                emoji = self.get_channel_emoji(channel)
                content += f"{emoji} **{channel.name}**\n📋 ID: `{channel.id}`\n\n"
                
                if len(content) > 1800:  # Limite pour éviter les messages trop longs
                    embed.description = content
                    await output_channel.send(embed=embed)
                    content = ""
                    embed = discord.Embed(title="📁 Salons sans catégorie (suite)", color=0x99AAB5)
            
            if content:
                embed.description = content
                await output_channel.send(embed=embed)
            
            await asyncio.sleep(0.5)
        
        # Publier les catégories et leurs salons
        sorted_categories = sorted(categories.keys(), key=lambda c: c.position)
        
        for category in sorted_categories:
            channels = categories[category]
            if not channels:  # Catégorie vide, afficher quand même
                embed = discord.Embed(
                    title=f"📂 {category.name}",
                    description="*Catégorie vide*",
                    color=discord.Color.blue()
                )
                embed.add_field(name="🆔 ID Catégorie", value=f"`{category.id}`", inline=False)
                await output_channel.send(embed=embed)
                continue
                
            embed = discord.Embed(
                title=f"📂 {category.name}",
                color=discord.Color.blue()
            )
            embed.add_field(name="🆔 ID Catégorie", value=f"`{category.id}`", inline=False)
            
            content = ""
            # Trier les channels par position dans la catégorie
            sorted_channels = sorted(channels, key=lambda c: c.position)
            
            for channel in sorted_channels:
                emoji = self.get_channel_emoji(channel)
                content += f"{emoji} **{channel.name}**\n📋 ID: `{channel.id}`\n\n"
                
                if len(content) > 1600:  # Limite plus basse pour laisser place au header
                    embed.description = content
                    await output_channel.send(embed=embed)
                    content = ""
                    embed = discord.Embed(title=f"📂 {category.name} (suite)", color=discord.Color.blue())
                    await asyncio.sleep(0.5)
            
            if content:
                embed.description = content
                await output_channel.send(embed=embed)
            
            await asyncio.sleep(0.5)  # Éviter le rate limiting

    async def scan_roles(self, guild, output_channel_id):
        """Scanner et publier les rôles avec leurs IDs"""
        output_channel = self.bot.get_channel(output_channel_id)
        if not output_channel:
            return
        
        # Créer l'embed principal
        main_embed = discord.Embed(
            title="🏷️ Rôles du Serveur",
            description=f"**{guild.name}** - {len(guild.roles)} rôles au total",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        main_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await output_channel.send(embed=main_embed)
        
        # Trier les rôles par position (du plus haut au plus bas)
        sorted_roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        
        embed = discord.Embed(
            title="📋 Liste des Rôles",
            color=discord.Color.green()
        )
        
        content = ""
        for role in sorted_roles:
            # Couleur du rôle
            color_hex = f"#{role.color.value:06x}" if role.color.value != 0 else "#99aab5"
            
            # Permissions spéciales
            perms = []
            if role.permissions.administrator:
                perms.append("👑 Admin")
            if role.permissions.manage_guild:
                perms.append("⚙️ Gérer")
            if role.permissions.kick_members:
                perms.append("👢 Kick")
            if role.permissions.ban_members:
                perms.append("🔨 Ban")
            
            perm_text = " | ".join(perms) if perms else "📝 Standard"
            
            content += f"**{role.name}**\n"
            content += f"📋 ID: `{role.id}`\n"
            content += f"🎨 {color_hex} | 👥 {len(role.members)} membres\n"
            content += f"🔐 {perm_text}\n\n"
            
            if len(content) > 1800:
                embed.description = content
                await output_channel.send(embed=embed)
                content = ""
                embed = discord.Embed(title="📋 Liste des Rôles (suite)", color=discord.Color.green())
                await asyncio.sleep(0.5)
        
        if content:
            embed.description = content
            await output_channel.send(embed=embed)

    async def scan_emojis(self, guild, output_channel_id):
        """Scanner et publier les emojis avec leurs IDs"""
        output_channel = self.bot.get_channel(output_channel_id)
        if not output_channel:
            return
        
        # Créer l'embed principal
        main_embed = discord.Embed(
            title="😀 Emojis du Serveur",
            description=f"**{guild.name}** - {len(guild.emojis)} emojis personnalisés",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.now()
        )
        main_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await output_channel.send(embed=main_embed)
        
        if not guild.emojis:
            no_emoji_embed = discord.Embed(
                title="😕 Aucun emoji personnalisé",
                description="Ce serveur n'a pas d'emojis personnalisés.",
                color=discord.Color.orange()
            )
            return await output_channel.send(embed=no_emoji_embed)
        
        # Séparer emojis statiques et animés
        static_emojis = [e for e in guild.emojis if not e.animated]
        animated_emojis = [e for e in guild.emojis if e.animated]
        
        # Emojis statiques
        if static_emojis:
            embed = discord.Embed(
                title="🖼️ Emojis Statiques",
                color=discord.Color.blue()
            )
            
            content = ""
            for emoji in sorted(static_emojis, key=lambda e: e.name.lower()):
                content += f"{emoji} **{emoji.name}**\n"
                content += f"📋 ID: `{emoji.id}`\n"
                content += f"🔗 Code: `<:{emoji.name}:{emoji.id}>`\n\n"
                
                if len(content) > 1800:
                    embed.description = content
                    await output_channel.send(embed=embed)
                    content = ""
                    embed = discord.Embed(title="🖼️ Emojis Statiques (suite)", color=discord.Color.blue())
                    await asyncio.sleep(0.5)
            
            if content:
                embed.description = content
                await output_channel.send(embed=embed)
        
        # Emojis animés
        if animated_emojis:
            embed = discord.Embed(
                title="🎬 Emojis Animés",
                color=discord.Color.purple()
            )
            
            content = ""
            for emoji in sorted(animated_emojis, key=lambda e: e.name.lower()):
                content += f"{emoji} **{emoji.name}**\n"
                content += f"📋 ID: `{emoji.id}`\n"
                content += f"🔗 Code: `<a:{emoji.name}:{emoji.id}>`\n\n"
                
                if len(content) > 1800:
                    embed.description = content
                    await output_channel.send(embed=embed)
                    content = ""
                    embed = discord.Embed(title="🎬 Emojis Animés (suite)", color=discord.Color.purple())
                    await asyncio.sleep(0.5)
            
            if content:
                embed.description = content
                await output_channel.send(embed=embed)

    def get_channel_emoji(self, channel):
        """Retourner l'emoji approprié selon le type de channel"""
        if isinstance(channel, discord.TextChannel):
            return "💬"
        elif isinstance(channel, discord.VoiceChannel):
            return "🎤"
        elif isinstance(channel, discord.StageChannel):
            return "🎭"
        elif isinstance(channel, discord.ForumChannel):
            return "📋"
        elif isinstance(channel, discord.CategoryChannel):
            return "📂"
        elif isinstance(channel, discord.NewsChannel):
            return "📢"
        elif isinstance(channel, discord.Thread):
            return "🧵"
        else:
            return "📺"

    @commands.group(name="utilsconfig")
    @checks.admin_or_permissions(administrator=True)
    async def utils_config(self, ctx):
        """⚙️ Configuration du système Utils"""
        pass

    @utils_config.command(name="server")
    async def set_target_server(self, ctx, server_id: int):
        """🎯 Définir le serveur à scanner"""
        guild = self.bot.get_guild(server_id)
        if not guild:
            return await ctx.send("❌ Serveur introuvable avec cet ID.")
        
        await self.config.target_server_id.set(server_id)
        
        embed = discord.Embed(
            title="✅ Serveur cible configuré",
            description=f"Le serveur **{guild.name}** sera scanné lors du prochain `!utils`.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @utils_config.command(name="channels")
    async def set_channels_output(self, ctx, channel: discord.TextChannel):
        """📺 Définir le channel de sortie pour les salons"""
        await self.config.channels_output.set(channel.id)
        
        embed = discord.Embed(
            title="✅ Channel salons configuré",
            description=f"Les salons seront publiés dans {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @utils_config.command(name="roles")
    async def set_roles_output(self, ctx, channel: discord.TextChannel):
        """🏷️ Définir le channel de sortie pour les rôles"""
        await self.config.roles_output.set(channel.id)
        
        embed = discord.Embed(
            title="✅ Channel rôles configuré",
            description=f"Les rôles seront publiés dans {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @utils_config.command(name="emojis")
    async def set_emojis_output(self, ctx, channel: discord.TextChannel):
        """😀 Définir le channel de sortie pour les emojis"""
        await self.config.emojis_output.set(channel.id)
        
        embed = discord.Embed(
            title="✅ Channel emojis configuré",
            description=f"Les emojis seront publiés dans {channel.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @utils_config.command(name="show")
    async def show_config(self, ctx):
        """📋 Afficher la configuration actuelle"""
        target_server_id = await self.config.target_server_id()
        channels_output = await self.config.channels_output()
        roles_output = await self.config.roles_output()
        emojis_output = await self.config.emojis_output()
        
        target_guild = self.bot.get_guild(target_server_id)
        channels_channel = self.bot.get_channel(channels_output)
        roles_channel = self.bot.get_channel(roles_output)
        emojis_channel = self.bot.get_channel(emojis_output)
        
        embed = discord.Embed(
            title="⚙️ Configuration Utils",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(
            name="🎯 Serveur cible",
            value=f"**{target_guild.name}** ({target_server_id})" if target_guild else f"Introuvable ({target_server_id})",
            inline=False
        )
        
        embed.add_field(
            name="📺 Channel salons",
            value=channels_channel.mention if channels_channel else f"Introuvable ({channels_output})",
            inline=True
        )
        
        embed.add_field(
            name="🏷️ Channel rôles",
            value=roles_channel.mention if roles_channel else f"Introuvable ({roles_output})",
            inline=True
        )
        
        embed.add_field(
            name="😀 Channel emojis",
            value=emojis_channel.mention if emojis_channel else f"Introuvable ({emojis_output})",
            inline=True
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utils(bot))

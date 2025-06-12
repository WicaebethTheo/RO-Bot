import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import asyncio

class Track(commands.Cog):
    """🔍 Système de tracking et logging pour serveur Discord"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        
        default_guild = {
            "track_category_id": None,
            "channels": {
                "messages": None,
                "images": None,
                "deletes": None,
                "voice": None,
                "joins": None,
                "edits": None,
                "leaves": None,
                "roles": None,
                "bans": None,
                "reactions": None
            }
        }
        
        self.config.register_guild(**default_guild)

    @commands.group(name="track")
    @checks.admin_or_permissions(manage_guild=True)
    async def track(self, ctx):
        """🔍 Commandes de gestion du système de tracking"""
        pass

    @track.command(name="setup")
    async def setup_track(self, ctx):
        """🚀 Crée automatiquement la catégorie Track avec tous les channels"""
        
        # Embed de début
        setup_embed = discord.Embed(
            title="🔍 Configuration du système Track",
            description="Création en cours de la catégorie et des channels de logging...",
            color=discord.Color.blue()
        )
        setup_msg = await ctx.send(embed=setup_embed)
        
        try:
            # Créer la catégorie Track
            category = await ctx.guild.create_category(
                name="📊 Track",
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
            )
            
            # Sauvegarder l'ID de la catégorie
            await self.config.guild(ctx.guild).track_category_id.set(category.id)
            
            # Définir les channels à créer
            channels_to_create = [
                ("messages", "💬 Messages", "Logs des messages envoyés"),
                ("images", "🖼️ Images", "Logs des images partagées"),
                ("deletes", "🗑️ Deletes", "Logs des messages supprimés"),
                ("voice", "🎤 Voice", "Logs des événements vocaux"),
                ("joins", "📥 Joins", "Logs des arrivées de membres"),
                ("edits", "✏️ Edits", "Logs des messages modifiés"),
                ("leaves", "📤 Leaves", "Logs des départs de membres"),
                ("roles", "🏷️ Roles", "Logs des modifications de rôles"),
                ("bans", "🔨 Bans", "Logs des bannissements"),
                ("reactions", "😀 Reactions", "Logs des réactions")
            ]
            
            created_channels = {}
            
            # Créer chaque channel
            for channel_key, channel_name, description in channels_to_create:
                channel = await ctx.guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    topic=description,
                    overwrites={
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    }
                )
                created_channels[channel_key] = channel.id
                
                # Petit délai pour éviter le rate limit
                await asyncio.sleep(0.5)
            
            # Sauvegarder tous les IDs des channels
            await self.config.guild(ctx.guild).channels.set(created_channels)
            
            # Embed de succès avec les IDs
            success_embed = discord.Embed(
                title="✅ Système Track configuré !",
                description=f"Catégorie et channels créés dans {category.mention}",
                color=discord.Color.green()
            )
            
            # Ajouter les IDs des channels
            channel_list = ""
            for channel_key, channel_id in created_channels.items():
                channel = ctx.guild.get_channel(channel_id)
                channel_list += f"• {channel.mention} - `{channel_id}`\n"
            
            success_embed.add_field(
                name="📋 Channels créés",
                value=channel_list,
                inline=False
            )
            
            success_embed.add_field(
                name="📊 Catégorie Track",
                value=f"{category.mention} - `{category.id}`",
                inline=False
            )
            
            success_embed.set_footer(text="Tous les IDs ont été sauvegardés dans la configuration")
            
            await setup_msg.edit(embed=success_embed)
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="❌ Permissions insuffisantes",
                description="Je n'ai pas les permissions pour créer des catégories/channels.",
                color=discord.Color.red()
            )
            await setup_msg.edit(embed=error_embed)
        except Exception as e:
            error_embed = discord.Embed(
                title="💥 Erreur",
                description=f"Une erreur s'est produite:\n```{str(e)}```",
                color=discord.Color.red()
            )
            await setup_msg.edit(embed=error_embed)

    @track.command(name="ids")
    async def show_ids(self, ctx):
        """📋 Affiche tous les IDs des channels Track"""
        
        category_id = await self.config.guild(ctx.guild).track_category_id()
        channels = await self.config.guild(ctx.guild).channels()
        
        if not category_id:
            error_embed = discord.Embed(
                title="⚠️ Système non configuré",
                description="Utilisez `!track setup` d'abord pour créer le système.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=error_embed)
        
        # Embed avec tous les IDs
        ids_embed = discord.Embed(
            title="🔍 IDs du système Track",
            color=discord.Color.blue()
        )
        
        # Catégorie
        category = ctx.guild.get_channel(category_id)
        if category:
            ids_embed.add_field(
                name="📊 Catégorie Track",
                value=f"{category.mention}\n`{category_id}`",
                inline=False
            )
        
        # Channels
        if channels:
            channel_list = ""
            for channel_key, channel_id in channels.items():
                if channel_id:
                    channel = ctx.guild.get_channel(channel_id)
                    if channel:
                        channel_list += f"• **{channel_key}**: {channel.mention} - `{channel_id}`\n"
                    else:
                        channel_list += f"• **{channel_key}**: Channel supprimé - `{channel_id}`\n"
            
            if channel_list:
                ids_embed.add_field(
                    name="📋 Channels Track",
                    value=channel_list,
                    inline=False
                )
        
        ids_embed.set_footer(text="Copiez ces IDs pour configurer d'autres bots/cogs")
        
        await ctx.send(embed=ids_embed)

    @track.command(name="reset")
    async def reset_track(self, ctx):
        """🔄 Supprime et recrée tout le système Track"""
        
        # Demande de confirmation
        confirm_embed = discord.Embed(
            title="⚠️ Confirmation requise",
            description="Cette action va supprimer tous les channels Track existants et les recréer.\n\n"
                       "Êtes-vous sûr ? Tapez `confirmer` pour continuer.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=confirm_embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            response = await self.bot.wait_for("message", check=check, timeout=30.0)
            if response.content.lower() != "confirmer":
                return await ctx.send("❌ Opération annulée.")
            
            # Supprimer les channels existants
            category_id = await self.config.guild(ctx.guild).track_category_id()
            if category_id:
                category = ctx.guild.get_channel(category_id)
                if category:
                    # Supprimer tous les channels de la catégorie
                    for channel in category.channels:
                        try:
                            await channel.delete()
                            await asyncio.sleep(0.5)
                        except:
                            pass
                    
                    # Supprimer la catégorie
                    try:
                        await category.delete()
                    except:
                        pass
            
            # Réinitialiser la config
            await self.config.guild(ctx.guild).clear()
            
            # Recréer le système
            await self.setup_track(ctx)
            
        except asyncio.TimeoutError:
            await ctx.send("❌ Temps écoulé. Opération annulée.")

    @track.command(name="status")
    async def track_status(self, ctx):
        """📊 Affiche le statut du système Track"""
        
        category_id = await self.config.guild(ctx.guild).track_category_id()
        channels = await self.config.guild(ctx.guild).channels()
        
        status_embed = discord.Embed(
            title="📊 Statut du système Track",
            color=discord.Color.blue()
        )
        
        # Vérifier la catégorie
        if category_id:
            category = ctx.guild.get_channel(category_id)
            if category:
                status_embed.add_field(
                    name="📊 Catégorie",
                    value=f"✅ {category.mention}",
                    inline=True
                )
            else:
                status_embed.add_field(
                    name="📊 Catégorie",
                    value="❌ Supprimée",
                    inline=True
                )
        else:
            status_embed.add_field(
                name="📊 Catégorie",
                value="⚠️ Non configurée",
                inline=True
            )
        
        # Vérifier les channels
        if channels:
            active_channels = 0
            total_channels = len(channels)
            
            for channel_key, channel_id in channels.items():
                if channel_id and ctx.guild.get_channel(channel_id):
                    active_channels += 1
            
            status_embed.add_field(
                name="📋 Channels",
                value=f"✅ {active_channels}/{total_channels} actifs",
                inline=True
            )
        else:
            status_embed.add_field(
                name="📋 Channels",
                value="⚠️ Aucun configuré",
                inline=True
            )
        
        # Recommandations
        if not category_id or not channels:
            status_embed.add_field(
                name="💡 Recommandation",
                value="Utilisez `!track setup` pour configurer le système",
                inline=False
            )
        
        await ctx.send(embed=status_embed)

async def setup(bot):
    await bot.add_cog(Track(bot)) 
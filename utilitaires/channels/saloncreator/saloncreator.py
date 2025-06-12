import discord
from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import humanize_list
import asyncio
from typing import Optional


class SalonCreator(commands.Cog):
    """Cog pour créer automatiquement tous les salons Discord avec leurs émojis"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)
        
        # Structure complète des salons avec émojis
        self.server_structure = {
            "Bienvenue": {
                "emoji": "👋",
                "channels": [
                    {"name": "bienvenue", "emoji": "📘", "type": "text"},
                    {"name": "règlement", "emoji": "📜", "type": "text"},
                    {"name": "auto-rôles", "emoji": "📁", "type": "text"},
                    {"name": "support", "emoji": "🚩", "type": "text"},
                    {"name": "recrutements", "emoji": "📧", "type": "text"},
                    {"name": "nous-soutenir", "emoji": "✨", "type": "text"}
                ]
            },
            "Informations": {
                "emoji": "ℹ️",
                "channels": [
                    {"name": "annonces", "emoji": "📢", "type": "text"},
                    {"name": "giveaways", "emoji": "🎉", "type": "text"},
                    {"name": "tournois", "emoji": "🏆", "type": "text"},
                    {"name": "soutiens", "emoji": "🔔", "type": "text"},
                    {"name": "sondages", "emoji": "📊", "type": "text"}
                ]
            },
            "Communauté": {
                "emoji": "👥",
                "channels": [
                    {"name": "clip-pp", "emoji": "🧠", "type": "text"},
                    {"name": "ranked", "emoji": "🌱", "type": "text"},
                    {"name": "suggestions", "emoji": "🗨️", "type": "text"},
                    {"name": "commandes", "emoji": "💻", "type": "text"},
                    {"name": "vos-réseaux", "emoji": "🧡", "type": "text"}
                ]
            },
            "Time 2 Chill": {
                "emoji": "😎",
                "channels": [
                    {"name": "time2cook", "emoji": "👨‍🍳", "type": "text"},
                    {"name": "time2draw", "emoji": "🎨", "type": "text"},
                    {"name": "time2read", "emoji": "📖", "type": "text"},
                    {"name": "time2watch", "emoji": "👀", "type": "text"},
                    {"name": "time2play", "emoji": "🎮", "type": "text"}
                ]
            },
            "PARTIES PERSO": {
                "emoji": "🎮",
                "channels": [
                    {"name": "parties-perso", "emoji": "🟢", "type": "text"},
                    {"name": "règlement-pp", "emoji": "📋", "type": "text"},
                    {"name": "roulette-maps", "emoji": "👑", "type": "text"},
                    {"name": "party-code", "emoji": "🚩", "type": "text"},
                    {"name": "party-code-staff", "emoji": "🚩", "type": "text"},
                    {"name": "demande-organisateur", "emoji": "🚩", "type": "text"}
                ]
            },
            "Show Matchs": {
                "emoji": "📺",
                "channels": [
                    {"name": "Préparation 1", "emoji": "🎭", "type": "voice"},
                    {"name": "Attaque", "emoji": "🎭", "type": "voice"},
                    {"name": "Défense", "emoji": "🎭", "type": "voice"}
                ]
            },
            "SUPPORT": {
                "emoji": "🛠️",
                "channels": [
                    {"name": "annonce-importante", "emoji": "📣", "type": "text"},
                    {"name": "signalements", "emoji": "⚠️", "type": "text"},
                    {"name": "screenshot", "emoji": "", "type": "text"},
                    {"name": "discussion-staff", "emoji": "⚠️", "type": "text"},
                    {"name": "compte-rendu", "emoji": "⚠️", "type": "text"},
                    {"name": "comment-sanctionner", "emoji": "⚠️", "type": "text"},
                    {"name": "sanction", "emoji": "⚠️", "type": "text"},
                    {"name": "record-potentiel-cheat", "emoji": "⚠️", "type": "text"},
                    {"name": "giveaway", "emoji": "🎉", "type": "text"},
                    {"name": "historique-sanction", "emoji": "⚠️", "type": "text"},
                    {"name": "ancien-tickets", "emoji": "🎫", "type": "text"},
                    {"name": "headstaff", "emoji": "⚠️", "type": "text"},
                    {"name": "graphismes", "emoji": "⚠️", "type": "text"},
                    {"name": "inscription-tournoi", "emoji": "⚠️", "type": "text"},
                    {"name": "demande-web", "emoji": "⚠️", "type": "text"},
                    {"name": "rank-radiant", "emoji": "⚠️", "type": "text"},
                    {"name": "stats-staff", "emoji": "⚠️", "type": "text"},
                    {"name": "Entretien", "emoji": "💬", "type": "voice"},
                    {"name": "Staff", "emoji": "🔒", "type": "voice"},
                    {"name": "réunion", "emoji": "📊", "type": "voice"}
                ]
            }
        }

    @commands.group(name="salon", invoke_without_command=True)
    @commands.admin_or_permissions(manage_guild=True)
    async def salon_group(self, ctx):
        """Commandes pour gérer les salons"""
        await ctx.send_help(ctx.command)

    @salon_group.command(name="create")
    @commands.admin_or_permissions(manage_guild=True)
    async def create_all_channels(self, ctx, *, confirmation: str = None):
        """
        Crée tous les salons et catégories du serveur avec leurs émojis
        
        Utilisez `[p]salon create CONFIRMER` pour confirmer la création
        """
        if confirmation != "CONFIRMER":
            embed = discord.Embed(
                title="⚠️ Confirmation requise",
                description=(
                    "Cette commande va créer toute la structure de salons du serveur.\n"
                    f"Pour confirmer, utilisez: `{ctx.prefix}salon create CONFIRMER`\n\n"
                    "**Structure qui sera créée:**\n"
                    + "\n".join([f"📁 **{cat}** ({len(data['channels'])} salons)" 
                               for cat, data in self.server_structure.items()])
                ),
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Confirmation reçue, procéder à la création
        embed = discord.Embed(
            title="🚀 Création des salons en cours...",
            description="La création de tous les salons a commencé. Cela peut prendre quelques minutes.",
            color=discord.Color.blue()
        )
        status_msg = await ctx.send(embed=embed)

        created_categories = 0
        created_channels = 0
        errors = []

        try:
            for category_name, category_data in self.server_structure.items():
                try:
                    # Vérifier si la catégorie existe déjà
                    existing_category = discord.utils.get(ctx.guild.categories, name=category_name)
                    
                    if existing_category:
                        category = existing_category
                    else:
                        # Créer la catégorie
                        category = await ctx.guild.create_category(category_name)
                        created_categories += 1
                    
                    # Créer les salons dans cette catégorie
                    for channel_data in category_data["channels"]:
                        channel_name = f"{channel_data['emoji']}-{channel_data['name']}" if channel_data['emoji'] else channel_data['name']
                        
                        # Vérifier si le salon existe déjà
                        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
                        
                        if existing_channel:
                            continue
                        
                        if channel_data["type"] == "voice":
                            await ctx.guild.create_voice_channel(
                                channel_name,
                                category=category
                            )
                        else:
                            await ctx.guild.create_text_channel(
                                channel_name,
                                category=category
                            )
                        
                        created_channels += 1
                        
                        # Petite pause pour éviter les limites de rate
                        await asyncio.sleep(0.5)
                
                except Exception as e:
                    errors.append(f"Erreur avec la catégorie {category_name}: {str(e)}")
                    continue
                
                # Mise à jour du statut
                embed = discord.Embed(
                    title="🚀 Création en cours...",
                    description=f"Catégories créées: {created_categories}\nSalons créés: {created_channels}",
                    color=discord.Color.blue()
                )
                await status_msg.edit(embed=embed)

        except Exception as e:
            errors.append(f"Erreur générale: {str(e)}")

        # Message final
        if errors:
            embed = discord.Embed(
                title="⚠️ Création terminée avec erreurs",
                description=(
                    f"**Résultat:**\n"
                    f"✅ Catégories créées: {created_categories}\n"
                    f"✅ Salons créés: {created_channels}\n\n"
                    f"**Erreurs ({len(errors)}):**\n" + "\n".join(errors[:5])
                ),
                color=discord.Color.orange()
            )
        else:
            embed = discord.Embed(
                title="✅ Création terminée avec succès !",
                description=(
                    f"**Résultat:**\n"
                    f"✅ Catégories créées: {created_categories}\n"
                    f"✅ Salons créés: {created_channels}\n\n"
                    f"Tous les salons ont été créés avec leurs émojis correspondants !"
                ),
                color=discord.Color.green()
            )
        
        await status_msg.edit(embed=embed)

    @salon_group.command(name="structure")
    async def show_structure(self, ctx):
        """Affiche la structure complète qui sera créée"""
        embed = discord.Embed(
            title="📋 Structure des salons",
            description="Voici la structure complète qui sera créée:",
            color=discord.Color.blue()
        )
        
        for category_name, category_data in self.server_structure.items():
            channels_list = []
            for channel in category_data["channels"]:
                channel_type = "🔊" if channel["type"] == "voice" else "💬"
                emoji = channel["emoji"] if channel["emoji"] else ""
                channels_list.append(f"{channel_type} {emoji}-{channel['name']}")
            
            embed.add_field(
                name=f"📁 {category_name}",
                value="\n".join(channels_list[:10]) + ("\n..." if len(channels_list) > 10 else ""),
                inline=False
            )
        
        await ctx.send(embed=embed)

    @salon_group.command(name="clean")
    @commands.admin_or_permissions(manage_guild=True)
    async def clean_channels(self, ctx, *, confirmation: str = None):
        """
        Supprime tous les salons et catégories vides du serveur
        
        Utilisez `[p]salon clean CONFIRMER` pour confirmer la suppression
        """
        if confirmation != "CONFIRMER":
            embed = discord.Embed(
                title="⚠️ Confirmation requise",
                description=(
                    "Cette commande va supprimer toutes les catégories vides du serveur.\n"
                    f"Pour confirmer, utilisez: `{ctx.prefix}salon clean CONFIRMER`"
                ),
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        deleted_categories = 0
        deleted_channels = 0
        
        # Supprimer les catégories vides
        for category in ctx.guild.categories:
            if not category.channels:
                try:
                    await category.delete()
                    deleted_categories += 1
                except:
                    pass

        embed = discord.Embed(
            title="🗑️ Nettoyage terminé",
            description=f"✅ Catégories vides supprimées: {deleted_categories}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed) 
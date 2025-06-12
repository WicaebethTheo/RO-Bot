import discord
from redbot.core import commands
import asyncio

class Boot(commands.Cog):
    """🚀 Système de boot pour restaurer tous les boutons persistants après un crash"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="boot")
    @commands.has_permissions(manage_guild=True)
    async def boot_system(self, ctx):
        """🚀 Lance tous les systèmes de setup pour restaurer les boutons persistants"""
        
        # Message de démarrage
        boot_embed = discord.Embed(
            title="🚀 Démarrage du système de boot",
            description="Restauration de tous les boutons persistants en cours...",
            color=0x00FF00
        )
        boot_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        boot_message = await ctx.send(embed=boot_embed)
        
        # Liste des commandes à exécuter
        setup_commands = [
            ("reglement", "publier", "📋 Règlement général"),
            ("reglementpp", "setup", "📜 Règlement parties personnalisées"),
            ("tickets", "setup", "🎫 Système de tickets"),
            ("autoroles", "setup", "🎮 Auto-rôles Valorant"), 
            ("setup_demande", None, "📢 Système de demande d'orga")
        ]
        
        success_count = 0
        error_count = 0
        results = []
        
        for i, (command_name, subcommand, description) in enumerate(setup_commands, 1):
            try:
                # Mettre à jour le statut
                progress_embed = discord.Embed(
                    title="🚀 Boot en cours...",
                    description=f"**Étape {i}/{len(setup_commands)}**\n\n"
                               f"🔄 Exécution: {description}\n"
                               f"📝 Commande: `!{command_name}{' ' + subcommand if subcommand else ''}`",
                    color=0xFFA500
                )
                progress_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
                
                # Ajouter les résultats précédents
                if results:
                    status_text = "\n".join(results[-3:])  # Afficher les 3 derniers
                    progress_embed.add_field(name="📊 Résultats récents", value=status_text, inline=False)
                
                await boot_message.edit(embed=progress_embed)
                
                # Exécuter la commande
                command_obj = self.bot.get_command(command_name)
                if command_obj:
                    if subcommand:
                        # Commande avec sous-commande
                        subcommand_obj = command_obj.get_command(subcommand)
                        if subcommand_obj:
                            await subcommand_obj.invoke(ctx)
                        else:
                            raise Exception(f"Sous-commande '{subcommand}' introuvable")
                    else:
                        # Commande simple
                        await command_obj.invoke(ctx)
                    
                    results.append(f"✅ {description}")
                    success_count += 1
                else:
                    results.append(f"❌ {description} (Commande introuvable)")
                    error_count += 1
                
                # Pause entre les commandes
                await asyncio.sleep(3)
                
            except Exception as e:
                results.append(f"❌ {description} (Erreur)")
                error_count += 1
                print(f"Erreur lors de l'exécution de {command_name}: {e}")
                continue
        
        # Message final
        if error_count == 0:
            final_color = 0x00FF00  # Vert
            final_title = "🎉 Boot terminé avec succès !"
            final_description = f"Tous les systèmes ont été restaurés ({success_count}/{len(setup_commands)})"
        elif success_count > 0:
            final_color = 0xFFA500  # Orange
            final_title = "⚠️ Boot terminé avec des erreurs"
            final_description = f"Systèmes restaurés: {success_count}/{len(setup_commands)}\nErreurs: {error_count}"
        else:
            final_color = 0xFF0000  # Rouge
            final_title = "❌ Échec du boot"
            final_description = f"Aucun système n'a pu être restauré (Erreurs: {error_count})"
        
        final_embed = discord.Embed(
            title=final_title,
            description=final_description,
            color=final_color
        )
        final_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        # Ajouter le détail des résultats
        status_text = "\n".join(results)
        final_embed.add_field(name="📊 Résultats détaillés", value=status_text, inline=False)
        
        final_embed.add_field(
            name="ℹ️ Information",
            value="Tous les boutons persistants ont été réinitialisés.\n"
                  "Les interfaces sont maintenant opérationnelles.",
            inline=False
        )
        
        final_embed.set_footer(text="Boot système terminé - Radiant Order")
        
        await boot_message.edit(embed=final_embed)

    @boot_system.error
    async def boot_error(self, ctx, error):
        """Gestion des erreurs du boot"""
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                title="❌ Permissions insuffisantes",
                description="Vous devez avoir les permissions `manage_guild` pour utiliser cette commande.",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="❌ Erreur système",
                description=f"Une erreur s'est produite lors du boot:\n```{str(error)}```",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)

    @commands.command(name="bootinfo")
    async def boot_info(self, ctx):
        """ℹ️ Informations sur le système de boot"""
        info_embed = discord.Embed(
            title="🚀 Système de Boot - Informations",
            description="Le système de boot affiche la liste des commandes à exécuter pour restaurer tous les boutons persistants après un crash du bot.",
            color=0x00B0F4
        )
        
        info_embed.add_field(
            name="📋 Commandes affichées",
            value="• 📋 **Règlement général** - `!reglement publier`\n"
                  "• 📜 **Règlement PP** - `!reglementpp publier`\n"
                  "• 🎫 **Système de tickets** - `!ticket setup`\n"
                  "• 🎮 **Auto-rôles Valorant** - `!autoroles setup`\n"
                  "• 📢 **Demande d'orga** - `!setup_demande`",
            inline=False
        )
        
        info_embed.add_field(
            name="🎯 Utilisation",
            value="```!boot``` - Affiche le guide de restauration\n"
                  "```!bootinfo``` - Affiche cette aide",
            inline=False
        )
        
        info_embed.add_field(
            name="⚠️ Important",
            value="• Commande réservée aux administrateurs\n"
                  "• Utilisez après un crash ou redémarrage\n"
                  "• Exécutez les commandes manuellement\n"
                  "• Ordre d'exécution important",
            inline=False
        )
        
        info_embed.set_footer(text="Radiant Order - Système de Boot")
        if ctx.guild.icon:
            info_embed.set_thumbnail(url=ctx.guild.icon.url)
        
        await ctx.send(embed=info_embed)

async def setup(bot):
    await bot.add_cog(Boot(bot))

import discord
from redbot.core import commands, checks
from redbot.core.bot import Red
import asyncio
from datetime import timedelta

class Clear(commands.Cog):
    """🧹 Commandes de nettoyage des messages"""

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge", "clean"])
    @checks.mod_or_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 10):
        """🧹 Nettoie les messages du channel actuel
        
        **Usage :**
        - `!clear` - Supprime 10 messages par défaut
        - `!clear 50` - Supprime 50 messages
        - `!clear 200` - Supprime 200 messages (maximum)
        
        **Permissions requises :** Gérer les messages
        """
        
        # Vérifications des limites
        if amount < 1:
            return await ctx.send("❌ Le nombre de messages doit être supérieur à 0.", delete_after=5)
        
        if amount > 200:
            return await ctx.send("❌ Je ne peux pas supprimer plus de 200 messages à la fois.", delete_after=5)
        
        # Vérifier les permissions du bot
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            return await ctx.send("❌ Je n'ai pas la permission de gérer les messages dans ce channel.", delete_after=5)
        
        try:
            # Message de confirmation avant suppression
            confirm_msg = await ctx.send(f"🧹 Suppression de {amount} messages en cours...")
            
            # Supprimer les messages (Discord limite à 14 jours)
            cutoff_date = discord.utils.utcnow() - timedelta(days=14)
            
            # Récupérer les messages à supprimer
            messages_to_delete = []
            async for message in ctx.channel.history(limit=amount + 1):  # +1 pour inclure la commande
                if message.created_at > cutoff_date:
                    messages_to_delete.append(message)
                else:
                    break
            
            # Supprimer les messages par batch (Discord limite à 100 par batch)
            deleted_count = 0
            
            # Supprimer par chunks de 100 messages max
            while messages_to_delete:
                chunk = messages_to_delete[:100]
                messages_to_delete = messages_to_delete[100:]
                
                if len(chunk) == 1:
                    # Un seul message - suppression individuelle
                    await chunk[0].delete()
                    deleted_count += 1
                else:
                    # Plusieurs messages - suppression en lot
                    await ctx.channel.delete_messages(chunk)
                    deleted_count += len(chunk)
                
                # Pause pour éviter le rate limit
                if messages_to_delete:
                    await asyncio.sleep(1)
            
            # Message de confirmation
            if deleted_count > 0:
                success_embed = discord.Embed(
                    title="🧹 Nettoyage terminé !",
                    description=f"**{deleted_count}** messages supprimés avec succès.",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                success_embed.set_footer(text=f"Nettoyage effectué par {ctx.author.display_name}")
                
                final_msg = await ctx.send(embed=success_embed)
                
                # Supprimer le message de confirmation après 10 secondes
                await asyncio.sleep(10)
                try:
                    await final_msg.delete()
                except:
                    pass
            else:
                await ctx.send("⚠️ Aucun message récent trouvé à supprimer.", delete_after=5)
        
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions nécessaires pour supprimer ces messages.", delete_after=5)
        
        except discord.HTTPException as e:
            await ctx.send(f"❌ Erreur lors de la suppression des messages: {str(e)}", delete_after=5)
        
        except Exception as e:
            await ctx.send(f"❌ Une erreur inattendue s'est produite: {str(e)}", delete_after=5)

    @commands.command(name="clearuser", aliases=["purgeuser"])
    @checks.mod_or_permissions(manage_messages=True)
    async def clear_user_messages(self, ctx, user: discord.Member, amount: int = 50):
        """🧹 Nettoie les messages d'un utilisateur spécifique
        
        **Usage :**
        - `!clearuser @utilisateur` - Supprime 50 messages de l'utilisateur
        - `!clearuser @utilisateur 20` - Supprime 20 messages de l'utilisateur
        
        **Permissions requises :** Gérer les messages
        """
        
        if amount < 1:
            return await ctx.send("❌ Le nombre de messages doit être supérieur à 0.", delete_after=5)
        
        if amount > 100:
            return await ctx.send("❌ Je ne peux pas chercher plus de 100 messages à la fois.", delete_after=5)
        
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            return await ctx.send("❌ Je n'ai pas la permission de gérer les messages dans ce channel.", delete_after=5)
        
        try:
            confirm_msg = await ctx.send(f"🧹 Recherche des messages de {user.mention}...")
            
            # Fonction pour vérifier si le message appartient à l'utilisateur
            def check_user(message):
                return message.author == user
            
            # Supprimer les messages de l'utilisateur
            deleted = await ctx.channel.purge(limit=amount * 3, check=check_user, before=ctx.message)
            
            # Supprimer le message de confirmation
            try:
                await confirm_msg.delete()
            except:
                pass
            
            if deleted:
                success_embed = discord.Embed(
                    title="🧹 Nettoyage utilisateur terminé !",
                    description=f"**{len(deleted)}** messages de {user.mention} supprimés.",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                success_embed.set_footer(text=f"Nettoyage effectué par {ctx.author.display_name}")
                
                final_msg = await ctx.send(embed=success_embed)
                await asyncio.sleep(10)
                try:
                    await final_msg.delete()
                except:
                    pass
            else:
                await ctx.send(f"⚠️ Aucun message récent de {user.mention} trouvé.", delete_after=5)
        
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions nécessaires.", delete_after=5)
        
        except Exception as e:
            await ctx.send(f"❌ Erreur: {str(e)}", delete_after=5)

    @commands.command(name="clearbot", aliases=["purgebots"])
    @checks.mod_or_permissions(manage_messages=True)
    async def clear_bot_messages(self, ctx, amount: int = 50):
        """🧹 Nettoie les messages des bots
        
        **Usage :**
        - `!clearbot` - Supprime 50 messages de bots
        - `!clearbot 30` - Supprime 30 messages de bots
        
        **Permissions requises :** Gérer les messages
        """
        
        if amount < 1:
            return await ctx.send("❌ Le nombre de messages doit être supérieur à 0.", delete_after=5)
        
        if amount > 100:
            return await ctx.send("❌ Je ne peux pas chercher plus de 100 messages à la fois.", delete_after=5)
        
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            return await ctx.send("❌ Je n'ai pas la permission de gérer les messages dans ce channel.", delete_after=5)
        
        try:
            confirm_msg = await ctx.send("🧹 Recherche des messages de bots...")
            
            # Fonction pour vérifier si le message provient d'un bot
            def check_bot(message):
                return message.author.bot
            
            # Supprimer les messages des bots
            deleted = await ctx.channel.purge(limit=amount * 2, check=check_bot, before=ctx.message)
            
            # Supprimer le message de confirmation
            try:
                await confirm_msg.delete()
            except:
                pass
            
            if deleted:
                success_embed = discord.Embed(
                    title="🧹 Nettoyage bots terminé !",
                    description=f"**{len(deleted)}** messages de bots supprimés.",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                success_embed.set_footer(text=f"Nettoyage effectué par {ctx.author.display_name}")
                
                final_msg = await ctx.send(embed=success_embed)
                await asyncio.sleep(10)
                try:
                    await final_msg.delete()
                except:
                    pass
            else:
                await ctx.send("⚠️ Aucun message de bot récent trouvé.", delete_after=5)
        
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions nécessaires.", delete_after=5)
        
        except Exception as e:
            await ctx.send(f"❌ Erreur: {str(e)}", delete_after=5)

    @clear_messages.error
    async def clear_error(self, ctx, error):
        """Gestion des erreurs pour la commande clear"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas la permission de gérer les messages.", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Le nombre de messages doit être un nombre entier.", delete_after=5)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ Tu n'as pas les permissions nécessaires pour cette commande.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Clear(bot))

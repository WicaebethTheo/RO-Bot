import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import asyncio
from datetime import datetime, timedelta
from typing import Optional

class BanSystem(commands.Cog):
    """⚖️ Système de modération avec avertissements progressifs"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=789456123987)
        
        default_guild = {
            "user_warnings": {},  # {user_id: {"count": int, "last_warning": timestamp}}
            "authorized_roles": [1381222157929025626, 1381221330971656222, 1380562058461839400, 1380638962632229054],
            "log_channel_id": 1380560668897443971,  # Channel pour les logs de sanctions
            "avert_role_1": 1380609403694088212,  # ID du rôle "Avert 1"
            "avert_role_2": 1380609528239882332,  # ID du rôle "Avert 2"
            "avert_role_3": 1380625102940667925   # ID du rôle "Avert 3" (optionnel)
        }
        
        self.config.register_guild(**default_guild)

    def has_moderation_role():
        """Vérifie si l'utilisateur a un rôle autorisé ou est Wicaebeth"""
        async def predicate(ctx):
            # Vérifier si c'est Wicaebeth (accès spécial)
            if ctx.author.id == 257152912776495104:
                return True
            
            guild_config = ctx.cog.config.guild(ctx.guild)
            authorized_roles = await guild_config.authorized_roles()
            
            for role_id in authorized_roles:
                role = ctx.guild.get_role(role_id)
                if role and role in ctx.author.roles:
                    return True
            
            raise commands.CheckFailure("Vous n'avez pas les permissions pour utiliser cette commande.")
        
        return commands.check(predicate)

    async def get_current_warning_level(self, member: discord.Member):
        """Détermine le niveau d'avertissement actuel basé sur les rôles"""
        guild_config = self.config.guild(member.guild)
        avert_role_1_id = await guild_config.avert_role_1()
        avert_role_2_id = await guild_config.avert_role_2()
        avert_role_3_id = await guild_config.avert_role_3()
        
        # Vérifier les rôles d'avertissement
        has_avert_1 = False
        has_avert_2 = False
        has_avert_3 = False
        
        if avert_role_1_id:
            avert_role_1 = member.guild.get_role(avert_role_1_id)
            if avert_role_1 and avert_role_1 in member.roles:
                has_avert_1 = True
        
        if avert_role_2_id:
            avert_role_2 = member.guild.get_role(avert_role_2_id)
            if avert_role_2 and avert_role_2 in member.roles:
                has_avert_2 = True
        
        if avert_role_3_id:
            avert_role_3 = member.guild.get_role(avert_role_3_id)
            if avert_role_3 and avert_role_3 in member.roles:
                has_avert_3 = True
        
        # Déterminer le niveau actuel
        if has_avert_3:
            return 3  # Déjà avert 3, prochaine sanction = ban
        elif has_avert_2:
            return 2  # Déjà avert 2, prochaine sanction = ban
        elif has_avert_1:
            return 1  # Déjà avert 1, prochaine sanction = avert 2
        else:
            return 0  # Aucun avertissement, prochaine sanction = avert 1

    async def apply_warning_role(self, member: discord.Member, warning_level: int, reason: str):
        """Applique ou met à jour les rôles d'avertissement"""
        guild_config = self.config.guild(member.guild)
        avert_role_1_id = await guild_config.avert_role_1()
        avert_role_2_id = await guild_config.avert_role_2()
        avert_role_3_id = await guild_config.avert_role_3()
        
        roles_to_add = []
        roles_to_remove = []
        
        if warning_level == 1 and avert_role_1_id:
            avert_role_1 = member.guild.get_role(avert_role_1_id)
            if avert_role_1:
                roles_to_add.append(avert_role_1)
        
        elif warning_level == 2:
            # Pour avert 2, ajouter avert 2 et retirer avert 1
            if avert_role_2_id:
                avert_role_2 = member.guild.get_role(avert_role_2_id)
                if avert_role_2:
                    roles_to_add.append(avert_role_2)
            
            if avert_role_1_id:
                avert_role_1 = member.guild.get_role(avert_role_1_id)
                if avert_role_1 and avert_role_1 in member.roles:
                    roles_to_remove.append(avert_role_1)
        
        # Pour le ban (niveau 3), retirer tous les rôles d'avertissement
        elif warning_level >= 3:
            if avert_role_1_id:
                avert_role_1 = member.guild.get_role(avert_role_1_id)
                if avert_role_1 and avert_role_1 in member.roles:
                    roles_to_remove.append(avert_role_1)
            
            if avert_role_2_id:
                avert_role_2 = member.guild.get_role(avert_role_2_id)
                if avert_role_2 and avert_role_2 in member.roles:
                    roles_to_remove.append(avert_role_2)
            
            if avert_role_3_id:
                avert_role_3 = member.guild.get_role(avert_role_3_id)
                if avert_role_3 and avert_role_3 in member.roles:
                    roles_to_remove.append(avert_role_3)
        
        # Appliquer les changements de rôles
        try:
            if roles_to_add:
                await member.add_roles(*roles_to_add, reason=f"Avertissement {warning_level} - {reason}")
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove, reason=f"Mise à jour avertissement {warning_level} - {reason}")
        except discord.Forbidden:
            print(f"[SANCTION SYSTEM] Impossible de modifier les rôles de {member.name}")
        except Exception as e:
            print(f"[SANCTION SYSTEM] Erreur lors de la modification des rôles: {str(e)}")

    async def send_sanction_log(self, ctx, member, warning_count, action_taken, raison, mp_sent):
        """Envoie un log de la sanction dans le channel configuré"""
        guild_config = self.config.guild(ctx.guild)
        log_channel_id = await guild_config.log_channel_id()
        
        if not log_channel_id:
            return
        
        log_channel = ctx.guild.get_channel(log_channel_id)
        if not log_channel:
            return
        
        try:
            # Déterminer la couleur selon le niveau
            colors = {
                1: discord.Color.orange(),
                2: discord.Color.red(), 
                3: discord.Color.dark_red()
            }
            embed_color = colors.get(warning_count, discord.Color.gray())
            
            # Déterminer l'emoji selon le niveau
            emojis = {
                1: "🕐",
                2: "🕐", 
                3: "🔒"
            }
            status_emoji = emojis.get(warning_count, "⚖️")
            
            embed = discord.Embed(
                title=f"{status_emoji} Sanction Appliquée",
                description=f"**Membre sanctionné**: {member.mention} ({member.name})\n"
                           f"**Avertissement**: {warning_count}/3\n"
                           f"**Action**: {action_taken}\n"
                           f"**Raison**: {raison}",
                color=embed_color,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="👤 Détails",
                value=f"**ID Membre**: {member.id}\n"
                      f"**Modérateur**: {ctx.author.mention}\n"
                      f"**Canal**: {ctx.channel.mention}\n"
                      f"**MP envoyé**: {'✅ Oui' if mp_sent else '❌ Non'}",
                inline=True
            )
            
            if warning_count < 3:
                next_actions = {1: "Timeout 1 semaine", 2: "Ban définitif"}
                embed.add_field(
                    name="⚠️ Prochain avertissement",
                    value=f"**{warning_count + 1}**: {next_actions.get(warning_count, 'N/A')}",
                    inline=True
                )
            
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text="Radiant Order - Logs de Modération")
            
            await log_channel.send(embed=embed)
            
        except Exception as e:
            print(f"[SANCTION SYSTEM] Erreur lors de l'envoi du log: {str(e)}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Gère les rejointes de membres avec avertissements (pour information seulement)"""
        guild_config = self.config.guild(member.guild)
        user_warnings = await guild_config.user_warnings()
        
        # Vérifier si le membre avait des avertissements précédents
        if str(member.id) in user_warnings:
            user_data = user_warnings[str(member.id)]
            warning_count = user_data.get("count", 0)
            
            if warning_count > 0:
                # Log de l'information (le membre ne devrait pas pouvoir revenir s'il était banni)
                print(f"[BAN SYSTEM] Retour d'un membre avec {warning_count} avertissement(s): {member.name} ({member.id})")
                
                # Chercher un salon de logs pour notifier
                for channel in member.guild.channels:
                    if "mod" in channel.name.lower() or "log" in channel.name.lower():
                        try:
                            embed = discord.Embed(
                                title="⚠️ Retour de Membre avec Avertissements",
                                description=f"{member.mention} est revenu sur le serveur.",
                                color=discord.Color.orange(),
                                timestamp=discord.utils.utcnow()
                            )
                            embed.add_field(name="👤 Membre", value=f"{member.name} ({member.id})", inline=True)
                            embed.add_field(name="📊 Avertissements", value=f"{warning_count}/3", inline=True)
                            embed.set_footer(text="Radiant Order - Système de Modération")
                            
                            await channel.send(embed=embed)
                            break
                        except:
                            continue

    @commands.group(name="sanction")
    @has_moderation_role()
    async def sanction_group(self, ctx):
        """⚖️ Système de sanctions avec avertissements progressifs"""
        if ctx.invoked_subcommand is None:
            await self.show_sanction_help(ctx)

    @sanction_group.command(name="user")
    async def sanction_user(self, ctx, member: discord.Member, *, raison: str):
        """🔨 Sanctionner un utilisateur avec système d'avertissements
        
        Avertissement 1: Timeout 1 jour + Rôle Avert 1
        Avertissement 2: Timeout 1 semaine + Rôle Avert 2
        Avertissement 3: Ban définitif
        
        La raison est OBLIGATOIRE pour toutes les sanctions.
        """
        
        # Vérifier que l'utilisateur ne se ban pas lui-même
        if member == ctx.author:
            return await ctx.send("❌ Vous ne pouvez pas vous bannir vous-même.")
        
        # Vérifier la hiérarchie des rôles
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("❌ Vous ne pouvez pas bannir quelqu'un ayant un rôle égal ou supérieur au vôtre.")
        
        # Vérifier le niveau d'avertissement actuel basé sur les rôles
        current_warning_level = await self.get_current_warning_level(member)
        
        # Déterminer le nouveau niveau d'avertissement
        new_warning_level = current_warning_level + 1
        
        # Récupérer les données de l'utilisateur pour mise à jour
        guild_config = self.config.guild(ctx.guild)
        user_warnings = await guild_config.user_warnings()
        
        # Initialiser ou récupérer les avertissements de l'utilisateur
        user_id = str(member.id)
        if user_id not in user_warnings:
            user_warnings[user_id] = {"count": current_warning_level, "last_warning": None}
        
        # Mettre à jour avec le nouveau niveau
        user_warnings[user_id]["count"] = new_warning_level
        user_warnings[user_id]["last_warning"] = discord.utils.utcnow().isoformat()
        
        # Sauvegarder les données
        await guild_config.user_warnings.set(user_warnings)
        
        # Afficher le niveau détecté dans les logs
        print(f"[SANCTION SYSTEM] Niveau détecté pour {member.name}: {current_warning_level} -> {new_warning_level}")
        
        # Envoyer un MP au membre AVANT le ban (pour tous les niveaux)
        mp_sent = False
        try:
            dm_embed = discord.Embed(
                title="⚖️ Sanction Reçue - Radiant Order",
                description=f"Vous avez reçu un avertissement sur **{ctx.guild.name}**.",
                color=discord.Color.orange() if new_warning_level == 1 else discord.Color.red() if new_warning_level == 2 else discord.Color.dark_red()
            )
            dm_embed.add_field(name="📊 Avertissement", value=f"**Numéro**: {new_warning_level}/3", inline=True)
            
            # Déterminer la sanction selon le niveau
            if new_warning_level == 1:
                sanction_text = "🕐 Timeout 1 jour + Rôle Avert 1"
            elif new_warning_level == 2:
                sanction_text = "🕐 Timeout 1 semaine + Rôle Avert 2"
            else:
                sanction_text = "🔒 Ban définitif"
            
            dm_embed.add_field(name="⚖️ Sanction", value=sanction_text, inline=True)
            dm_embed.add_field(name="📝 Raison", value=raison, inline=False)
            
            if new_warning_level < 3:
                dm_embed.add_field(
                    name="⚠️ Information importante",
                    value="Votre prochain avertissement entraînera une sanction plus sévère.\n"
                          "Respectez les règles du serveur pour éviter cela.",
                    inline=False
                )
            else:
                # Message spécial pour le ban définitif
                dm_embed.add_field(
                    name="🌐 Demande de Deban",
                    value="Pour faire une demande de deban, rendez-vous sur notre site web :\n"
                          "**https://radiantorder.com/deban**\n\n"
                          "Votre demande sera examinée par l'équipe de modération.",
                    inline=False
                )
                dm_embed.add_field(
                    name="⚖️ Informations",
                    value="• Ce ban est suite à votre 3ème avertissement\n"
                          "• Les demandes de deban ne sont pas garanties\n"
                          "• Respectez les délais de traitement",
                    inline=False
                )
            
            dm_embed.set_footer(text="Radiant Order - Équipe de Modération")
            await member.send(embed=dm_embed)
            mp_sent = True
            
        except discord.Forbidden:
            print(f"[BAN SYSTEM] Impossible d'envoyer le MP à {member.name} ({member.id})")
            mp_sent = False
        
        # Appliquer la sanction selon le niveau d'avertissement
        action_taken = ""
        embed_color = discord.Color.orange()
        
        try:
            if new_warning_level == 1:
                # Avertissement 1: Timeout 1 jour + Rôle
                timeout_until = discord.utils.utcnow() + timedelta(days=1)
                await member.timeout(timeout_until, reason=f"Avertissement 1 - Timeout 1 jour - {raison}")
                await self.apply_warning_role(member, 1, raison)
                action_taken = "🕐 **Timeout 1 jour + Rôle Avert 1**"
                embed_color = discord.Color.orange()
                
            elif new_warning_level == 2:
                # Avertissement 2: Timeout 1 semaine + Rôle
                timeout_until = discord.utils.utcnow() + timedelta(days=7)
                await member.timeout(timeout_until, reason=f"Avertissement 2 - Timeout 1 semaine - {raison}")
                await self.apply_warning_role(member, 2, raison)
                action_taken = "🕐 **Timeout 1 semaine + Rôle Avert 2**"
                embed_color = discord.Color.red()
                    
            elif new_warning_level >= 3:
                # Avertissement 3: Ban définitif
                await self.apply_warning_role(member, 3, raison)  # Retirer les rôles d'avert
                await member.ban(reason=f"Avertissement 3 - Ban définitif - {raison}", delete_message_days=1)
                action_taken = "🔒 **BAN DÉFINITIF** - Contactez le site web pour une demande de deban"
                embed_color = discord.Color.dark_red()
                
                # Log détaillé pour le ban définitif
                print(f"[BAN SYSTEM] Ban définitif pour {member.name} ({member.id})")
                print(f"  - Niveau détecté: {current_warning_level} -> {new_warning_level}")
                print(f"  - Raison: {raison}")
                print(f"  - Modérateur: {ctx.author.name}")
                print(f"  - MP envoyé: {'Oui' if mp_sent else 'Non'}")
            
            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="⚖️ Sanction Appliquée",
                description=f"**Membre**: {member.mention}\n"
                           f"**Niveau détecté**: {current_warning_level} -> {new_warning_level}/3\n"
                           f"**Action**: {action_taken}\n"
                           f"**Raison**: {raison}",
                color=embed_color,
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="👤 Informations",
                value=f"**Nom**: {member.name}\n"
                      f"**ID**: {member.id}\n"
                      f"**Modérateur**: {ctx.author.mention}\n"
                      f"**MP envoyé**: {'✅ Oui' if mp_sent else '❌ Non'}",
                inline=True
            )
            
            if new_warning_level < 3:
                next_action = "Timeout 1 semaine + Rôle Avert 2" if new_warning_level == 1 else "Ban définitif"
                embed.add_field(
                    name="⚠️ Prochain avertissement",
                    value=f"**{new_warning_level + 1}**: {next_action}",
                    inline=True
                )
            
            embed.set_footer(text="Radiant Order - Système de Modération")
            
            await ctx.send(embed=embed)
            
            # Log de l'action dans le channel configuré
            await self.send_sanction_log(ctx, member, new_warning_level, action_taken, raison, mp_sent)
            
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions nécessaires pour appliquer cette sanction.")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'application de la sanction: {str(e)}")

    @sanction_group.command(name="check")
    async def check_warning_level(self, ctx, member: discord.Member):
        """🔍 Diagnostic - Vérifier le niveau d'avertissement détecté pour un membre"""
        
        # Vérifier le niveau actuel basé sur les rôles
        current_warning_level = await self.get_current_warning_level(member)
        
        guild_config = self.config.guild(ctx.guild)
        avert_role_1_id = await guild_config.avert_role_1()
        avert_role_2_id = await guild_config.avert_role_2()
        avert_role_3_id = await guild_config.avert_role_3()
        
        # Vérifier quels rôles le membre possède
        roles_status = []
        
        if avert_role_1_id:
            avert_role_1 = ctx.guild.get_role(avert_role_1_id)
            if avert_role_1:
                has_role = avert_role_1 in member.roles
                status = "✅ POSSÈDE" if has_role else "❌ N'a pas"
                roles_status.append(f"{status} {avert_role_1.mention} (ID: {avert_role_1_id})")
            else:
                roles_status.append(f"❓ Rôle Avert 1 introuvable (ID: {avert_role_1_id})")
        
        if avert_role_2_id:
            avert_role_2 = ctx.guild.get_role(avert_role_2_id)
            if avert_role_2:
                has_role = avert_role_2 in member.roles
                status = "✅ POSSÈDE" if has_role else "❌ N'a pas"
                roles_status.append(f"{status} {avert_role_2.mention} (ID: {avert_role_2_id})")
            else:
                roles_status.append(f"❓ Rôle Avert 2 introuvable (ID: {avert_role_2_id})")
        
        if avert_role_3_id:
            avert_role_3 = ctx.guild.get_role(avert_role_3_id)
            if avert_role_3:
                has_role = avert_role_3 in member.roles
                status = "✅ POSSÈDE" if has_role else "❌ N'a pas"
                roles_status.append(f"{status} {avert_role_3.mention} (ID: {avert_role_3_id})")
            else:
                roles_status.append(f"❓ Rôle Avert 3 introuvable (ID: {avert_role_3_id})")
        
        # Déterminer la prochaine sanction
        next_sanctions = {
            0: "🕐 Timeout 1 jour + Rôle Avert 1",
            1: "🕐 Timeout 1 semaine + Rôle Avert 2", 
            2: "🔒 Ban définitif",
            3: "🔒 Ban définitif (déjà Avert 3)"
        }
        
        next_sanction = next_sanctions.get(current_warning_level, "❓ Niveau inconnu")
        
        embed = discord.Embed(
            title="🔍 Diagnostic d'Avertissement",
            description=f"**Membre analysé**: {member.mention}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Niveau détecté",
            value=f"**{current_warning_level}/3**",
            inline=True
        )
        
        embed.add_field(
            name="⚖️ Prochaine sanction",
            value=next_sanction,
            inline=True
        )
        
        embed.add_field(
            name="🏷️ Statut des rôles",
            value="\n".join(roles_status) if roles_status else "Aucun rôle configuré",
            inline=False
        )
        
        # Ajouter les données stockées
        user_warnings = await guild_config.user_warnings()
        user_id = str(member.id)
        if user_id in user_warnings:
            stored_data = user_warnings[user_id]
            embed.add_field(
                name="💾 Données stockées",
                value=f"Count: {stored_data.get('count', 0)}\nDernier: {stored_data.get('last_warning', 'N/A')}",
                inline=True
            )
        
        embed.set_footer(text="Radiant Order - Diagnostic de Modération")
        await ctx.send(embed=embed)

    @sanction_group.command(name="setroles")
    async def set_avert_roles(self, ctx, avert1_role: discord.Role, avert2_role: discord.Role, avert3_role: discord.Role = None):
        """🏷️ Configurer les rôles d'avertissement (avert 1, avert 2, et optionnellement avert 3)"""
        guild_config = self.config.guild(ctx.guild)
        await guild_config.avert_role_1.set(avert1_role.id)
        await guild_config.avert_role_2.set(avert2_role.id)
        
        if avert3_role:
            await guild_config.avert_role_3.set(avert3_role.id)
        
        embed = discord.Embed(
            title="🏷️ Rôles d'Avertissement Configurés",
            description="Les rôles d'avertissement ont été configurés avec succès.",
            color=discord.Color.green()
        )
        embed.add_field(name="🕐 Rôle Avert 1", value=avert1_role.mention, inline=True)
        embed.add_field(name="🚫 Rôle Avert 2", value=avert2_role.mention, inline=True)
        
        if avert3_role:
            embed.add_field(name="🔒 Rôle Avert 3", value=avert3_role.mention, inline=True)
        
        embed.add_field(
            name="ℹ️ Information", 
            value="Le système utilisera maintenant ces rôles pour détecter automatiquement le niveau d'avertissement.\n"
                  "Utilisez `!sanction check @membre` pour tester la détection.",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @sanction_group.command(name="info")
    async def sanction_info(self, ctx, member: discord.Member):
        """📊 Afficher les informations d'avertissements d'un membre"""
        guild_config = self.config.guild(ctx.guild)
        user_warnings = await guild_config.user_warnings()
        
        # Vérifier le niveau basé sur les rôles
        current_warning_level = await self.get_current_warning_level(member)
        
        user_id = str(member.id)
        stored_data = user_warnings.get(user_id, {})
        stored_count = stored_data.get("count", 0)
        last_warning = stored_data.get("last_warning")
        
        # Utiliser le niveau détecté par les rôles comme référence
        warning_count = max(current_warning_level, stored_count)
        
        if warning_count == 0:
            embed = discord.Embed(
                title="📊 Informations d'Avertissements",
                description=f"{member.mention} n'a aucun avertissement.",
                color=discord.Color.green()
            )
        else:
            # Déterminer le statut actuel
            status = "🕐 Timeout 1 jour + Rôle Avert 1" if warning_count == 1 else "🕐 Timeout 1 semaine + Rôle Avert 2" if warning_count == 2 else "🔒 Ban définitif"
            status_color = discord.Color.orange() if warning_count == 1 else discord.Color.red() if warning_count == 2 else discord.Color.dark_red()
            
            # Informations sur les rôles actuels
            avert_role_1_id = await guild_config.avert_role_1()
            avert_role_2_id = await guild_config.avert_role_2()
            
            role_info = []
            if avert_role_1_id:
                avert_role_1 = ctx.guild.get_role(avert_role_1_id)
                if avert_role_1 and avert_role_1 in member.roles:
                    role_info.append(f"✅ {avert_role_1.mention}")
                else:
                    role_info.append(f"❌ {avert_role_1.mention if avert_role_1 else 'Rôle Avert 1 non configuré'}")
            
            if avert_role_2_id:
                avert_role_2 = ctx.guild.get_role(avert_role_2_id)
                if avert_role_2 and avert_role_2 in member.roles:
                    role_info.append(f"✅ {avert_role_2.mention}")
                else:
                    role_info.append(f"❌ {avert_role_2.mention if avert_role_2 else 'Rôle Avert 2 non configuré'}")
            
            embed = discord.Embed(
                title="📊 Informations d'Avertissements",
                description=f"**Membre**: {member.mention}\n"
                           f"**Niveau détecté**: {current_warning_level}/3\n"
                           f"**Niveau stocké**: {stored_count}/3\n"
                           f"**Statut actuel**: {status}",
                color=status_color,
                timestamp=discord.utils.utcnow()
            )
            
            if role_info:
                embed.add_field(
                    name="🏷️ Rôles d'Avertissement",
                    value="\n".join(role_info),
                    inline=True
                )
            
            if last_warning:
                try:
                    last_date = datetime.fromisoformat(last_warning)
                    embed.add_field(
                        name="📅 Dernier avertissement",
                        value=f"<t:{int(last_date.timestamp())}:F>",
                        inline=True
                    )
                except:
                    embed.add_field(
                        name="📅 Dernier avertissement",
                        value="Date invalide",
                        inline=True
                    )
            
            # Ajouter les rôles actuels
            current_roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
            if current_roles:
                embed.add_field(
                    name="🏷️ Rôles actuels",
                    value=", ".join(current_roles[:10]),  # Limiter à 10 rôles
                    inline=False
                )
        
        embed.set_footer(text="Radiant Order - Système de Modération")
        await ctx.send(embed=embed)

    @sanction_group.command(name="reset")
    async def reset_warnings(self, ctx, member: discord.Member, *, raison: str):
        """🔄 Remettre à zéro les avertissements d'un membre et retirer les sanctions actives
        
        La raison est OBLIGATOIRE.
        """
        guild_config = self.config.guild(ctx.guild)
        user_warnings = await guild_config.user_warnings()
        
        user_id = str(member.id)
        
        # Vérifier le niveau actuel basé sur les rôles
        current_warning_level = await self.get_current_warning_level(member)
        
        # Supprimer les avertissements
        if user_id in user_warnings:
            old_count = user_warnings[user_id].get("count", 0)
            del user_warnings[user_id]
            await guild_config.user_warnings.set(user_warnings)
        else:
            old_count = 0
        
        # Utiliser le niveau le plus élevé entre stocké et détecté
        effective_old_count = max(old_count, current_warning_level)
        
        # Retirer les sanctions actives selon le niveau d'avertissement
        sanctions_removed = []
        try:
            # Retirer le timeout s'il y en a un (avertissements 1 et 2)
            if effective_old_count in [1, 2]:
                try:
                    await member.timeout(None, reason=f"Reset des avertissements - {raison}")
                    sanctions_removed.append("✅ Timeout retiré")
                except:
                    sanctions_removed.append("⚠️ Timeout déjà expiré")
            
            # Retirer tous les rôles d'avertissement
            avert_role_1_id = await guild_config.avert_role_1()
            avert_role_2_id = await guild_config.avert_role_2()
            
            roles_to_remove = []
            if avert_role_1_id:
                avert_role_1 = ctx.guild.get_role(avert_role_1_id)
                if avert_role_1 and avert_role_1 in member.roles:
                    roles_to_remove.append(avert_role_1)
            
            if avert_role_2_id:
                avert_role_2 = ctx.guild.get_role(avert_role_2_id)
                if avert_role_2 and avert_role_2 in member.roles:
                    roles_to_remove.append(avert_role_2)
            
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove, reason=f"Reset des avertissements - {raison}")
                sanctions_removed.append(f"✅ {len(roles_to_remove)} rôle(s) d'avertissement retiré(s)")
            
            # Note : Pour les bans définitifs (avertissement 3), utiliser !sanction unban
            
        except discord.Forbidden:
            sanctions_removed.append("❌ Permissions insuffisantes")
        
        embed = discord.Embed(
            title="🔄 Avertissements Remis à Zéro",
            description=f"**Membre**: {member.mention}\n"
                       f"**Anciens avertissements**: {effective_old_count}\n"
                       f"**Nouveaux avertissements**: 0\n"
                       f"**Raison**: {raison}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="👤 Modérateur", value=ctx.author.mention, inline=True)
        
        if sanctions_removed:
            embed.add_field(
                name="🔧 Actions effectuées",
                value="\n".join(sanctions_removed),
                inline=True
            )
        
        if effective_old_count >= 3:
            embed.add_field(
                name="⚠️ Important",
                value="Pour un ban définitif, utilisez `!sanction unban <ID_utilisateur> <raison>`\n"
                      "Exemple: `!sanction unban 123456789 Appel accepté`",
                inline=False
            )
        
        embed.set_footer(text="Radiant Order - Système de Modération")
        
        await ctx.send(embed=embed)
        
        # MP au membre (si possible et s'il n'est pas banni)
        try:
            dm_embed = discord.Embed(
                title="🔄 Avertissements Remis à Zéro",
                description=f"Vos avertissements sur **{ctx.guild.name}** ont été remis à zéro.",
                color=discord.Color.green()
            )
            dm_embed.add_field(name="📝 Raison", value=raison, inline=False)
            dm_embed.add_field(name="✅ Nouveau départ", value="Respectez les règles pour éviter de nouveaux avertissements.", inline=False)
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass

    @sanction_group.command(name="list")
    async def list_warnings(self, ctx):
        """📋 Lister tous les membres avec des avertissements"""
        guild_config = self.config.guild(ctx.guild)
        user_warnings = await guild_config.user_warnings()
        
        if not user_warnings:
            embed = discord.Embed(
                title="📋 Liste des Avertissements",
                description="Aucun membre n'a d'avertissements actifs.",
                color=discord.Color.green()
            )
            return await ctx.send(embed=embed)
        
        # Trier par nombre d'avertissements (descendant)
        sorted_warnings = sorted(user_warnings.items(), key=lambda x: x[1].get("count", 0), reverse=True)
        
        embed = discord.Embed(
            title="📋 Liste des Avertissements",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        warning_text = ""
        for user_id, data in sorted_warnings[:20]:  # Limiter à 20 entrées
            member = ctx.guild.get_member(int(user_id))
            count = data.get("count", 0)
            
            if member:
                status_emoji = "🔒" if count >= 3 else "🚫" if count == 2 else "🕐"
                warning_text += f"{status_emoji} **{member.name}** - {count} avertissement(s)\n"
            else:
                warning_text += f"❓ **Utilisateur inconnu** ({user_id}) - {count} avertissement(s)\n"
        
        if warning_text:
            embed.description = warning_text
        else:
            embed.description = "Aucun membre avec avertissements trouvé."
        
        embed.set_footer(text="Radiant Order - Système de Modération")
        await ctx.send(embed=embed)

    @sanction_group.command(name="unban")
    async def unban_user(self, ctx, user_id: int, *, args: str):
        """🔓 Débannir un utilisateur par son ID
        
        Paramètres:
        - user_id: ID de l'utilisateur à débannir
        - raison: Raison du deban (OBLIGATOIRE)
        - --keep-warnings: Optionnel, conserve les avertissements
        
        Exemples:
        !sanction unban 123456789 Appel accepté
        !sanction unban 123456789 Deban temporaire --keep-warnings
        """
        
        # Parser les arguments
        keep_warnings = "--keep-warnings" in args
        raison = args.replace("--keep-warnings", "").strip()
        
        if not raison:
            return await ctx.send("❌ La raison est obligatoire.\n"
                                 "Exemple: `!sanction unban 123456789 Appel accepté`\n"
                                 "Ajouter `--keep-warnings` pour conserver les avertissements.")
        
        reset_warnings = not keep_warnings  # Inverse de keep_warnings
        
        try:
            # Vérifier si l'utilisateur est banni
            try:
                ban_entry = await ctx.guild.fetch_ban(discord.Object(id=user_id))
                banned_user = ban_entry.user
            except discord.NotFound:
                return await ctx.send(f"❌ L'utilisateur avec l'ID `{user_id}` n'est pas banni sur ce serveur.")
            
            # Débannir l'utilisateur
            await ctx.guild.unban(discord.Object(id=user_id), reason=f"Deban manuel - {raison}")
            
            # Gestion des avertissements
            guild_config = self.config.guild(ctx.guild)
            user_warnings = await guild_config.user_warnings()
            user_str_id = str(user_id)
            
            old_warnings = 0
            if user_str_id in user_warnings:
                old_warnings = user_warnings[user_str_id].get("count", 0)
                
                if reset_warnings:
                    # Supprimer les avertissements
                    del user_warnings[user_str_id]
                    await guild_config.user_warnings.set(user_warnings)
                    warnings_status = "✅ Avertissements supprimés"
                else:
                    warnings_status = f"⚠️ Avertissements conservés ({old_warnings}/3)"
            else:
                warnings_status = "ℹ️ Aucun avertissement trouvé"
            
            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="🔓 Utilisateur Débanni",
                description=f"**Utilisateur**: {banned_user.name} ({banned_user.mention})\n"
                           f"**ID**: {user_id}\n"
                           f"**Raison**: {raison}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="👤 Informations",
                value=f"**Nom complet**: {banned_user}\n"
                      f"**Modérateur**: {ctx.author.mention}\n"
                      f"**Anciens avertissements**: {old_warnings}/3",
                inline=True
            )
            
            embed.add_field(
                name="📊 Statut des Avertissements",
                value=warnings_status,
                inline=True
            )
            
            embed.set_thumbnail(url=banned_user.display_avatar.url)
            embed.set_footer(text="Radiant Order - Système de Modération")
            
            await ctx.send(embed=embed)
            
            # Log de l'action
            print(f"[BAN SYSTEM] Deban manuel effectué:")
            print(f"  - Utilisateur: {banned_user.name} ({user_id})")
            print(f"  - Modérateur: {ctx.author.name}")
            print(f"  - Avertissements reset: {'Oui' if reset_warnings else 'Non'}")
            print(f"  - Raison: {raison}")
            
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions pour débannir cet utilisateur.")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors du deban: {str(e)}")
            print(f"[BAN SYSTEM] Erreur deban {user_id}: {str(e)}")

    @sanction_group.command(name="untimeout")
    async def remove_timeout(self, ctx, member: discord.Member, *, raison: str):
        """🕐 Retirer le timeout d'un membre (sans affecter les avertissements)
        
        La raison est OBLIGATOIRE.
        """
        
        # Vérifier si le membre a un timeout actif
        if member.timed_out_until is None:
            return await ctx.send(f"❌ {member.mention} n'a pas de timeout actif.")
        
        try:
            # Retirer le timeout
            await member.timeout(None, reason=raison)
            
            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="🕐 Timeout Retiré",
                description=f"**Membre**: {member.mention}\n"
                           f"**Raison**: {raison}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            
            embed.add_field(
                name="👤 Informations",
                value=f"**Nom**: {member.name}\n"
                      f"**ID**: {member.id}\n"
                      f"**Modérateur**: {ctx.author.mention}",
                inline=True
            )
            
            embed.add_field(
                name="ℹ️ Note",
                value="Les avertissements du membre n'ont pas été modifiés.\n"
                      "Utilisez `!sanction reset` pour les supprimer.",
                inline=True
            )
            
            embed.set_footer(text="Radiant Order - Système de Modération")
            await ctx.send(embed=embed)
            
            # MP au membre
            try:
                dm_embed = discord.Embed(
                    title="🕐 Timeout Retiré - Radiant Order",
                    description=f"Votre timeout sur **{ctx.guild.name}** a été retiré.",
                    color=discord.Color.green()
                )
                dm_embed.add_field(name="📝 Raison", value=raison, inline=False)
                dm_embed.add_field(name="⚠️ Rappel", value="Respectez les règles du serveur.", inline=False)
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass
                
            # Log de l'action
            print(f"[SANCTION SYSTEM] Timeout retiré:")
            print(f"  - Membre: {member.name} ({member.id})")
            print(f"  - Modérateur: {ctx.author.name}")
            print(f"  - Raison: {raison}")
            
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas les permissions pour retirer le timeout de ce membre.")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors du retrait du timeout: {str(e)}")

    async def show_sanction_help(self, ctx):
        """Affiche l'aide du système de sanction"""
        embed = discord.Embed(
            title="⚖️ Système de Sanction - Aide",
            description="Système de modération avec avertissements progressifs pour Radiant Order",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📋 Commandes Disponibles",
            value="`!sanction user <@membre> <raison>` - Appliquer une sanction\n"
                  "`!sanction check <@membre>` - 🔍 Diagnostic du niveau d'avertissement\n"
                  "`!sanction info <@membre>` - Voir les avertissements\n"
                  "`!sanction reset <@membre> <raison>` - Reset complet (avertissements + sanctions)\n"
                  "`!sanction untimeout <@membre> <raison>` - Retirer uniquement le timeout\n"
                  "`!sanction setroles <@role_avert1> <@role_avert2> [@role_avert3]` - Configurer les rôles\n"
                  "`!sanction list` - Lister tous les avertissements\n"
                  "`!sanction unban <ID_utilisateur> <raison>` - Débannir par ID (ajouter --keep-warnings pour conserver)",
            inline=False
        )
        
        embed.add_field(
            name="⚖️ Système d'Avertissements",
            value="**1er avertissement**: 🕐 Timeout 1 jour + Rôle Avert 1\n"
                  "**2ème avertissement**: 🕐 Timeout 1 semaine + Rôle Avert 2\n"
                  "**3ème avertissement**: 🔒 Ban définitif",
            inline=False
        )
        
        embed.add_field(
            name="🏷️ Détection Automatique",
            value="• Le système détecte automatiquement le niveau d'avertissement via les rôles\n"
                  "• Si un membre a le rôle \"Avert 1\", la prochaine sanction sera \"Avert 2\"\n"
                  "• Si un membre a le rôle \"Avert 2\", la prochaine sanction sera \"Ban définitif\"",
            inline=False
        )
        
        embed.add_field(
            name="🔒 Ban Définitif",
            value="• Contactez le site web pour une demande de deban\n"
                  "• Respectez les délais de traitement\n"
                  "• Les timeouts 1 et 2 se terminent automatiquement",
            inline=False
        )
        
        # Afficher les rôles autorisés
        guild_config = self.config.guild(ctx.guild)
        authorized_roles_ids = await guild_config.authorized_roles()
        authorized_roles = []
        
        for role_id in authorized_roles_ids:
            role = ctx.guild.get_role(role_id)
            if role:
                authorized_roles.append(role.mention)
            else:
                authorized_roles.append(f"Rôle ID: {role_id}")
        
        embed.add_field(
            name="🔐 Rôles Autorisés",
            value="\n".join(authorized_roles) if authorized_roles else "Aucun rôle configuré",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Important",
            value="**La raison est OBLIGATOIRE** pour toutes les commandes de sanction.\n"
                  "Les logs sont automatiquement envoyés dans le channel de modération.\n"
                  "**Configurez d'abord les rôles** avec `!sanction setroles`",
            inline=False
        )
        
        embed.set_footer(text="Radiant Order - Système de Modération")
        await ctx.send(embed=embed)

    @sanction_group.error
    async def sanction_error(self, ctx, error):
        """Gestion des erreurs pour les commandes de sanction"""
        if isinstance(error, commands.CheckFailure):
            # Afficher les rôles autorisés dans le message d'erreur
            guild_config = self.config.guild(ctx.guild)
            authorized_roles_ids = await guild_config.authorized_roles()
            authorized_roles = []
            
            for role_id in authorized_roles_ids:
                role = ctx.guild.get_role(role_id)
                if role:
                    authorized_roles.append(role.mention)
                else:
                    authorized_roles.append(f"Rôle ID: {role_id}")
            
            roles_text = "\n".join(authorized_roles) if authorized_roles else "Aucun rôle configuré"
            
            embed = discord.Embed(
                title="❌ Accès Refusé",
                description="Vous n'avez pas les permissions nécessaires pour utiliser cette commande.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="🔐 Rôles Autorisés",
                value=roles_text,
                inline=False
            )
            embed.set_footer(text="Radiant Order - Système de Modération")
            
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Membre introuvable.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Argument manquant. Utilisez `!sanction` pour voir l'aide.")

async def setup(bot):
    await bot.add_cog(BanSystem(bot))

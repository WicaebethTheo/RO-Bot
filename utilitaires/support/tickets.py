import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import datetime
import asyncio
import io
import html

class SupportView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Créer un ticket Support", style=discord.ButtonStyle.primary, emoji="<a:CanYouHelp_By_Frogverbal:1380889107323949106>", custom_id="support_ticket")
    async def support_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.create_ticket(interaction, "support")

class RecruitmentView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Créer un ticket Recrutement", style=discord.ButtonStyle.success, emoji="<a:CanYouHelp_By_Frogverbal:1380889107323949106>", custom_id="recruitment_ticket")
    async def recruitment_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.create_ticket(interaction, "recrutement")

class TicketControlView(discord.ui.View):
    def __init__(self, cog, ticket_type, creator_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.ticket_type = ticket_type
        self.creator_id = creator_id

    @discord.ui.button(label="Fermer le ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.close_ticket(interaction, self.ticket_type, self.creator_id)

    @discord.ui.button(label="Sauvegarder les logs", style=discord.ButtonStyle.secondary, emoji="<:helper:1380889105164013710>", custom_id="save_logs")
    async def save_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.save_ticket_logs(interaction, manual=True)

class TicketSystem(commands.Cog):
    """🎫 Système de tickets pour support et recrutement"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=555666777)
        
        default_guild = {
            "channels": {
                "support": 1380560533102530560,
                "recrutement": 1380560536546316348,
                "logs": 1380560672294961302
            },
            "category_id": 1380567327103516692,
            "ticket_counter": 0,
            "active_tickets": {}
        }
        
        self.config.register_guild(**default_guild)
        
        # Vues persistantes
        self.support_view = SupportView(self)
        self.recruitment_view = RecruitmentView(self)

    async def cog_load(self):
        """Ajouter les vues persistantes au bot"""
        self.bot.add_view(self.support_view)
        self.bot.add_view(self.recruitment_view)

    async def create_ticket(self, interaction, ticket_type):
        """Créer un nouveau ticket"""
        guild = interaction.guild
        user = interaction.user
        
        # Vérifier si l'utilisateur a déjà un ticket ouvert
        active_tickets = await self.config.guild(guild).active_tickets()
        user_tickets = [ticket for ticket in active_tickets.values() if ticket.get("creator_id") == user.id]
        
        if user_tickets:
            error_embed = discord.Embed(
                title="⚠️ Ticket déjà ouvert",
                description="Vous avez déjà un ticket ouvert. Veuillez le fermer avant d'en créer un nouveau.",
                color=discord.Color.orange()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        # Incrémenter le compteur de tickets
        counter = await self.config.guild(guild).ticket_counter()
        counter += 1
        await self.config.guild(guild).ticket_counter.set(counter)
        
        # Récupérer la catégorie
        category_id = await self.config.guild(guild).category_id()
        category = guild.get_channel(category_id)
        
        if not category:
            error_embed = discord.Embed(
                title="❌ Erreur de configuration",
                description="Catégorie de tickets introuvable. Contactez un administrateur.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        # Créer le nom du ticket
        ticket_name = f"{'🎧-support' if ticket_type == 'support' else '💼-recrutement'}-{counter:04d}"
        
        try:
            # Permissions du ticket
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            
            # Ajouter les permissions pour les administrateurs
            for role in guild.roles:
                if role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            
            # Créer le channel
            ticket_channel = await guild.create_text_channel(
                name=ticket_name,
                category=category,
                overwrites=overwrites,
                topic=f"Ticket {ticket_type} de {user.display_name} (ID: {user.id})"
            )
            
            # Embed de bienvenue dans le ticket
            welcome_embed = discord.Embed(
                title=f"🎫 Ticket {ticket_type.title()} #{counter:04d}",
                description=f"Bonjour {user.mention} !\n\n"
                           f"{'🎧 Support demandé' if ticket_type == 'support' else '💼 Candidature de recrutement'}\n\n"
                           f"Un membre du staff va vous répondre rapidement.\n"
                           f"Décrivez votre {'problème' if ticket_type == 'support' else 'candidature'} de manière détaillée.",
                color=discord.Color.blue() if ticket_type == 'support' else discord.Color.green()
            )
            welcome_embed.add_field(name="👤 Créateur", value=user.mention, inline=True)
            welcome_embed.add_field(name="📅 Créé le", value=f"<t:{int(datetime.datetime.now().timestamp())}:F>", inline=True)
            welcome_embed.add_field(name="🆔 ID Utilisateur", value=f"`{user.id}`", inline=True)
            welcome_embed.set_thumbnail(url=user.display_avatar.url)
            welcome_embed.set_footer(text="Utilisez les boutons ci-dessous pour gérer ce ticket")
            
            # Vue de contrôle du ticket
            control_view = TicketControlView(self, ticket_type, user.id)
            
            await ticket_channel.send(embed=welcome_embed, view=control_view)
            
            # Sauvegarder les informations du ticket
            ticket_data = {
                "channel_id": ticket_channel.id,
                "creator_id": user.id,
                "type": ticket_type,
                "created_at": datetime.datetime.now().isoformat(),
                "counter": counter
            }
            
            active_tickets[str(ticket_channel.id)] = ticket_data
            await self.config.guild(guild).active_tickets.set(active_tickets)
            
            # Réponse de confirmation
            success_embed = discord.Embed(
                title="✅ Ticket créé !",
                description=f"Votre ticket {ticket_type} a été créé : {ticket_channel.mention}",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="❌ Permissions insuffisantes",
                description="Je n'ai pas les permissions pour créer des channels.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="💥 Erreur",
                description=f"Une erreur s'est produite :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    async def close_ticket(self, interaction, ticket_type, creator_id):
        """Fermer un ticket avec confirmation"""
        # Vérifier les permissions
        if not (interaction.user.guild_permissions.administrator or interaction.user.id == creator_id):
            error_embed = discord.Embed(
                title="❌ Permissions insuffisantes",
                description="Seuls les administrateurs et le créateur du ticket peuvent le fermer.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
        # Demander confirmation
        confirm_embed = discord.Embed(
            title="⚠️ Confirmation de fermeture",
            description="Êtes-vous sûr de vouloir fermer ce ticket ?\n\n"
                       "⚡ Les logs seront automatiquement sauvegardés\n"
                       "🗑️ Le channel sera supprimé dans 10 secondes",
            color=discord.Color.orange()
        )
        
        await interaction.response.send_message(embed=confirm_embed)
        
        # Sauvegarder les logs avant de fermer
        await self.save_ticket_logs(interaction, manual=False)
        
        # Attendre 10 secondes puis supprimer
        await asyncio.sleep(10)
        
        try:
            # Supprimer de la config
            active_tickets = await self.config.guild(interaction.guild).active_tickets()
            if str(interaction.channel.id) in active_tickets:
                del active_tickets[str(interaction.channel.id)]
                await self.config.guild(interaction.guild).active_tickets.set(active_tickets)
            
            # Supprimer le channel
            await interaction.channel.delete(reason="Ticket fermé")
            
        except Exception as e:
            print(f"Erreur lors de la fermeture du ticket: {e}")

    async def save_ticket_logs(self, interaction, manual=False):
        """Sauvegarder les logs du ticket en HTML"""
        try:
            # Récupérer tous les messages du channel
            messages = []
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                messages.append(message)
            
            # Récupérer les infos du ticket
            active_tickets = await self.config.guild(interaction.guild).active_tickets()
            ticket_info = active_tickets.get(str(interaction.channel.id), {})
            
            # Générer le HTML
            html_content = self.generate_html_log(messages, ticket_info, interaction.channel)
            
            # Créer le fichier
            filename = f"ticket-{ticket_info.get('type', 'unknown')}-{ticket_info.get('counter', '0000'):04d}.html"
            file_buffer = io.BytesIO(html_content.encode('utf-8'))
            file = discord.File(file_buffer, filename=filename)
            
            # Envoyer dans le channel de logs
            logs_channel_id = await self.config.guild(interaction.guild).channels()
            logs_channel = interaction.guild.get_channel(logs_channel_id.get("logs"))
            
            if logs_channel:
                # Embed pour accompagner le log
                log_embed = discord.Embed(
                    title="📋 Logs de ticket sauvegardés",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.now()
                )
                log_embed.add_field(name="🎫 Ticket", value=interaction.channel.name, inline=True)
                log_embed.add_field(name="📝 Type", value=ticket_info.get('type', 'Inconnu'), inline=True)
                log_embed.add_field(name="👤 Créateur", value=f"<@{ticket_info.get('creator_id')}>", inline=True)
                log_embed.add_field(name="📅 Créé le", value=ticket_info.get('created_at', 'Inconnu'), inline=True)
                log_embed.add_field(name="💬 Messages", value=f"{len(messages)} messages", inline=True)
                log_embed.add_field(name="🔄 Sauvegarde", value="Manuelle" if manual else "Automatique", inline=True)
                
                await logs_channel.send(embed=log_embed, file=file)
                
                if manual:
                    success_embed = discord.Embed(
                        title="✅ Logs sauvegardés",
                        description=f"Les logs ont été sauvegardés dans {logs_channel.mention}",
                        color=discord.Color.green()
                    )
                    await interaction.followup.send(embed=success_embed, ephemeral=True)
            
        except Exception as e:
            if manual:
                error_embed = discord.Embed(
                    title="❌ Erreur de sauvegarde",
                    description=f"Impossible de sauvegarder les logs :\n```{str(e)}```",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=error_embed, ephemeral=True)

    def generate_html_log(self, messages, ticket_info, channel):
        """Générer le contenu HTML des logs"""
        creator_id = ticket_info.get('creator_id', 'Inconnu')
        ticket_type = ticket_info.get('type', 'inconnu')
        created_at = ticket_info.get('created_at', 'Inconnu')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket {ticket_type.title()} - {channel.name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #2c2f33;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #7289da, #5865f2);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .ticket-info {{
            background-color: #36393f;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #7289da;
        }}
        .message {{
            background-color: #40444b;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 3px solid #7289da;
        }}
        .message.bot {{
            border-left-color: #faa61a;
        }}
        .message-header {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        .avatar {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        .username {{
            font-weight: bold;
            color: #7289da;
        }}
        .timestamp {{
            color: #b9bbbe;
            font-size: 0.85em;
            margin-left: auto;
        }}
        .message-content {{
            line-height: 1.4;
            word-wrap: break-word;
        }}
        .attachment {{
            background-color: #2f3136;
            padding: 10px;
            border-radius: 5px;
            margin-top: 8px;
            border: 1px solid #4f545c;
        }}
        .embed {{
            background-color: #2f3136;
            border-left: 4px solid #7289da;
            padding: 10px;
            margin-top: 8px;
            border-radius: 0 5px 5px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background-color: #36393f;
            border-radius: 8px;
            color: #b9bbbe;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎫 Logs du Ticket - {html.escape(channel.name)}</h1>
        <p>Système de tickets Radiant Order</p>
    </div>
    
    <div class="ticket-info">
        <h3>📋 Informations du ticket</h3>
        <p><strong>Type :</strong> {ticket_type.title()}</p>
        <p><strong>Créateur :</strong> <@{creator_id}> (ID: {creator_id})</p>
        <p><strong>Créé le :</strong> {created_at}</p>
        <p><strong>Channel :</strong> #{channel.name}</p>
        <p><strong>Messages :</strong> {len(messages)} messages</p>
        <p><strong>Sauvegardé le :</strong> {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
    </div>
    
    <div class="messages">
"""
        
        for message in messages:
            # Échapper le contenu HTML
            content = html.escape(message.content) if message.content else "<em>Pas de contenu</em>"
            username = html.escape(message.author.display_name)
            timestamp = message.created_at.strftime('%d/%m/%Y à %H:%M:%S')
            avatar_url = str(message.author.display_avatar.url)
            
            bot_class = " bot" if message.author.bot else ""
            
            html_content += f"""
        <div class="message{bot_class}">
            <div class="message-header">
                <img src="{avatar_url}" alt="Avatar" class="avatar">
                <span class="username">{username}</span>
                <span class="timestamp">{timestamp}</span>
            </div>
            <div class="message-content">{content}</div>
"""
            
            # Ajouter les pièces jointes
            if message.attachments:
                for attachment in message.attachments:
                    html_content += f"""
            <div class="attachment">
                📎 <a href="{attachment.url}" target="_blank">{html.escape(attachment.filename)}</a>
                ({attachment.size} bytes)
            </div>
"""
            
            # Ajouter les embeds (simplifiés)
            if message.embeds:
                for embed in message.embeds:
                    if embed.title or embed.description:
                        html_content += f"""
            <div class="embed">
                {f'<strong>{html.escape(embed.title)}</strong><br>' if embed.title else ''}
                {html.escape(embed.description) if embed.description else ''}
            </div>
"""
            
            html_content += "        </div>\n"
        
        html_content += f"""
    </div>
    
    <div class="footer">
        <p>📊 Logs générés automatiquement par le système de tickets Radiant Order</p>
        <p>🕒 Généré le {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
        
        return html_content

    @commands.group(name="tickets")
    @checks.admin_or_permissions(manage_guild=True)
    async def tickets(self, ctx):
        """🎫 Gestion du système de tickets"""
        pass

    @tickets.command(name="setup")
    async def setup_tickets(self, ctx):
        """🚀 Configure les messages de tickets dans les channels"""
        channels = await self.config.guild(ctx.guild).channels()
        
        # Message de début
        setup_embed = discord.Embed(
            title="<a:maruloader:1380888045259329569> Configuration des tickets en cours...",
            description="Nettoyage et configuration des channels...",
            color=discord.Color.orange()
        )
        setup_message = await ctx.send(embed=setup_embed)
        
        try:
            # Nettoyer le channel support
            support_channel = ctx.guild.get_channel(channels["support"])
            if support_channel:
                setup_embed.description = f"<a:maruloader:1380888045259329569> Nettoyage du salon {support_channel.mention}..."
                await setup_message.edit(embed=setup_embed)
                
                # Supprimer tous les messages (par batch de 100 maximum)
                try:
                    await support_channel.purge(limit=None, check=lambda m: True)
                except discord.Forbidden:
                    # Si on ne peut pas purge, supprimer un par un
                    async for message in support_channel.history(limit=None):
                        try:
                            await message.delete()
                        except:
                            continue
                
                # Envoyer le nouveau message de support
                setup_embed.description = f"<a:maruloader:1380888045259329569> Configuration du salon {support_channel.mention}..."
                await setup_message.edit(embed=setup_embed)
                
                support_embed = discord.Embed(
                    title="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Support Technique",
                    description="**Besoin d'aide ?**\n\n"
                               "Cliquez sur le bouton ci-dessous pour créer un ticket de support.\n"
                               "Un membre du staff vous aidera rapidement !\n\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Décrivez votre problème clairement\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Soyez patient, nous répondons rapidement\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Un seul ticket par personne à la fois",
                    color=discord.Color.blue()
                )
                support_embed.set_footer(text="Radiant Order - Support")
                    
                await support_channel.send(embed=support_embed, view=self.support_view)
            
            # Nettoyer le channel recrutement
            recruitment_channel = ctx.guild.get_channel(channels["recrutement"])
            if recruitment_channel:
                setup_embed.description = f"<a:maruloader:1380888045259329569> Nettoyage du salon {recruitment_channel.mention}..."
                await setup_message.edit(embed=setup_embed)
                
                # Supprimer tous les messages (par batch de 100 maximum)
                try:
                    await recruitment_channel.purge(limit=None, check=lambda m: True)
                except discord.Forbidden:
                    # Si on ne peut pas purge, supprimer un par un
                    async for message in recruitment_channel.history(limit=None):
                        try:
                            await message.delete()
                        except:
                            continue
                
                # Envoyer le nouveau message de recrutement
                setup_embed.description = f"<a:maruloader:1380888045259329569> Configuration du salon {recruitment_channel.mention}..."
                await setup_message.edit(embed=setup_embed)
                
                recruitment_embed = discord.Embed(
                    title="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Recrutement",
                    description="**Intéressé pour rejoindre l'équipe ?**\n\n"
                               "Cliquez sur le bouton ci-dessous pour postuler !\n"
                               "Nos recruteurs examineront votre candidature.\n\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Présentez-vous et vos motivations\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Indiquez vos compétences et expériences\n"
                               "<a:Animated_Arrow_Blue:1380888378953961472> Une candidature par personne",
                    color=discord.Color.green()
                )
                recruitment_embed.set_footer(text="Radiant Order - Recrutement")
                
                await recruitment_channel.send(embed=recruitment_embed, view=self.recruitment_view)
            
            # Message de succès final
            success_embed = discord.Embed(
                title="✅ Système de tickets configuré",
                description="Les channels ont été nettoyés et les messages avec boutons ont été configurés avec succès !",
                color=discord.Color.green()
            )
            success_embed.add_field(
                name="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Support", 
                value=f"{support_channel.mention if support_channel else 'Non configuré'}", 
                inline=True
            )
            success_embed.add_field(
                name="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Recrutement", 
                value=f"{recruitment_channel.mention if recruitment_channel else 'Non configuré'}", 
                inline=True
            )
            success_embed.set_footer(text="Configuration terminée - Radiant Order")
            
            await setup_message.edit(embed=success_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erreur lors de la configuration",
                description=f"Une erreur s'est produite :\n```{str(e)}```",
                color=discord.Color.red()
            )
            await setup_message.edit(embed=error_embed)

    @tickets.command(name="stats")
    async def tickets_stats(self, ctx):
        """📊 Statistiques des tickets"""
        active_tickets = await self.config.guild(ctx.guild).active_tickets()
        total_created = await self.config.guild(ctx.guild).ticket_counter()
        
        # Compter par type
        support_tickets = len([t for t in active_tickets.values() if t.get("type") == "support"])
        recruitment_tickets = len([t for t in active_tickets.values() if t.get("type") == "recrutement"])
        
        embed = discord.Embed(
            title="📊 Statistiques des tickets",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="🎫 Total créés", value=f"{total_created}", inline=True)
        embed.add_field(name="📖 Actuellement ouverts", value=f"{len(active_tickets)}", inline=True)
        embed.add_field(name="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Support ouverts", value=f"{support_tickets}", inline=True)
        embed.add_field(name="<a:CanYouHelp_By_Frogverbal:1380889107323949106> Recrutement ouverts", value=f"{recruitment_tickets}", inline=True)
        embed.add_field(name="✅ Fermés", value=f"{total_created - len(active_tickets)}", inline=True)
        
        await ctx.send(embed=embed)

    @tickets.command(name="close")
    async def force_close_ticket(self, ctx, channel: discord.TextChannel = None):
        """🔒 Forcer la fermeture d'un ticket (Admin)"""
        target_channel = channel or ctx.channel
        
        active_tickets = await self.config.guild(ctx.guild).active_tickets()
        ticket_info = active_tickets.get(str(target_channel.id))
        
        if not ticket_info:
            return await ctx.send("❌ Ce n'est pas un ticket actif.")
        
        # Simuler une interaction pour la fermeture
        class FakeInteraction:
            def __init__(self, channel, user, guild):
                self.channel = channel
                self.user = user
                self.guild = guild
        
        fake_interaction = FakeInteraction(target_channel, ctx.author, ctx.guild)
        await self.close_ticket(fake_interaction, ticket_info["type"], ticket_info["creator_id"])

async def setup(bot):
    await bot.add_cog(TicketSystem(bot)) 
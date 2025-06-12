import discord
from redbot.core import commands
import asyncio

class NayanaButton(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, label: str, custom_id: str):
        super().__init__(style=style, label=label, custom_id=custom_id)
        
    async def callback(self, interaction: discord.Interaction):
        if self.custom_id == "nayana_oui":
            response_embed = discord.Embed(
                title="😏 Parfait !",
                description="J'arrive ce soir à 22h, mets-toi en p'tite tenue 😘",
                color=0xFF69B4
            )
        elif self.custom_id == "nayana_non":
            response_embed = discord.Embed(
                title="😢 Dommage",
                description="Dommage ;'(",
                color=0x808080
            )
        
        # Désactiver les boutons après utilisation
        for item in self.view.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=response_embed, view=self.view)

class NayanaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.add_item(NayanaButton(discord.ButtonStyle.green, "Oui", "nayana_oui"))
        self.add_item(NayanaButton(discord.ButtonStyle.red, "Non", "nayana_non"))
    
    async def on_timeout(self):
        # Désactiver tous les boutons quand le timeout est atteint
        for item in self.children:
            item.disabled = True

class Nayana(commands.Cog):
    """Cog pour envoyer des messages spéciaux à Nayana"""

    def __init__(self, bot):
        self.bot = bot
        self.target_user_id = 994323170800697374

    @commands.command(name="nayana")
    async def nayana_command(self, ctx):
        """Envoie un message spécial à Nayana"""
        
        # Récupérer l'utilisateur cible
        target_user = self.bot.get_user(self.target_user_id)
        
        if not target_user:
            try:
                target_user = await self.bot.fetch_user(self.target_user_id)
            except discord.NotFound:
                error_embed = discord.Embed(
                    title="❌ Erreur",
                    description="Utilisateur introuvable.",
                    color=0xFF0000
                )
                return await ctx.send(embed=error_embed)
        
        # Créer l'embed du message
        message_embed = discord.Embed(
            title="💕 Message spécial",
            description="Bonjour, tu veux que je me mette dans ton lit ce soir ? 😏",
            color=0xFF1493
        )        
        # Créer la vue avec les boutons
        view = NayanaView()
        
        try:
            # Envoyer le message en privé
            await target_user.send(embed=message_embed, view=view)
            
            # Confirmation dans le canal
            success_embed = discord.Embed(
                title="✅ Message envoyé !",
                description=f"Le message a été envoyé en privé à {target_user.display_name}.",
                color=0x00FF00
            )
            await ctx.send(embed=success_embed)
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="❌ Erreur",
                description="Impossible d'envoyer un message privé à cet utilisateur. Ses DMs sont peut-être fermés.",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erreur",
                description=f"Une erreur s'est produite : {str(e)}",
                color=0xFF0000
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Nayana(bot))

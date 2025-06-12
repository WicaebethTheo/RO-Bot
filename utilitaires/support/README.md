# 🎫 TicketSystem - Système de Tickets Support & Recrutement

## 📋 Description
Système complet de tickets interactifs pour support technique et recrutement avec boutons Discord, gestion des permissions, sauvegarde automatique des logs en HTML et interface moderne.

## ✨ Fonctionnalités

### 🎯 **Tickets Interactifs**
- Création via boutons Discord intuitifs
- Deux types : Support technique et Recrutement
- Channels privés avec permissions automatiques
- Système de numérotation séquentielle

### 🔐 **Gestion des Permissions**
- Accès restreint : Créateur + Administrateurs uniquement
- Permissions automatiques configurées à la création
- Protection complète de la confidentialité
- Un seul ticket par utilisateur à la fois

### 💾 **Sauvegarde Automatique**
- Génération de logs HTML stylés automatique
- Sauvegarde à la fermeture ou manuelle
- Design Discord-like avec avatars et timestamps
- Archivage dans channel dédié

### 🎨 **Interface Moderne**
- Boutons persistants avec emojis
- Embeds stylés et informatifs
- Couleurs thématiques (bleu=support, vert=recrutement)
- Messages de confirmation intuitifs

## 🚀 Installation & Configuration

```bash
# Charger le cog
!load utilitaires.support

# Configurer les messages avec boutons
!tickets setup

# Voir les statistiques
!tickets stats
```

## 🎯 Configuration par Défaut

### **Channels & Catégorie**
```
🎧 Support:      1380560533102530560
💼 Recrutement:  1380560536546316348
📁 Catégorie:    1380567327103516692
📋 Logs:         1380560672294961302
```

### **Boutons Interactifs**
- **Bouton Bleu** : "🎧 Créer un ticket Support"
- **Bouton Vert** : "💼 Créer un ticket Recrutement"

## 🎮 Commandes

### **Commandes Admin** (Permissions requises)
- `!tickets setup` - Configurer les messages avec boutons
- `!tickets stats` - Voir les statistiques des tickets
- `!tickets close [channel]` - Forcer la fermeture d'un ticket

### **Boutons dans les Tickets**
- `🔒 Fermer le ticket` - Fermeture avec sauvegarde auto
- `📋 Sauvegarder les logs` - Sauvegarde manuelle

### **Exemples d'utilisation**
```bash
# Configuration initiale
!tickets setup

# Voir l'activité
!tickets stats

# Fermer un ticket spécifique
!tickets close #🎧-support-0001
```

## 🔧 Fonctionnement Technique

### **Processus de Création**
1. **Clic utilisateur** → Bouton support/recrutement
2. **Vérification** → Contrôle ticket existant
3. **Création** → Channel privé dans catégorie
4. **Permissions** → Admin + créateur uniquement
5. **Message** → Embed de bienvenue avec boutons

### **Architecture des Vues**
```python
class SupportView(discord.ui.View):
    # Vue persistante pour le channel support
    
class TicketControlView(discord.ui.View):
    # Boutons de gestion dans chaque ticket
```

### **Nomenclature des Tickets**
- Support : `🎧-support-0001, 🎧-support-0002...`
- Recrutement : `💼-recrutement-0001, 💼-recrutement-0002...`

## 🎨 Interface Utilisateur

### **Message d'Accueil Support**
```
🎧 Support Technique

Besoin d'aide ?

Cliquez sur le bouton ci-dessous pour créer un ticket de support.
Un membre du staff vous aidera rapidement !

🔹 Décrivez votre problème clairement
🔹 Soyez patient, nous répondons rapidement
🔹 Un seul ticket par personne à la fois

[🎧 Créer un ticket Support]

Spike Rush - Support
```

### **Ticket Créé**
```
🎫 Ticket Support #0001

Bonjour @utilisateur !

🎧 Support demandé

Un membre du staff va vous répondre rapidement.
Décrivez votre problème de manière détaillée.

👤 Créateur: @utilisateur
📅 Créé le: 25/12/2024 à 15:30:45
🆔 ID Utilisateur: 123456789

[🔒 Fermer le ticket] [📋 Sauvegarder les logs]

Utilisez les boutons ci-dessous pour gérer ce ticket
```

## 📊 Sauvegarde HTML

### **Fonctionnalités des Logs**
- **Design Discord-like** avec CSS moderne
- **Avatars** et usernames stylés
- **Timestamps** précis pour chaque message
- **Embeds** et pièces jointes préservés
- **Métadonnées** complètes du ticket

### **Exemple de Log Généré**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Ticket Support - 🎧-support-0001</title>
    <style>/* CSS Discord-like */</style>
</head>
<body>
    <div class="header">
        <h1>🎫 Logs du Ticket - 🎧-support-0001</h1>
    </div>
    
    <div class="ticket-info">
        📋 Informations du ticket
        Type: Support
        Créateur: @utilisateur (ID: 123456789)
        Créé le: 2024-12-25...
        Messages: 15 messages
    </div>
    
    <div class="messages">
        <!-- Messages avec avatars et styling -->
    </div>
</body>
</html>
```

## 🔒 Permissions Requises

### **Bot**
- `Manage Channels` - Créer les tickets
- `Manage Permissions` - Configurer les droits
- `Send Messages` - Envoyer des messages
- `Embed Links` - Créer des embeds
- `Attach Files` - Joindre les logs HTML

### **Admin**
- `Administrator` - Gestion complète
- `Manage Guild` - Configuration du serveur

### **Utilisateurs**
- Aucune permission spéciale requise pour créer des tickets

## 📊 Statistiques & Monitoring

### **Métriques Trackées**
- Total de tickets créés
- Tickets actuellement ouverts
- Répartition support/recrutement
- Tickets fermés avec succès
- Temps de résolution moyen

### **Commande Stats**
```
📊 Statistiques des tickets

🎫 Total créés: 47
📖 Actuellement ouverts: 3
🎧 Support ouverts: 2
💼 Recrutement ouverts: 1
✅ Fermés: 44
```

## 🔧 Configuration Avancée

### **Personnaliser les Messages**
Modifiez les embeds dans le code :
```python
support_embed = discord.Embed(
    title="🎧 Support Technique",
    description="Votre message personnalisé...",
    color=discord.Color.blue()
)
```

### **Modifier les Channels**
Changez les IDs dans la configuration :
```python
default_guild = {
    "channels": {
        "support": VOTRE_CHANNEL_ID,
        "recrutement": VOTRE_CHANNEL_ID,
        "logs": VOTRE_CHANNEL_ID
    }
}
```

### **Customiser les Permissions**
Ajustez la fonction de création des permissions :
```python
overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    # Ajouter d'autres rôles...
}
```

## 🐛 Résolution de Problèmes

### Boutons non fonctionnels
1. Vérifier que le cog est chargé : `!loaded`
2. Reconfigurer : `!tickets setup`
3. Contrôler les permissions du bot

### Tickets non créés
1. Vérifier les permissions `Manage Channels`
2. S'assurer que la catégorie existe
3. Contrôler l'espace disponible (limite 50 channels/catégorie)

### Logs non sauvegardés
1. Vérifier les permissions `Attach Files`
2. Contrôler l'existence du channel de logs
3. Tester la sauvegarde manuelle

### Erreurs de permissions
1. Vérifier que l'utilisateur est admin pour les commandes de gestion
2. Contrôler les permissions du bot dans la catégorie
3. Tester dans un autre serveur

## 📝 Maintenance

### **Nettoyage Automatique**
- Suppression automatique des tickets fermés
- Sauvegarde préservée dans le channel de logs
- Gestion intelligente des doublons

### **Optimisation des Performances**
```python
# Vues persistantes pour éviter les redémarrages
self.bot.add_view(self.support_view)
self.bot.add_view(self.recruitment_view)
```

### **Gestion des Erreurs**
- Try/catch sur toutes les opérations sensibles
- Messages d'erreur informatifs pour les utilisateurs
- Logs détaillés pour le debugging

## 🔄 Mises à Jour

### Version 1.0.0 (Actuelle)
- ✅ Système complet de tickets avec boutons
- ✅ Deux types : Support et Recrutement
- ✅ Sauvegarde HTML automatique et manuelle
- ✅ Gestion des permissions avancée
- ✅ Interface utilisateur moderne
- ✅ Statistiques et monitoring

### Améliorations futures
- 🔮 Système de catégories personnalisées
- 🔮 Templates de réponses automatiques
- 🔮 Intégration avec systèmes externes
- 🔮 Notifications webhook
- 🔮 Système de priorités
- 🔮 Temps de réponse automatiques

## ⚠️ Considérations Importantes

### **Limites Discord**
- Maximum 50 channels par catégorie
- Limite de 500 channels par serveur
- Taille maximale des fichiers HTML : 8MB

### **Confidentialité**
- Tickets strictement privés
- Logs sécurisés dans channel dédié
- Aucun accès externe possible

### **Performance**
- Vues persistantes pour optimiser les redémarrages
- Traitement asynchrone des créations
- Gestion intelligente de la mémoire

## 🤝 Support

Pour assistance et questions :
1. Vérifier `!tickets stats` pour l'état du système
2. Consulter les logs du bot
3. Tester dans un serveur de développement
4. Contacter l'équipe de développement

## 🎯 Bonnes Pratiques

1. **Configuration initiale** avec `!tickets setup`
2. **Monitoring régulier** des statistiques
3. **Nettoyage périodique** des anciens logs HTML
4. **Formation du staff** sur l'utilisation du système
5. **Sauvegarde** des configurations importantes
6. **Test préalable** avant mise en production

---

*Système de tickets professionnel pour une gestion efficace du support et du recrutement ! 🎫* 
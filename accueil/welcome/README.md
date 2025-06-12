# 🎉 Welcome - Système de Bienvenue Spike Rush

## 📋 Description
Système de bienvenue automatique avec messages personnalisés, GIF d'accueil et embeds stylés pour le serveur Spike Rush.

## ✨ Fonctionnalités

### 🎯 **Messages Automatiques**
- Détection automatique des nouveaux membres
- Messages de bienvenue personnalisés avec mentions
- GIF intégré pour l'ambiance gaming
- Embeds stylés aux couleurs du serveur

### 🎨 **Design & Styling**
- Couleurs personnalisées (bleu Discord)
- Avatar du membre affiché
- Informations détaillées (date d'arrivée, compte créé)
- Footer personnalisé "Spike Rush"

### ⚙️ **Configuration**
- Channel de bienvenue : `1380560522977742909`
- GIF par défaut : Animation gaming intégrée
- Messages configurables via commandes admin

## 🚀 Installation

```bash
# Charger le cog
!load accueil.welcome

# Configurer le channel (optionnel, déjà configuré)
!welcome setchannel #salon-bienvenue

# Tester le message
!welcome test
```

## 🎮 Commandes

### **Commandes Admin** (Permissions requises)
- `!welcome setchannel <channel>` - Définir le channel de bienvenue
- `!welcome setmessage <message>` - Personnaliser le message
- `!welcome toggle` - Activer/Désactiver les messages
- `!welcome test` - Tester le message de bienvenue
- `!welcome config` - Voir la configuration actuelle

### **Exemple de personnalisation**
```bash
!welcome setmessage "Salut {user} ! Bienvenue sur **Spike Rush** ! 🎮 
Prends tes armes et rejoins-nous dans l'arène !"
```

## 📊 Variables Disponibles

Dans les messages personnalisés, vous pouvez utiliser :
- `{user}` - Mention du nouveau membre
- `{username}` - Nom d'utilisateur 
- `{server}` - Nom du serveur
- `{member_count}` - Nombre total de membres

## 🎯 Configuration par Défaut

```python
Channel: 1380560522977742909
GIF: https://media.discordapp.net/attachments/...
Message: "Bienvenue {user} sur **Spike Rush** ! 🎮..."
Activé: True
```

## 🔧 Fonctionnement Technique

1. **Événement** : `on_member_join` détecte les arrivées
2. **Vérification** : Contrôle que le membre n'est pas un bot
3. **Génération** : Création de l'embed personnalisé
4. **Envoi** : Message posté dans le channel configuré
5. **Logs** : Enregistrement pour le suivi

## 🎨 Aperçu du Message

```
🎉 Nouveau Membre !
Bienvenue wica sur Spike Rush ! 🎮

Prépare-toi pour des battles épiques et rejoins notre communauté de gamers ! 
N'hésite pas à consulter les règles et à te présenter.

👤 Membre: @wica
📅 Arrivé le: 25/12/2024 à 15:30
🎯 Membre n°: 150
⭐ Compte créé: Il y a 2 ans

[GIF gaming animé]

Spike Rush - Bienvenue dans l'arène !
```

## 🔒 Permissions Requises

**Bot :**
- `Send Messages` - Envoyer des messages
- `Embed Links` - Intégrer des liens
- `Attach Files` - Joindre des fichiers (pour les GIF)
- `Read Message History` - Lire l'historique

**Admin :**
- `Manage Guild` - Gérer le serveur (pour les commandes de config)

## 🐛 Résolution de Problèmes

### Le bot ne répond pas aux arrivées
1. Vérifier que le cog est chargé : `!loaded`
2. Contrôler les permissions du bot
3. Vérifier la configuration : `!welcome config`

### Messages non affichés
1. Vérifier que le channel existe
2. Contrôler les permissions dans le channel
3. Vérifier que les événements sont activés

### GIF non affiché
1. Vérifier la validité de l'URL
2. Contrôler la taille du fichier
3. Tester avec une autre image

## 📝 Changelog

### Version 1.0.0
- ✅ Messages automatiques de bienvenue
- ✅ Embeds stylés avec GIF
- ✅ Commandes de configuration
- ✅ Variables dynamiques
- ✅ Gestion des permissions

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez ce README
2. Testez avec `!welcome test`
3. Consultez les logs du bot
4. Contactez un administrateur 
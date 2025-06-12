# 📜 Règlement PP - Système de Parties Personnalisées

## 🎯 Description

Le système **ReglementPP** est un cog Red-DiscordBot qui gère automatiquement les règles des parties personnalisées Valorant pour **Radiant Order**. Il propose un règlement stylé avec des boutons interactifs pour l'acceptation des règles et la gestion des notifications.

## ✨ Fonctionnalités

### 🎨 **Interface Moderne**
- **4 embeds** avec design coloré et thématique
- **Logo Valorant** intégré
- **Boutons persistants** (fonctionnent après redémarrage)
- **Messages éphémères** pour les interactions

### 🔘 **Boutons Interactifs**
- **✅ J'accepte les règles PP** : Attribution automatique du rôle d'accès
- **🔔 Notifications PP** : Toggle du rôle de notifications

### 📊 **Gestion Administrative**
- Configuration flexible des channels et rôles
- Statistiques détaillées
- Système de permissions intégré

## 🚀 Installation

1. Placez le dossier `reglementpp` dans votre répertoire cogs RedBot
2. Chargez le cog : `!load reglementpp`
3. Configurez les paramètres (optionnel, pré-configuré)
4. Déployez le règlement : `!reglementpp setup`

## ⚙️ Configuration

### 🎯 **Paramètres par Défaut**
```python
Channel règlement : 1380560604376596500
Rôle règles PP   : 1380615723692326992
Rôle notifications: 1380616851427557406
```

### 🛠️ **Commandes de Configuration**

| Commande | Description |
|----------|-------------|
| `!reglementpp` | Afficher la configuration actuelle |
| `!reglementpp setup` | Déployer le règlement complet |
| `!reglementpp channel <#channel>` | Changer le channel du règlement |
| `!reglementpp rulesrole <@role>` | Définir le rôle d'accès PP |
| `!reglementpp notifsrole <@role>` | Définir le rôle de notifications |
| `!reglementpp stats` | Voir les statistiques |

## 📋 Structure du Règlement

### 1. **📜 Introduction**
- Présentation du système PP de Radiant Order
- Message d'accueil convivial

### 2. **⚡ Préparation**
- **👑 Gestion Staff** : Rôle des organisateurs
- **⚖️ Formation des Équipes** : Obligation d'indiquer son peak elo
- **🗺️ Sélection de Map** : Système de roulette avec votes
- **✅ Validation** : Acceptation des règles obligatoire

### 3. **🎮 Règles en Jeu**
- **🔫 Limites d'Armes** : 1 Odin, 1 Judge, 1 Operator par équipe
- **🗣️ Communication** : Chat vocal autorisé avant les manches
- **🚫 Interdictions** : Instalock, trashtalk, smurf, absence non justifiée

### 4. **🎯 Objectif**
- Esprit fair-play pour tous les niveaux
- Sanctions pour attitudes négatives
- Boutons d'interaction

## 🔒 Permissions Requises

### 🤖 **Pour le Bot**
- `Manage Roles` (Gérer les rôles)
- `Send Messages` (Envoyer des messages)
- `Embed Links` (Intégrer des liens)
- `Use External Emojis` (Utiliser des emojis externes)

### 👤 **Pour les Administrateurs**
- `Manage Guild` (Gérer le serveur) ou permissions administrateur

## 📊 Fonctionnement des Boutons

### ✅ **Acceptation des Règles**
```python
# Vérifie si l'utilisateur a déjà le rôle
if rules_role in user.roles:
    return "Déjà validé"

# Ajoute le rôle d'accès PP
await user.add_roles(rules_role)
# Message de confirmation éphémère
```

### 🔔 **Notifications PP**
```python
# Toggle du rôle
if notifs_role in user.roles:
    await user.remove_roles(notifs_role)  # Désactiver
else:
    await user.add_roles(notifs_role)     # Activer
```

## 📈 Statistiques

Le système track automatiquement :
- **Nombre de joueurs** ayant accepté les règles
- **Nombre d'abonnés** aux notifications
- **Taux de participation** aux notifications

## 🎨 Personnalisation

### 🎨 **Couleurs des Embeds**
```python
Introduction : 0x5865F2  # Bleu Discord
Préparation  : 0xFEE75C  # Jaune
Règles       : 0xED4245  # Rouge
Objectif     : 0x57F287  # Vert
```

### 🖼️ **Images**
- **Thumbnail** : Logo Valorant officiel
- **Footer** : Icône du serveur (si disponible)

## 🐛 Dépannage

### ❌ **Erreurs Communes**

| Erreur | Solution |
|--------|----------|
| "Rôle non configuré" | Vérifier les IDs de rôles dans la config |
| "Permissions insuffisantes" | Donner les rôles `Manage Roles` au bot |
| "Channel introuvable" | Configurer le bon channel avec `!reglementpp channel` |

### 🔧 **Commandes de Debug**
```bash
!reglementpp              # Voir la config actuelle
!reglementpp stats        # Vérifier les statistiques
!reglementpp cleanup      # Nettoyer si nécessaire
```

## 📝 Changelog

### v1.0.0 (Actuel)
- ✅ Système de règlement complet
- ✅ Boutons persistants
- ✅ Configuration flexible
- ✅ Statistiques intégrées
- ✅ Design moderne avec embeds colorés

## 💡 Support

Pour toute question ou problème :
1. Vérifiez la configuration avec `!reglementpp`
2. Consultez les logs du bot
3. Vérifiez les permissions Discord

---

**🎮 Développé pour Radiant Order - Valorant Community** 
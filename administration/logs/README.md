# 🔍 Track Cog - Système de Logging

Cog automatisé pour créer un système complet de tracking et logging des événements Discord.

## ✨ Fonctionnalités

- **Création automatique** de la catégorie "📊 Track"
- **10 channels de logging** spécialisés
- **Permissions configurées** automatiquement
- **Sauvegarde des IDs** pour intégration avec d'autres bots
- **Gestion complète** du système

## 🚀 Installation

1. **Ajouter le chemin :**
   ```
   !addpath /home/wica/cogs/administration/logs
   ```

2. **Charger le cog :**
   ```
   !load track
   ```

## 📋 Channels créés automatiquement

| Channel | Description |
|---------|-------------|
| 💬 Messages | Logs des messages envoyés |
| 🖼️ Images | Logs des images partagées |
| 🗑️ Deletes | Logs des messages supprimés |
| 🎤 Voice | Logs des événements vocaux |
| 📥 Joins | Logs des arrivées de membres |
| ✏️ Edits | Logs des messages modifiés |
| 📤 Leaves | Logs des départs de membres |
| 🏷️ Roles | Logs des modifications de rôles |
| 🔨 Bans | Logs des bannissements |
| 😀 Reactions | Logs des réactions |

## 🛠️ Commandes disponibles

### `!track setup`
Crée automatiquement toute la structure Track :
- Catégorie "📊 Track"
- Tous les 10 channels de logging
- Permissions appropriées
- Sauvegarde des IDs

### `!track ids`
Affiche tous les IDs des channels créés pour pouvoir les utiliser dans d'autres configurations.

### `!track status`
Vérifie l'état du système Track et indique s'il y a des problèmes.

### `!track reset`
Supprime complètement le système existant et le recrée (avec confirmation).

## 🔧 Permissions requises

- **Gérer les channels** pour créer/supprimer
- **Gérer les catégories** pour la structure
- **Voir les channels** pour vérifier l'état

## 🎯 Utilisation

1. **Configuration initiale :**
   ```
   !track setup
   ```

2. **Récupérer les IDs :**
   ```
   !track ids
   ```

3. **Vérifier le statut :**
   ```
   !track status
   ```

## 📊 Exemple de résultat

Après `!track setup`, vous obtiendrez :
```
📊 Track/
├── 💬 messages (ID: 123456789)
├── 🖼️ images (ID: 123456790)
├── 🗑️ deletes (ID: 123456791)
├── 🎤 voice (ID: 123456792)
├── 📥 joins (ID: 123456793)
├── ✏️ edits (ID: 123456794)
├── 📤 leaves (ID: 123456795)
├── 🏷️ roles (ID: 123456796)
├── 🔨 bans (ID: 123456797)
└── 😀 reactions (ID: 123456798)
```

## 🔗 Intégration

Les IDs générés peuvent être utilisés pour configurer :
- Autres bots de logging (Carl-bot, Dyno, etc.)
- Webhooks personnalisés
- Systèmes de monitoring
- Intégrations externes

## 🛡️ Sécurité

- Channels **privés** par défaut (seuls les admins peuvent voir)
- Permissions **automatiquement configurées**
- Bot a les permissions **lecture/écriture** nécessaires

---
*Système de tracking professionnel pour serveurs Discord organisés ! 🔍* 
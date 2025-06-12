# 🔨 Système de Sanctions - Radiant Order

## 📋 Description
Système de sanctions progressives avec escalade automatique pour le serveur Radiant Order. Le système applique des sanctions de plus en plus sévères à chaque avertissement.

## ⚙️ Fonctionnalités

### 🔄 Escalade automatique des sanctions
- **Avertissement 1** : Timeout de 1 jour + message privé
- **Avertissement 2** : Timeout de 1 semaine + message privé  
- **Avertissement 3** : Ban définitif + message privé avec info de débannissement

### 📨 Messages privés automatiques
- Envoyés **AVANT** l'application de la sanction
- Contiennent la raison et les informations sur la durée
- Pour les bans définitifs : lien vers le site de débannissement

### 📊 Logging automatique
- Tous les logs envoyés dans le canal ID: `1380560668897443971`
- Embeds détaillés avec informations du modérateur et du membre
- Historique complet des sanctions

## 🎯 Commandes

### `!sanction user @membre <raison>`
Applique la prochaine sanction à un membre.
- La raison est **obligatoire**
- Escalade automatique selon l'historique

### `!sanction info @membre`
Affiche l'historique des sanctions d'un membre.

### `!sanction reset @membre`
Remet à zéro le compteur de sanctions d'un membre.

### `!sanction untimeout @membre`
Retire le timeout d'un membre manuellement.

### `!sanction unban <user_id>`
Débannit un utilisateur par son ID.

### `!sanction list`
Affiche la liste de tous les membres sanctionnés.

## 🔐 Permissions requises
- Rôles autorisés : Administrateurs, Modérateurs, Staff autorisé
- Permission `ban_members` requise pour les bans
- Permission `moderate_members` requise pour les timeouts

## 📁 Fichiers
- `sanction.py` : Code principal du système
- Configuration automatique des paramètres

## 🚀 Installation
1. Charger le cog : `!load administration.moderation.ban.sanction`
2. Le système est automatiquement configuré
3. Canal de logs : `1380560668897443971`

## ⚠️ Important
- Les raisons sont obligatoires pour toutes les sanctions
- Les messages privés sont envoyés avant les sanctions
- Système d'escalade automatique non modifiable
- Logs détaillés pour tous les actions

# ⚖️ Système de Ban - Modération Progressive

## 🎯 Description

Le **BanSystem** est un cog Red-DiscordBot qui implémente un système de modération avec avertissements progressifs pour **Radiant Order**. Il gère automatiquement les sanctions avec 3 niveaux d'escalade et inclut un système de JAIL permanente.

## ✨ Fonctionnalités

### 🔥 **Système d'Avertissements Progressifs**
- **3 niveaux** de sanctions automatiques
- **Escalade progressive** selon les infractions
- **Persistance** des avertissements même après déconnexion
- **Gestion automatique** des retours de membres

### 🛡️ **Sécurité & Permissions**
- **Rôles autorisés** configurables
- **Vérification hiérarchique** des rôles
- **Protection** contre l'auto-bannissement
- **Logs automatiques** des actions

### 🔒 **Système JAIL Avancé**
- **Suppression automatique** de tous les rôles
- **Accès restreint** au salon JAIL uniquement
- **Réapplication automatique** en cas de retour
- **Persistance permanente** des sanctions

## 🚀 Installation

1. Placez le dossier `ban` dans votre répertoire cogs RedBot
2. Chargez le cog : `!load ban`
3. Les paramètres sont pré-configurés pour Radiant Order
4. Utilisez `!ban` pour voir l'aide

## ⚙️ Configuration

### 🎯 **Paramètres par Défaut**
```python
# Rôles autorisés à utiliser les commandes
authorized_roles: [1380562058461839400, 1380562966575059116, 1380563626846322819]

# Rôles de sanction
ban_week_role: 1380609528239882332  # Ban 1 semaine
jail_role: 1380625102940667925      # JAIL permanente

# Channel JAIL
jail_channel: 1380625688482152499
```

## 📋 Système d'Avertissements

### 🔢 **Niveaux de Sanction**

| Avertissement | Sanction | Durée | Description |
|---------------|----------|-------|-------------|
| **1er** 🕐 | Timeout | 24 heures | Restriction temporaire |
| **2ème** 🚫 | Ban Rôle | 1 semaine | Rôle de bannissement |
| **3ème** 🔒 | JAIL | Permanent | Isolation complète |

### ⚡ **Escalade Automatique**
- **Timeout → Ban** : Suppression automatique du timeout
- **Ban → JAIL** : Retrait du rôle ban + nettoyage complet
- **Compteur persistant** : Les avertissements sont sauvegardés

## 🛠️ Commandes

### 📊 **Commandes Principales**

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!ban user <@membre> [raison]` | Appliquer un avertissement | `!ban user @John spam répétitif` |
| `!ban info <@membre>` | Voir les avertissements | `!ban info @John` |
| `!ban reset <@membre> [raison]` | Remettre à zéro | `!ban reset @John seconde chance` |
| `!ban list` | Lister tous les avertissements | `!ban list` |
| `!ban` | Afficher l'aide | `!ban` |

### 🔨 **Détail des Commandes**

#### **!ban user**
```bash
!ban user @membre [raison]
```
- **Applique** l'avertissement suivant au membre
- **Incrémente** automatiquement le compteur
- **Applique** la sanction correspondante
- **Envoie** un MP informatif au membre

#### **!ban info**
```bash
!ban info @membre
```
- **Affiche** le nombre d'avertissements
- **Montre** le statut de sanction actuel
- **Indique** la date du dernier avertissement
- **Liste** les rôles actuels du membre

#### **!ban reset**
```bash
!ban reset @membre [raison]
```
- **Supprime** tous les avertissements
- **Retire** toutes les sanctions actives
- **Envoie** une notification au membre
- **Log** l'action de réinitialisation

#### **!ban list**
```bash
!ban list
```
- **Liste** tous les membres avec avertissements
- **Trie** par nombre d'avertissements
- **Limite** à 20 entrées maximum
- **Affiche** le statut de chaque membre

## 🔒 Système JAIL Détaillé

### 🏗️ **Fonctionnement**
1. **Application** : Au 3ème avertissement
2. **Nettoyage** : Suppression de tous les rôles
3. **Isolation** : Accès au salon JAIL uniquement
4. **Persistance** : Sauvegarde permanente

### 🔄 **Gestion des Retours**
```python
@commands.Cog.listener()
async def on_member_join(self, member):
    # Vérification automatique des avertissements
    # Réapplication de la JAIL si nécessaire
    # Nettoyage des rôles
    # Log de l'action
```

### 📡 **Détection Automatique**
- **Listener** sur les rejointes de membres
- **Vérification** du niveau d'avertissement
- **Réapplication** automatique de la JAIL
- **Logs** dans les channels de modération

## 🔐 Permissions Requises

### 🤖 **Pour le Bot**
- `Manage Roles` (Gérer les rôles)
- `Moderate Members` (Modérer les membres - timeout)
- `Send Messages` (Envoyer des messages)
- `Embed Links` (Intégrer des liens)

### 👤 **Pour les Modérateurs**
- Avoir l'un des **rôles autorisés** configurés
- **Hiérarchie** : Ne peut pas sanctionner un rôle égal/supérieur

## 📊 Fonctionnalités Avancées

### 💬 **Messages Privés Automatiques**
```python
# Message envoyé au membre sanctionné
title="⚖️ Sanction Reçue - Radiant Order"
- Numéro d'avertissement (X/3)
- Type de sanction appliquée
- Raison de la sanction
- Avertissement pour le prochain niveau
```

### 📋 **Logs Automatiques**
- **Recherche automatique** des channels de logs
- **Détection** des mots-clés "mod" ou "log"
- **Embeds stylés** avec toutes les informations
- **Timestamps** et métadonnées complètes

### 🛡️ **Sécurités Intégrées**
- **Vérification hiérarchique** des rôles
- **Protection auto-bannissement**
- **Gestion d'erreurs** complète
- **Validation des permissions**

## 🎨 Interface Utilisateur

### 📱 **Embeds Modernes**
- **Couleurs dynamiques** selon la gravité
- **Emojis thématiques** pour chaque action
- **Informations complètes** et structurées
- **Footer** avec branding Radiant Order

### 🎯 **Codes Couleur**
```python
Avertissement 1: Orange  (discord.Color.orange())
Avertissement 2: Rouge   (discord.Color.red())
Avertissement 3: Rouge foncé (discord.Color.dark_red())
Reset: Vert             (discord.Color.green())
```

## 🐛 Dépannage

### ❌ **Erreurs Communes**

| Erreur | Cause | Solution |
|--------|-------|----------|
| "Permissions insuffisantes" | Bot sans droits | Donner `Manage Roles` |
| "Rôle introuvable" | ID incorrect | Vérifier les IDs de rôles |
| "Hiérarchie invalide" | Rôle trop bas | Repositionner le rôle du bot |

### 🔧 **Commandes de Debug**
```bash
!ban info @membre     # Vérifier l'état d'un membre
!ban list            # Voir tous les avertissements
```

### 📊 **Vérifications**
1. **Permissions** : Bot a `Manage Roles`
2. **Hiérarchie** : Rôle bot au-dessus des rôles de sanction
3. **Configuration** : IDs de rôles corrects
4. **Channels** : Channel JAIL accessible

## 🔄 Workflow Complet

### 📈 **Exemple d'Escalade**
```
1. Membre fait du spam
   → !ban user @membre spam dans le chat
   → Timeout 24h + Notification MP

2. Membre récidive après timeout
   → !ban user @membre récidive de spam  
   → Ban 1 semaine (rôle) + Fin timeout

3. Membre récidive encore
   → !ban user @membre spam persistant
   → JAIL permanente + Suppression tous rôles

4. Membre quitte et revient
   → Détection automatique
   → Réapplication JAIL + Log
```

## 📝 Données Sauvegardées

### 💾 **Structure de Données**
```json
{
  "user_warnings": {
    "123456789": {
      "count": 2,
      "last_warning": "2024-01-15T14:30:00"
    }
  }
}
```

### 🔄 **Persistance**
- **Sauvegarde automatique** après chaque action
- **Conservation** même après redémarrage du bot
- **Historique** des avertissements
- **Timestamps** précis

## 💡 Conseils d'Utilisation

### 📚 **Bonnes Pratiques**
1. **Communiquez** clairement les règles
2. **Documentez** les raisons des sanctions
3. **Utilisez** le reset avec parcimonie
4. **Vérifiez** régulièrement la liste des avertissements

### ⚖️ **Modération Équitable**
- **Escalade progressive** respectée
- **Raisons explicites** pour chaque sanction
- **Notifications** systématiques aux membres
- **Possibilité de reset** pour seconde chance

## 📈 Métriques & Suivi

### 📊 **Statistiques Disponibles**
- **Nombre total** d'avertissements actifs
- **Répartition** par niveau de sanction
- **Historique** des sanctions appliquées
- **Membres** en JAIL permanente

---

**⚖️ Développé pour Radiant Order - Justice et Fair-Play** 
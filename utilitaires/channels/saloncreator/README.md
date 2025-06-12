# 🏗️ SalonCreator - Cog RedBot

Un cog RedBot pour créer automatiquement toute la structure de salons de votre serveur Discord Time 2 Clutch avec les bonnes émojis.

## 📋 Description

Ce cog permet de créer automatiquement tous les salons et catégories de votre serveur Discord selon une structure prédéfinie, avec leurs émojis correspondants. Parfait pour créer rapidement l'architecture complète d'un serveur gaming/esport.

## 🚀 Installation

### Prérequis
- RedBot v3.5+ installé et configuré
- Permissions administrateur sur le serveur Discord
- Le bot doit avoir les permissions de créer des salons et catégories

### Étapes d'installation

1. **Téléchargez ou clonez les fichiers du cog dans votre dossier `cogs/`**
   ```
   cogs/
   └── saloncreator/
       ├── __init__.py
       ├── saloncreator.py
       └── README.md
   ```

2. **Ajoutez le chemin des cogs à RedBot (si pas déjà fait)**
   ```
   !addpath /chemin/vers/vos/cogs
   ```

3. **Chargez le cog**
   ```
   !load saloncreator
   ```

4. **Vérifiez que le cog est chargé**
   ```
   !cogs
   ```

## 🎮 Utilisation

### Commandes disponibles

#### `!salon` ou `!salon help`
Affiche l'aide des commandes disponibles.

#### `!salon structure`
Affiche un aperçu complet de la structure qui sera créée.
- **Permissions :** Aucune permission spéciale requise
- **Usage :** `!salon structure`

#### `!salon create CONFIRMER`
Crée toute la structure de salons du serveur.
- **Permissions requises :** Administrateur ou permission "Gérer le serveur"
- **Confirmation obligatoire :** Vous devez taper exactement `CONFIRMER`
- **Usage :** `!salon create CONFIRMER`

#### `!salon clean CONFIRMER`
Supprime toutes les catégories vides du serveur.
- **Permissions requises :** Administrateur ou permission "Gérer le serveur"
- **Confirmation obligatoire :** Vous devez taper exactement `CONFIRMER`
- **Usage :** `!salon clean CONFIRMER`

## 📁 Structure créée

Le cog créera **7 catégories** avec plus de **40 salons** :

### 👋 Bienvenue (6 salons)
- 📘-bienvenue
- 📜-règlement
- 📁-auto-rôles
- 🚩-support
- 📧-recrutements
- ✨-nous-soutenir

### ℹ️ Informations (5 salons)
- 📢-annonces
- 🎉-giveaways
- 🏆-tournois
- 🔔-soutiens
- 📊-sondages

### 👥 Communauté (5 salons)
- 🧠-clip-pp
- 🌱-ranked
- 🗨️-suggestions
- 💻-commandes
- 🧡-vos-réseaux

### 😎 Time 2 Chill (5 salons)
- 👨‍🍳-time2cook
- 🎨-time2draw
- 📖-time2read
- 👀-time2watch
- 🎮-time2play

### 🎮 PARTIES PERSO (6 salons)
- 🟢-parties-perso
- 📋-règlement-pp
- 👑-roulette-maps
- 🚩-party-code
- 🚩-party-code-staff
- 🚩-demande-organisateur

### 📺 Show Matchs (3 salons vocaux)
- 🎭-Préparation 1 (vocal)
- 🎭-Attaque (vocal)
- 🎭-Défense (vocal)

### 🛠️ SUPPORT (20 salons)
- 📣-annonce-importante
- ⚠️-signalements
- screenshot
- ⚠️-discussion-staff
- ⚠️-compte-rendu
- ⚠️-comment-sanctionner
- ⚠️-sanction
- ⚠️-record-potentiel-cheat
- 🎉-giveaway
- ⚠️-historique-sanction
- 🎫-ancien-tickets
- ⚠️-headstaff
- ⚠️-graphismes
- ⚠️-inscription-tournoi
- ⚠️-demande-web
- ⚠️-rank-radiant
- ⚠️-stats-staff
- 💬-Entretien (vocal)
- 🔒-Staff (vocal)
- 📊-réunion (vocal)

## ✨ Fonctionnalités

- ✅ **Détection automatique** : Ne recrée pas les salons/catégories existants
- ✅ **Création progressive** : Mise à jour en temps réel du statut
- ✅ **Gestion d'erreurs** : Rapport détaillé des éventuels problèmes
- ✅ **Rate limiting** : Pause automatique pour respecter les limites Discord
- ✅ **Support mixte** : Salons textuels et vocaux
- ✅ **Sécurité** : Confirmation obligatoire pour éviter les erreurs
- ✅ **Permissions** : Vérification des permissions administrateur

## 🔧 Exemple d'utilisation

```bash
# 1. Voir la structure qui sera créée
!salon structure

# 2. Créer tous les salons (attention à bien taper CONFIRMER)
!salon create CONFIRMER

# 3. Nettoyer les catégories vides si besoin
!salon clean CONFIRMER
```

## ⚠️ Notes importantes

### Performance
- La création complète peut prendre **5-10 minutes** selon le serveur
- Une pause de 0.5 seconde est appliquée entre chaque création
- Le processus affiche le progrès en temps réel

### Permissions requises
- Le bot doit avoir la permission **"Gérer les salons"**
- L'utilisateur doit être **Administrateur** ou avoir **"Gérer le serveur"**

### Sécurité
- Confirmation obligatoire avec le mot exact `CONFIRMER`
- Les salons existants ne sont jamais supprimés ou modifiés
- Seules les catégories complètement vides peuvent être supprimées

### Limites Discord
- Discord limite la création de salons (rate limit)
- Le script respecte automatiquement ces limites
- En cas d'erreur de rate limit, relancez simplement la commande

## 🛠️ Dépannage

### Le cog ne se charge pas
```bash
# Vérifiez que le chemin est correct
!addpath /chemin/vers/vos/cogs

# Rechargez le cog
!reload saloncreator
!load saloncreator
```

### Erreur de permissions
- Vérifiez que le bot a les permissions "Gérer les salons"
- Vérifiez que vous êtes administrateur du serveur

### Création interrompue
- La commande peut être relancée sans problème
- Les salons déjà créés ne seront pas dupliqués

### Erreurs de rate limit
- Attendez quelques minutes
- Relancez la commande `!salon create CONFIRMER`

## 📝 Logs et debug

Pour voir les logs détaillés en cas de problème :
```bash
!set serverprefix .
.debug
```

## 🔄 Mise à jour

Pour mettre à jour le cog :
```bash
!unload saloncreator
# Remplacez les fichiers
!load saloncreator
```

## 🆘 Support

En cas de problème :
1. Vérifiez les permissions du bot
2. Consultez les logs avec `!debug`
3. Testez d'abord avec `!salon structure`
4. Assurez-vous d'avoir tapé exactement `CONFIRMER`

## 📄 Licence

Ce cog est fourni tel quel pour RedBot. Libre d'utilisation et de modification.

---

**Développé pour le serveur Time 2 Clutch** 🎮 
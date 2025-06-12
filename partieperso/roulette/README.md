# 🎲 Roulette MAP Valorant - Radiant Order

## 📋 Description
Système de roulette de maps Valorant avec mécanisme de vote interactif pour choisir la map de jeu de manière démocratique.

## ⚙️ Fonctionnalités

### 🎮 Maps Valorant intégrées
- **ASCENT** - Map classique avec mid control
- **BIND** - Map avec téléporteurs 
- **BREEZE** - Map longue portée
- **FRACTURE** - Map avec spawn splité
- **HAVEN** - Map à 3 sites
- **ICEBOX** - Map verticale
- **LOTUS** - Map avec mécaniques rotations
- **PEARL** - Map underwater theme
- **SPLIT** - Map verticale urbaine
- **SUNSET** - Map récente
- **ABYSS** - Map la plus récente

### 🗳️ Système de vote interactif
- **Vote accept/reject** : Les joueurs peuvent accepter ou refuser la map
- **Seuil minimum** : 6 votes nécessaires pour valider un choix
- **Timeout** : 60 secondes pour voter
- **Vote unique** : Chaque utilisateur ne peut voter qu'une fois
- **Relance automatique** : Si la map est refusée, nouvelle roulette

### 🎨 Animation immersive
- **Animation de chargement** : GIF et effets visuels
- **Défilement de maps** : Simulation de roulette
- **Effet de ralentissement** : Suspense avant le résultat
- **Embeds dynamiques** : Couleurs et informations en temps réel

### 📊 Informations détaillées
- **Compteurs de votes** : Affichage en temps réel
- **Temps restant** : Compte à rebours visible
- **Auteur de la roulette** : Identification du lanceur
- **Résultats colorés** : Vert (accepté), Rouge (refusé), Jaune (timeout)

## 🎯 Commandes

### `!roulette`
Lance une roulette de map avec système de vote.
- Commande réservée aux rôles autorisés
- Fonctionne dans le canal dédié ou redirige automatiquement
- Supprime automatiquement la commande pour garder le canal propre

## 🔐 Rôles autorisés

### 👑 Staff autorisé
- **Administrateur** (ID: 1380562058461839400)
- **Responsables** (ID: 1380562966575059116)
- **Assistants Responsable** (ID: 1380575934410915911)
- **Modérateurs** (ID: 1380563626846322819)
- **Helper** (ID: 1380564333242613821)
- **Staff Interne** (ID: 1380574085708513340)
- **Développeur** (ID: 1380574650689388695)
- **Ressources Humaines** (ID: 1380573287834456184)

### 🔑 Accès spécial
- **Wicaebeth** (ID: 257152912776495104) - Accès automatique

## ⚙️ Configuration

### 📺 Canal de roulette
- Canal ID: `1380560607383912511`

### 🗳️ Paramètres de vote
- **Votes minimum requis** : 6 votes
- **Durée du vote** : 60 secondes
- **Boutons** : ✅ Accepter / ❌ Refuser

### 🎨 Éléments visuels
- **GIF de chargement** : Animation immersive
- **Images des maps** : Visuels haute qualité pour chaque map
- **Thumbnails** : Logo du serveur
- **Avatars** : Photo de profil de l'utilisateur

## 🔄 Flux de fonctionnement

1. **Lancement** : Utilisateur tape `!roulette`
2. **Animation** : Chargement avec défilement de maps
3. **Résultat** : Affichage de la map sélectionnée
4. **Vote** : 60 secondes pour voter accept/reject
5. **Décision** :
   - ✅ 6+ votes "Accepter" → Map confirmée
   - ❌ 6+ votes "Refuser" → Nouvelle roulette
   - ⏰ Timeout → Map gardée par défaut

## 📁 Fichiers
- `maproulette.py` : Code principal du système
- Configuration intégrée dans le code

## 🚀 Installation
1. Charger le cog : `!load partieperso.roulette.maproulette`
2. Le système est automatiquement configuré
3. Canal de roulette : `1380560607383912511`

## ⚠️ Important
- Système de vote démocratique
- Relance automatique si map refusée
- Animation immersive pour l'expérience
- Restriction aux rôles autorisés seulement
- Nettoyage automatique des commandes 
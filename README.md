# 🤖 Structure des Cogs Red Bot

Cette arborescence organise les cogs Red Bot par catégories fonctionnelles pour une meilleure lisibilité et maintenance.

## 📁 Structure des Dossiers

### 🎉 **Accueil** (`accueil/`)
Gestion de l'arrivée et de l'intégration des nouveaux membres
- `welcome/` - Messages de bienvenue automatiques
- `verification/` - Système de vérification des nouveaux membres
- `regles/` - Affichage et gestion des règles du serveur

### ⚙️ **Administration** (`administration/`)
Outils d'administration et de gestion du serveur
- `moderation/` - Commandes de modération (ban, kick, mute, etc.)
- `permissions/` - Gestion des permissions et accès
- `roles/` - Attribution et gestion des rôles
- `logs/` - Système de journalisation des événements

### 🛠️ **Utilitaires** (`utilitaires/`)
Commandes et outils pratiques pour les utilisateurs
- `channels/` - Création et gestion des salons (ex: saloncreator)
- `messages/` - Gestion des messages (édition, suppression, etc.)
- `informations/` - Commandes d'information (userinfo, serverinfo, etc.)

### 🎮 **Divertissement** (`divertissement/`)
Cogs pour l'animation et le divertissement
- `jeux/` - Mini-jeux et activités ludiques
- `musique/` - Bot musique et gestion audio
- `interactions/` - Commandes d'interaction sociale (câlins, etc.)

### 💰 **Économie** (`economie/`)
Système économique du serveur
- `points/` - Gestion des points/monnaie virtuelle
- `boutique/` - Système d'achat et de vente
- `recompenses/` - Système de récompenses et achievements

## 🚀 Installation des Cogs

Pour charger un cog, utilisez la commande Red Bot :
```
[p]load <categorie>.<nom_du_cog>
```

Exemple : `[p]load utilitaires.channels.saloncreator`

## 📝 Conventions de Nommage

- **Dossiers** : en minuscules, mots descriptifs
- **Cogs** : nom explicite de la fonctionnalité
- **Structure** : `categorie/sous-categorie/nom_du_cog/`

## 🔧 Développement

Chaque cog doit contenir :
- `__init__.py` - Fichier d'initialisation
- `nom_du_cog.py` - Code principal du cog
- `README.md` - Documentation spécifique (optionnel)

---
*Structure optimisée pour Red Bot - Organisée par fonctionnalités* 
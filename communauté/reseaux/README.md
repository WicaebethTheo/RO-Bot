# 📱 Système Vos Réseaux - Radiant Order

## 📋 Description

Le système "Vos Réseaux" permet de gérer un canal dédié au partage de réseaux sociaux et créations personnelles des membres, avec des conditions d'accès pour maintenir la qualité du contenu et encourager l'activité communautaire.

## ✨ Fonctionnalités

### 🛡️ **Contrôle d'accès**
- **Double condition** : Rôle "Actif" OU whitelist administrateur
- **Message informatif** : Explique clairement les conditions
- **Encouragement** à l'activité communautaire

### 📱 **Gestion du contenu**
- **Types acceptés** : Réseaux sociaux, créations, projets gaming
- **Règles claires** : Contenu interdit explicitement listé
- **Nettoyage automatique** : Canal purgé avant chaque setup

### 🎨 **Interface professionnelle**
- **Design cohérent** : Emojis personnalisés Radiant Order
- **Organisation claire** : Informations structurées en sections
- **Guidance complète** : Instructions pour obtenir l'accès

## 🚀 Installation

### 1. Configuration initiale
```bash
# Charger le cog
!load vosreseaux

# Configurer le canal
!vosreseaux channel #vos-reseaux

# Configurer le rôle actif
!vosreseaux role @Actif

# Déployer le message informatif
!vosreseaux setup
```

### 2. Vérification
```bash
# Voir la configuration actuelle
!vosreseaux
```

## 📝 Utilisation

### 👥 **Pour les membres**

#### ✅ **Accès avec rôle Actif**
1. **Obtenir le rôle** par l'activité communautaire
2. **Poster librement** dans le canal vos réseaux
3. **Respecter les règles** de contenu

#### 🎫 **Accès par whitelist**
1. **Contacter le staff** en message privé
2. **Expliquer le contenu** à partager
3. **Attendre l'approbation** des modérateurs/administrateurs

### 🛡️ **Pour les administrateurs**

#### Commandes de configuration
```bash
# Voir la configuration
!vosreseaux

# Configurer le canal
!vosreseaux channel #vos-reseaux

# Configurer le rôle requis
!vosreseaux role @Actif

# Redéployer le message (purge le canal)
!vosreseaux setup
```

## 🎨 Interface Visuelle

### 📤 **Message informatif du canal**
```
💬 Vos Réseaux - Conditions de Publication

Bienvenue dans le canal vos réseaux ! 🌟

⚠️ Conditions pour poster dans ce canal :

✅ Option 1 : Avoir le rôle @Actif
👑 Option 2 : Demander une whitelist aux administrateurs/modérateurs

🔔 Pourquoi ces conditions ?
• ⚡ Maintenir la qualité du contenu
• 💙 Encourager l'activité communautaire
• ⏳ Éviter le spam et les contenus non pertinents

➡️ Comment obtenir l'accès ?
• Rôle Actif : Participez activement à la communauté
• Whitelist : Contactez un membre du staff en privé

💬 Partagez vos réseaux sociaux, chaînes, projets et créations !

┌─ 🔔 Types de contenus acceptés ─┐
• Chaînes YouTube/Twitch
• Profils Instagram/TikTok  
• Projets créatifs
• Contenu lié au gaming
• Créations artistiques

┌─ ❌ Contenus interdits ─┐
• Spam répétitif
• Contenu NSFW
• Publicités non liées
• Self-promotion excessive
• Liens malveillants
```

## ✅ Contenus Acceptés

### 🎮 **Gaming & Streaming**
- **Chaînes Twitch** : Streams gaming, discussions
- **Chaînes YouTube** : Gameplay, tutoriels, montages
- **Clips & Highlights** : Moments épiques, skillshots

### 🎨 **Créations Artistiques**
- **Fanart** : Dessins, illustrations Valorant/gaming
- **Montages vidéo** : Éditing, effets spéciaux
- **Musique** : Compositions, remixes, covers

### 📱 **Réseaux Sociaux**
- **Instagram** : Photos gaming, setup, lifestyle
- **TikTok** : Vidéos courtes, trends gaming
- **Twitter** : Partage de réflexions, actualités

### 💻 **Projets Techniques**
- **Développement** : Applications, sites web, outils
- **Design** : Logos, interfaces, branding
- **Streaming setup** : Configurations, overlays

## ❌ Contenus Interdits

### 🚫 **Spam & Répétition**
- **Posts répétitifs** : Même contenu plusieurs fois
- **Auto-promotion excessive** : Plus de 2-3 posts par semaine
- **Contenu non original** : Reposts sans attribution

### 🔞 **Contenu inapproprié**
- **NSFW** : Contenu adulte, violent, choquant
- **Harcèlement** : Contenu offensant, discriminatoire
- **Contenu illégal** : Piratage, activités illicites

### 💸 **Publicités non autorisées**
- **Liens d'affiliation** non déclarés
- **Vente forcée** : Produits non liés au gaming
- **Phishing** : Liens malveillants, arnaques

## 🔧 Configuration technique

### Paramètres par défaut
- **Canal réseaux** : À configurer par l'administrateur
- **Rôle actif** : À configurer par l'administrateur
- **Nettoyage automatique** : Activé lors du setup

### Structure des données
```json
{
  "reseaux_channel": null,
  "actif_role": null
}
```

## 🎯 Exemples d'utilisation

### Scénario 1 : Membre actif partage sa chaîne
1. **A le rôle Actif** grâce à sa participation
2. **Poste sa chaîne Twitch** avec description
3. **Communauté interagit** et découvre le contenu

### Scénario 2 : Nouveau membre veut partager
1. **N'a pas encore le rôle Actif**
2. **Contacte un modérateur** en privé
3. **Explique son projet** créatif
4. **Obtient une whitelist** temporaire
5. **Participe plus** pour obtenir le rôle Actif

### Scénario 3 : Créateur partage son art
1. **Artiste avec rôle Actif**
2. **Partage ses fanarts Valorant**
3. **Reçoit feedback** de la communauté
4. **Crée des œuvres personnalisées** pour les membres

## 🔒 Permissions requises

### Bot
- `Send Messages` - Envoyer le message informatif
- `Embed Links` - Afficher les embeds
- `Manage Messages` - Purger le canal lors du setup

### Utilisateurs
- **Membres** : Rôle Actif OU whitelist pour poster
- **Administrateurs** : Permission `manage_guild` pour les commandes admin
- **Modérateurs** : Peuvent accorder des whitelists

## 🎨 Emojis utilisés

Le système utilise les emojis personnalisés de Radiant Order :
- `<a:speechbubble:1380892653847314534>` - Communication, réseaux
- `<a:check_ravena:1380884332708626493>` - Conditions acceptées
- `<a:uncheck_ravena:1380884331534483629>` - Contenus interdits
- `<a:Warning:1380884984595742790>` - Avertissements
- `<a:whitecrown:1380899677297315880>` - Administration, whitelist
- `<a:FallingPetals:1380882470060425267>` - Bienvenue, créativité
- `<a:boost:1380882468621520916>` - Qualité, amélioration
- `<a:Lightblueheartgif:1380882450439471165>` - Communauté
- `<a:PinkLoading:1380886781062414356>` - Éviter le spam
- `<a:Animated_Arrow_Blue:1380888378953961472>` - Instructions
- `<a:agooglebell:1380895257541083300>` - Types de contenu

## 🐛 Dépannage

### Problèmes courants

**Le message ne s'affiche pas**
- Vérifier que le canal est configuré : `!vosreseaux channel #canal`
- Vérifier les permissions du bot
- Relancer `!vosreseaux setup`

**Le rôle n'apparaît pas**
- Configurer le rôle : `!vosreseaux role @RoleActif`
- Vérifier que le rôle existe
- Relancer le setup pour actualiser

**Impossible de purger le canal**
- Vérifier les permissions `Manage Messages`
- Le setup continuera sans nettoyage si permissions manquantes

### Commandes de diagnostic
```bash
# Voir la configuration complète
!vosreseaux

# Tester le redéploiement
!vosreseaux setup

# Reconfigurer si nécessaire
!vosreseaux channel #nouveau-canal
!vosreseaux role @nouveau-role
```

## 📈 Avantages du système

### 🎯 **Pour la communauté**
- **Encourage l'activité** pour obtenir le rôle Actif
- **Découverte de talents** dans la communauté
- **Partage créatif** organisé et de qualité
- **Networking** entre créateurs

### 🛡️ **Pour les modérateurs**
- **Contrôle du spam** automatique
- **Qualité du contenu** maintenue
- **Charge de modération** réduite
- **Règles claires** pour tous

### 💡 **Pour les créateurs**
- **Visibilité** auprès de la communauté
- **Feedback constructif** des autres membres
- **Motivation** à rester actif
- **Opportunités** de collaboration

## 🚀 Évolutions possibles

### Fonctionnalités futures
- **Système de votes** pour les créations
- **Catégories** de contenu avec tags
- **Spotlight** mensuel des meilleurs contenus
- **Intégration** avec un système de points/reputation

### Améliorations techniques
- **Détection automatique** des types de liens
- **Notifications** pour nouveau contenu
- **Statistiques** d'engagement
- **Archive** des meilleures créations

## 📊 Métriques suggérées

Pour évaluer l'efficacité du système :
- **Nombre de posts** par semaine/mois
- **Engagement** (réactions, commentaires)
- **Nouvelles acquisitions** du rôle Actif
- **Diversité** des types de contenu partagés
- **Taux de respect** des règles

## 🎮 Impact sur la communauté

### 🌟 **Découverte de talents**
Le canal permet de révéler les créateurs de la communauté :
- **Streamers** en devenir
- **Artistes** talentueux
- **Développeurs** créatifs
- **Monteurs** vidéo

### 🤝 **Collaborations**
Facilite les collaborations entre membres :
- **Équipes** de création
- **Projets** communautaires
- **Événements** organisés
- **Soutien mutuel**

### 🏆 **Motivation**
Encourage l'activité et la créativité :
- **Objectif** d'obtenir le rôle Actif
- **Reconnaissance** par la communauté
- **Amélioration** continue
- **Fierté** d'appartenance

---

**Développé pour Radiant Order** 🎮
*Système Vos Réseaux v1.0 - Partager sa créativité en communauté* 
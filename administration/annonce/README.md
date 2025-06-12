# 🌟 Cog Annonce pour RedBot

## 📋 Description

Ce cog permet d'envoyer des **annonces élégantes** pour les réunions communautaires avec des **boutons interactifs** permettant aux membres d'indiquer leurs disponibilités de manière moderne et intuitive.

## ✨ Fonctionnalités

### 🎯 **Boutons Interactifs**
- **3 boutons** pour les jours de la semaine (Mercredi, Jeudi, Vendredi)
- **Toggle système** : cliquer à nouveau retire la disponibilité
- **Messages éphémères** : confirmations privées pour chaque utilisateur
- **Émojis animés** personnalisés pour une expérience visuelle riche

### 🎨 **Design Élégant**
- **Embeds Discord** avec mise en forme professionnelle
- **Émojis animés** personnalisés du serveur
- **Couleurs harmonieuses** et disposition claire
- **Version simple** sans embed disponible

### 🔒 **Sécurité**
- Commandes réservées aux **administrateurs**
- Gestion d'erreurs complète
- Suppression automatique des commandes pour garder les canaux propres

## 🚀 Installation

### 1. Placement du fichier
```bash
# Placer le fichier dans :
[RED_DATA_PATH]/cogs/administration/annonce/annonce.py
```

### 2. Chargement du cog
```
[p]load administration.annonce
```

## 📝 Commandes

### `[p]reunion [channel_id]`
**Envoie une annonce complète avec embed et boutons**

- **Paramètres** : `channel_id` (optionnel) - ID du canal où envoyer l'annonce
- **Permissions** : Administrateur requis
- **Usage** :
  ```
  [p]reunion                    # Dans le canal actuel
  [p]reunion 1380560638539071510 # Dans un canal spécifique
  ```

### `[p]reunion_simple [channel_id]`
**Version simplifiée sans embed mais avec boutons**

- **Paramètres** : `channel_id` (optionnel) - ID du canal où envoyer l'annonce
- **Permissions** : Administrateur requis
- **Usage** :
  ```
  [p]reunion_simple                    # Dans le canal actuel
  [p]reunion_simple 1380560638539071510 # Dans un canal spécifique
  ```

## 🎮 Utilisation des Boutons

### Pour les Membres
1. **Cliquer** sur le bouton du jour souhaité
2. **Confirmation** privée de l'ajout de disponibilité
3. **Re-cliquer** pour retirer la disponibilité
4. **Messages éphémères** : seul l'utilisateur voit les confirmations

### Boutons Disponibles
- 🟢 **Mercredi** (Style : Success)
- 🔵 **Jeudi** (Style : Primary)  
- ⚫ **Vendredi** (Style : Secondary)

## 🎨 Émojis Utilisés

### Émojis Animés Personnalisés
```html
<a:Anouncements_Animated:1380895055694528542>    # Titre principal
<a:agooglebell:1380895257541083300>              # Salutations
<a:speechbubble:1380892653847314534>             # Objet réunion
<a:Animated_Arrow_Blue:1380888378953961472>      # Disponibilités
<a:check_ravena:1380884332708626493>             # Validation
<a:uncheck_ravena:1380884331534483629>           # Suppression
<a:whitecrown:1380899677297315880>               # Participation
<a:Lightblueheartgif:1380882450439471165>        # Cœur bleu
<a:Lightpinkgothheartgif:1380882449126527037>    # Cœur rose
<a:Whitegothheartgif:1380882447507390474>        # Cœur blanc
```

## 🔧 Configuration Technique

### Dépendances
- **RedBot** 3.5+
- **discord.py** 2.0+
- **Python** 3.8+

### Permissions Bot Requises
- `Send Messages`
- `Use Slash Commands`
- `Embed Links`
- `Add Reactions`
- `Use External Emojis`

## 📊 Fonctionnalités Avancées

### Système de Stockage
- **Stockage temporaire** des réponses en mémoire
- **Persistance** pendant la session du bot
- **Reset automatique** au redémarrage

### Gestion d'Erreurs
- **Canal introuvable** : message d'erreur explicite
- **Permissions insuffisantes** : gestion automatique
- **Émojis manquants** : dégradation gracieuse

## 🛠️ Personnalisation

### Modifier les Jours
Pour changer les jours de disponibilité, modifier dans `DisponibiliteView` :
```python
# Changer les labels et custom_id des boutons
@discord.ui.button(label="Lundi", custom_id="lundi")
```

### Changer les Couleurs
```python
# Dans la création de l'embed
color=0x7289DA  # Code couleur hexadécimal
```

### Modifier les Émojis
Remplacer les IDs des émojis par ceux de votre serveur :
```python
emoji="<a:votre_emoji:ID_EMOJI>"
```

## 🐛 Dépannage

### Boutons non fonctionnels
1. Vérifier que le bot a les permissions `Use Slash Commands`
2. S'assurer que `discord.py` est à jour
3. Redémarrer le bot si nécessaire

### Émojis non affichés
1. Vérifier que les émojis existent sur le serveur
2. Contrôler les IDs des émojis personnalisés
3. S'assurer que le bot peut utiliser les émojis externes

### Messages d'erreur
- **"Canal introuvable"** : Vérifier l'ID du canal
- **"Permissions insuffisantes"** : Donner les droits administrateur
- **"Erreur lors de l'envoi"** : Vérifier les permissions du bot

## 📋 Changelog

### Version 1.0
- ✅ Implémentation des boutons interactifs
- ✅ Système de toggle pour les disponibilités
- ✅ Messages éphémères pour les confirmations
- ✅ Intégration des émojis animés personnalisés
- ✅ Deux versions : complète et simplifiée
- ✅ Gestion d'erreurs robuste

## 👥 Support

Pour toute question ou problème :
1. Vérifier ce README
2. Consulter les logs du bot
3. Tester avec les permissions administrateur

---
*Créé avec 💝 pour une communauté active et engagée !* 
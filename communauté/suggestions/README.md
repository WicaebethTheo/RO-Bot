# 🎯 Système de Suggestions - Radiant Order

## 📋 Description

Le système de suggestions permet aux membres de Radiant Order de proposer des améliorations pour le serveur de manière organisée et interactive. Les suggestions peuvent être votées par la communauté et examinées par l'équipe de modération.

## ✨ Fonctionnalités

### 🎮 **Interface Utilisateur**
- **Bouton interactif** : Clic simple pour soumettre une suggestion
- **Modal détaillé** : Formulaire avec titre, description et justification
- **Design cohérent** : Utilise les emojis personnalisés de Radiant Order

### 🗳️ **Système de Vote**
- **Vote positif/négatif** : Boutons avec compteurs en temps réel
- **Anti-spam** : Un vote par utilisateur, changement possible
- **Persistance** : Les votes fonctionnent après redémarrage du bot

### 🛡️ **Modération**
- **Approbation/Rejet** : Gestion par l'équipe staff
- **Raisons détaillées** : Possibilité d'expliquer les décisions
- **Statistiques** : Vue d'ensemble des suggestions par statut

## 🚀 Installation

### 1. Configuration initiale
```bash
# Charger le cog
!load suggestions

# Configurer le message principal (optionnel - canal déjà configuré)
!suggestions channel #suggestions

# Déployer l'interface
!suggestions setup
```

### 2. Vérification
```bash
# Voir la configuration actuelle
!suggestions
```

## 📝 Utilisation

### 👥 **Pour les membres**

1. **Soumettre une suggestion**
   - Aller dans le canal #suggestions
   - Cliquer sur le bouton `🌟 Soumettre une suggestion`
   - Remplir le formulaire modal :
     - **Titre** : Résumé court de l'idée (5-100 caractères)
     - **Description** : Explication détaillée (20-1000 caractères)
     - **Justification** : Pourquoi cette suggestion ? (10-500 caractères)

2. **Voter sur les suggestions**
   - Cliquer sur ✅ pour voter positivement
   - Cliquer sur ❌ pour voter négativement
   - Changer d'avis en cliquant sur l'autre bouton

### 🛡️ **Pour les modérateurs**

#### Commandes de base
```bash
# Voir toutes les suggestions
!suggestions list

# Voir par statut
!suggestions list pending     # En attente
!suggestions list approved    # Approuvées
!suggestions list rejected    # Rejetées
```

#### Gestion des suggestions
```bash
# Approuver une suggestion
!suggestions approve 1
!suggestions approve 1 Super idée, on va l'implémenter !

# Rejeter une suggestion
!suggestions reject 2
!suggestions reject 2 Pas compatible avec notre vision du serveur
```

#### Configuration
```bash
# Changer le canal de suggestions
!suggestions channel #nouveau-canal

# Reconfigurer l'interface
!suggestions setup
```

## 🎨 Interface Visuelle

### 📤 **Message de soumission**
```
🌟 Suggestions Radiant Order

Aide-nous à améliorer le serveur !

💬 Tu as une idée pour améliorer Radiant Order ?
⚡ Une suggestion de nouveau mode de jeu ?
➡️ Une amélioration pour la communauté ?

Clique sur le bouton ci-dessous pour soumettre ta suggestion !

👑 Règles pour les suggestions :
• Sois respectueux et constructif
• Explique clairement ton idée
• Justifie pourquoi ce serait bénéfique
• Une suggestion = un clic sur le bouton

🔔 Les membres peuvent voter pour tes suggestions !
⏳ L'équipe examinera chaque suggestion.

[🌟 Soumettre une suggestion]
```

### 📊 **Suggestion affichée**
```
🌟 Suggestion #1

Nouveau mode Spike Rush personnalisé

💬 Description
Ajouter un mode Spike Rush avec des capacités custom...

➡️ Justification
Cela rendrait les parties plus dynamiques et amusantes...

👑 Auteur
@Utilisateur

💬 Statut
⏳ En attente

[✅ 5] [❌ 1]
```

## 📊 Données stockées

Pour chaque suggestion, le système sauvegarde :
- **ID unique** : Numérotation automatique
- **Contenu** : Titre, description, justification
- **Auteur** : ID Discord de l'utilisateur
- **Votes** : Listes des upvotes/downvotes
- **Statut** : pending/approved/rejected
- **Modération** : Qui a examiné, quand, pourquoi
- **Timestamps** : Création et révision

## 🔧 Configuration technique

### Paramètres par défaut
- **Canal suggestions** : `1380560571874934896`
- **ID suivant** : Auto-incrémenté à partir de 1
- **Timeout boutons** : Aucun (persistants)

### Structure des données
```json
{
  "suggestions_channel": 1380560571874934896,
  "next_suggestion_id": 1,
  "suggestions_data": {
    "1": {
      "title": "Titre de la suggestion",
      "description": "Description détaillée",
      "reason": "Justification",
      "author_id": 123456789,
      "message_id": 987654321,
      "status": "pending",
      "upvotes": [user_id1, user_id2],
      "downvotes": [user_id3],
      "created_at": "2024-01-01T12:00:00",
      "reviewed_by": 456789123,
      "review_reason": "Raison de la décision",
      "reviewed_at": "2024-01-02T12:00:00"
    }
  }
}
```

## 🎯 Exemples d'utilisation

### Scénario 1 : Nouvelle suggestion
1. Membre clique sur le bouton
2. Remplit : "Tournoi mensuel" / "Organiser un tournoi..." / "Ça motiverait la communauté"
3. Suggestion #5 créée
4. Autres membres votent
5. Staff approuve avec raison

### Scénario 2 : Modération
```bash
# Staff voit les suggestions en attente
!suggestions list pending

# Examine la suggestion #3
# Décide de l'approuver
!suggestions approve 3 Excellente idée, on planifie ça !

# La suggestion est mise à jour automatiquement
```

## 🔒 Permissions requises

### Bot
- `Send Messages` - Envoyer des suggestions
- `Embed Links` - Afficher les embeds
- `Add Reactions` - Boutons (automatique avec UI)
- `Manage Messages` - Éditer les suggestions (statut)

### Utilisateurs
- **Membres** : Accès lecture au canal suggestions
- **Modérateurs** : Permission `manage_guild` pour les commandes admin

## 🎨 Emojis utilisés

Le système utilise les emojis personnalisés de Radiant Order :
- `<a:FallingPetals:1380882470060425267>` - Suggestions générales
- `<a:check_ravena:1380884332708626493>` - Succès/Approbation
- `<a:uncheck_ravena:1380884331534483629>` - Erreur/Rejet
- `<a:speechbubble:1380892653847314534>` - Communication
- `<a:boost:1380882468621520916>` - Améliorations
- `<a:Animated_Arrow_Blue:1380888378953961472>` - Actions
- `<a:whitecrown:1380899677297315880>` - Staff/Administration
- `<a:PinkLoading:1380886781062414356>` - En attente
- `<a:Warning:1380884984595742790>` - Avertissements
- `<a:agooglebell:1380895257541083300>` - Notifications

## 🐛 Dépannage

### Problèmes courants

**Le bouton ne fonctionne pas**
- Vérifier que le bot a les permissions
- Relancer `!suggestions setup`

**Les votes ne s'enregistrent pas**
- Redémarrer le bot pour recharger les vues
- Vérifier les permissions du bot

**Suggestions non affichées**
- Vérifier l'ID du canal dans la config
- S'assurer que le bot voit le canal

### Commandes de diagnostic
```bash
# Voir la configuration
!suggestions

# Tester les permissions
!suggestions setup

# Vérifier les données
!suggestions list all
```

## 📈 Statistiques

Le système suit automatiquement :
- Nombre total de suggestions
- Répartition par statut (en attente/approuvées/rejetées)
- Activité de vote
- Historique de modération

Accessible via `!suggestions` sans paramètres.

---

**Développé pour Radiant Order** 🎮
*Système de suggestions v1.0 - Cohérent avec l'identité visuelle du serveur* 
# 📢 Système de Demande d'Assistance - Radiant Order

## 📋 Description
Système de demande d'assistance pour l'organisation de parties et événements. Permet aux joueurs dans les salons de préparation de contacter directement les helpers en ligne.

## ⚙️ Fonctionnalités

### 🎤 Restriction aux salons de préparation
Les utilisateurs doivent être connectés dans un salon vocal de préparation :
- **🎤 〔🎮〕Préparation 1** (ID: 1380560625654304829)
- **🎤 〔🎮〕Préparation 2** (ID: 1380615433303883999) 
- **🎤 〔🎮〕Préparation 3** (ID: 1380615512161255425)
- **🎤 〔🎮〕Préparation 4** (ID: 1380617021359915190)

### 👥 Ping automatique des helpers
- Détection automatique des helpers en ligne (rôle ID: 1380564333242613821)
- Ping uniquement des membres avec statut actif (non offline)
- Affichage du nombre de helpers disponibles
- Identification du salon vocal du demandeur

### 🔐 Système de privilèges
#### 👑 **Rôles privilégiés** (utilisation illimitée)
- **Administrateur** (ID: 1380562058461839400)
- **Responsables** (ID: 1380562966575059116)
- **Assistants Responsable** (ID: 1380575934410915911)
- **Modérateurs** (ID: 1380563626846322819)
- **Helper** (ID: 1380564333242613821)

#### 👤 **Utilisateurs standards**
- Limitation de 10 minutes entre chaque utilisation (note informatif)
- Accès aux mêmes fonctionnalités

### 📊 Informations détaillées
- **Demandeur** : Nom et mention du membre
- **Salon vocal** : Nom du salon de préparation
- **Helpers disponibles** : Nombre et mentions
- **Timestamp** : Heure précise de la demande
- **Statut** : Indication du niveau de privilège

## 🎯 Commandes d'administration

### `!setup_demande`
Configure le système de demande d'assistance.
- **Permissions requises** : `manage_guild`
- **Fonctionnalités** :
  - Nettoie automatiquement le canal
  - Installe le message avec bouton persistant
  - Configure l'interface utilisateur complète

## ⚙️ Configuration

### 📺 Canal de demande
- Canal ID: `1380560617676603402`

### 🏷️ Rôle Helper ciblé
- Helper ID: `1380564333242613821`

### 🎤 Salons autorisés
```
Préparation 1: 1380560625654304829
Préparation 2: 1380615433303883999
Préparation 3: 1380615512161255425
Préparation 4: 1380617021359915190
```

### 👑 Rôles privilégiés
```
Administrateur: 1380562058461839400
Responsables: 1380562966575059116
Assistants Responsable: 1380575934410915911
Modérateurs: 1380563626846322819
Helper: 1380564333242613821
```

## 🔄 Flux de fonctionnement

1. **Connexion** : L'utilisateur se connecte dans un salon de préparation
2. **Demande** : Clic sur le bouton "📢 Appeler les helpers"
3. **Vérification** : Le système vérifie la présence dans un salon autorisé
4. **Détection** : Identification des helpers en ligne
5. **Notification** : Ping des helpers avec embed détaillé
6. **Confirmation** : Message de confirmation pour le demandeur

## 🎨 Interface utilisateur

### 📢 Bouton principal
- **Label** : "📢 Appeler les helpers"
- **Style** : Bouton bleu (primary)
- **Persistant** : Fonctionne après redémarrage du bot

### 📊 Embed de demande
- **Titre** : "🔔 Assistance Helpers"
- **Couleur** : Bleu (#00B0F4)
- **Informations** :
  - Nom du demandeur
  - Salon vocal actuel
  - Nombre de helpers en ligne
  - Statut de limitation/privilège

### ✅ Messages de confirmation
- **Succès** : Confirmation verte avec détails
- **Erreur** : Messages rouges explicatifs
- **Pas de helpers** : Notification orange

## 🛡️ Sécurités intégrées

### 🔍 Vérifications automatiques
- **Présence vocale** : Vérification de connexion dans un salon
- **Salon autorisé** : Validation de l'ID du salon
- **Rôle Helper** : Vérification de l'existence du rôle
- **Statut en ligne** : Filtrage des helpers hors ligne

### 🚫 Gestion des erreurs
- **Salon incorrect** : Message d'erreur avec liste des salons autorisés
- **Rôle manquant** : Notification d'erreur système
- **Aucun helper** : Information sur l'indisponibilité

## 📁 Fichiers
- `demandeorga.py` : Code principal du système
- Vues persistantes automatiques

## 🚀 Installation
1. Charger le cog : `!load partieperso.demandeorga.demandeorga`
2. Installer l'interface : `!setup_demande`
3. Le système est automatiquement configuré

## 📊 Avantages du système

### 🎯 **Pour les joueurs**
- **Accès direct** aux helpers depuis les salons de préparation
- **Réponse rapide** pour l'organisation de parties
- **Interface simple** et intuitive
- **Pas de commandes complexes** à retenir

### 👥 **Pour les helpers**
- **Notifications ciblées** uniquement quand nécessaire
- **Informations contextuelles** complètes
- **Identification rapide** du demandeur et du salon
- **Filtrage automatique** des demandes inappropriées

### 🔧 **Pour les administrateurs**
- **Configuration simple** avec une seule commande
- **Sécurité intégrée** avec vérifications automatiques
- **Logs automatiques** des demandes
- **Gestion des privilèges** flexible

## ⚠️ Important
- Seuls les utilisateurs dans les salons de préparation peuvent utiliser le système
- Les helpers sont pingués uniquement s'ils sont en ligne
- Les rôles staff n'ont aucune limitation d'utilisation
- Le système est persistent et survit aux redémarrages
- Messages d'erreur clairs pour guider les utilisateurs

## 💡 Conseils d'utilisation

### 📚 **Pour les joueurs**
- Connectez-vous dans un salon de préparation avant de demander de l'aide
- Soyez précis dans vos demandes d'assistance
- Respectez le travail des helpers

### 👮 **Pour les helpers**
- Répondez rapidement aux demandes d'assistance
- Rejoignez le salon vocal du demandeur
- Aidez à organiser les parties efficacement

### ⚙️ **Pour les modérateurs**
- Surveillez les abus potentiels du système
- Vérifiez régulièrement que les helpers sont disponibles
- Adaptez les salons autorisés selon les besoins

---

**📢 Développé pour Radiant Order - Organisation et Assistance Communautaire** 
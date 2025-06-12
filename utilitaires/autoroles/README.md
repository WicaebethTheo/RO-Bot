# 🎮 Système d'Auto-Rôles Valorant - Radiant Order

## 📋 Description
Système d'auto-attribution de rôles pour les rangs Valorant avec boutons interactifs et emojis personnalisés du serveur.

## ⚙️ Fonctionnalités

### 🏆 Rangs Valorant disponibles
- **Unrated** - Pas encore classé
- **Iron** - Fer (débutant) 
- **Bronze** - Bronze
- **Silver** - Argent (avec emoji personnalisé <:silver:1380633512495022222>)
- **Gold** - Or (avec emoji personnalisé <:gold:1380617981620518912>)
- **Platinum** - Platine
- **Diamond** - Diamant (avec emoji personnalisé <:diams:1380617948313555034>)
- **Ascendant** - Ascendant (avec emoji personnalisé <:ascendant:1380617956299509886>)
- **Immortal** - Immortel (avec emoji personnalisé <:immortal:1380617977803837531>)
- **Radiant** - Radiant (avec emoji personnalisé <:radiant:1380617911932030977>)

### 🔄 Système exclusif
- Un seul rang à la fois par utilisateur
- Changement automatique de rang (retire l'ancien)
- Interface intuitive avec boutons persistants

### 🎨 Interface utilisateur
- Messages séparés pour rangs débutants et avancés
- Boutons colorés selon le niveau de difficulté
- Emojis personnalisés pour les rangs élevés
- Design moderne et attrayant

## 🎯 Commandes d'administration

### `!autoroles setup`
Configure les messages d'auto-rôles dans le canal défini.
- Nettoie automatiquement le canal
- Envoie les nouveaux messages avec boutons
- Interface utilisateur complète

### `!autoroles setrole rank <nom_rang> @role`
Configure un rôle spécifique pour un rang.
```
!autoroles setrole rank Silver @Argent
```

### `!autoroles channel #canal`
Définit le canal où seront envoyés les messages d'auto-rôles.

### `!autoroles config`
Affiche la configuration actuelle du système.

### `!autoroles stats`
Affiche les statistiques de répartition des rangs.

## ⚙️ Configuration

### 📺 Canal par défaut
- Canal ID: `1380560529810002073`

### 🏷️ IDs des rôles configurés
```
Iron: 1380572318602104932
Bronze: 1380572089295044749  
Silver: 1380571873435320350
Gold: 1380571721672953856
Platinum: 1380571586326822923
Diamond: 1380571473873473666
Ascendant: 1380571196386443366
Immortal: 1380570565995266069
Radiant: 1380570718231724112
```

### 🎨 Emojis personnalisés
```
Silver: <:silver:1380633512495022222>
Gold: <:gold:1380617981620518912>
Diamond: <:diams:1380617948313555034>
Ascendant: <:ascendant:1380617956299509886>
Immortal: <:immortal:1380617977803837531>
Radiant: <:radiant:1380617911932030977>
```

## 🔐 Permissions requises
- `manage_roles` pour les commandes d'administration
- Aucune permission spéciale pour les utilisateurs

## 📁 Fichiers
- `autoroles.py` : Code principal du système
- Vues persistantes automatiques

## 🚀 Installation
1. Charger le cog : `!load utilitaires.autoroles.autoroles`
2. Configurer le canal : `!autoroles channel #canal`
3. Installer l'interface : `!autoroles setup`

## ⚠️ Important
- Les boutons sont persistants (fonctionnent après redémarrage)
- Système exclusif pour les rangs (un seul à la fois)
- Configuration automatique des IDs de rôles
- Emojis personnalisés pour une meilleure UX

## 🎯 Commandes

### Commandes Administrateur

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!autoroles setup` | Déploie les messages d'auto-rôles | `!autoroles setup` |
| `!autoroles setrole <type> <nom> <@role>` | Configure un rôle | `!autoroles setrole rank Gold @Gold` |
| `!autoroles channel <#channel>` | Définit le channel | `!autoroles channel #auto-roles` |
| `!autoroles config` | Affiche la configuration | `!autoroles config` |
| `!autoroles stats` | Statistiques des rôles | `!autoroles stats` |

### Types de rôles
- **rank** : Rangs Valorant (exclusifs)
- **pp** : Rôles parties personnalisées

## 🔧 Fonctionnement Technique

### Structure des Vues
```python
# Rangs débutants (Unrated → Gold)
ValorantRanksView()

# Rangs avancés (Platinum → Radiant) 
ValorantRanksView2()

# Règles PP
PPRulesView()
```

### Gestion des Rôles
- **Rangs exclusifs** : Retrait automatique des autres rangs
- **PP cumulatifs** : Possibilité d'avoir plusieurs rôles PP
- **Permissions sécurisées** : Vérification des permissions avant action

### Configuration JSON
```json
{
  "autoroles_channel": 1380560529810002073,
  "rank_roles": {
    "Unrated": null,
    "Iron": null,
    // ... autres rangs
  },
  "pp_roles": {
    "PP Accepté": null,
    "Joueur PP": null
  }
}
```

## 📊 Interface Utilisateur

### Messages Déployés

1. **Message d'introduction**
   - Explication du système
   - Logo Valorant
   - Instructions d'utilisation

2. **Rangs débutants** (Bronze)
   - Unrated, Iron, Bronze, Silver, Gold
   - Boutons secondaires avec emojis

3. **Rangs avancés** (Turquoise)
   - Platinum, Diamond, Ascendant, Immortal, Radiant
   - Boutons primaires et danger

4. **Règles PP** (Vert)
   - Règles détaillées
   - Boutons d'acceptation et d'accès

### Confirmations Utilisateur
- **Ajout de rang** : Message personnalisé avec thumbnail
- **Retrait de rôle** : Confirmation orange
- **Erreurs** : Messages explicatifs pour résoudre les problèmes

## 🛠️ Résolution de Problèmes

### Boutons qui ne répondent pas
- Vérifiez que le bot a les permissions `Manage Roles`
- Redémarrez le bot pour recharger les vues persistantes
- Vérifiez la hiérarchie des rôles

### Rôles non configurés
```
!autoroles config
```
Configurez les rôles manquants avec `!autoroles setrole`

### Permissions insuffisantes
- Le bot doit avoir un rôle supérieur aux rôles qu'il gère
- Permission `Manage Roles` obligatoire
- Accès en écriture au channel configuré

## 📈 Bonnes Pratiques

### Hiérarchie des Rôles
1. Placez le rôle du bot au-dessus des rôles à gérer
2. Organisez les rangs par ordre croissant
3. Séparez les rôles PP des rangs

### Gestion Communautaire
- Expliquez le système aux nouveaux membres
- Créez des channels spécifiques aux différents rangs
- Utilisez les statistiques pour adapter le contenu

### Sécurité
- Limitez les permissions du rôle bot
- Surveillez les logs d'attribution de rôles
- Vérifiez régulièrement la configuration

## 🎮 Intégration Spike Rush

Ce système est spécialement optimisé pour les serveurs **Spike Rush** avec :
- **Thème Valorant** complet
- **Règles PP intégrées** pour les events
- **Interface gaming** moderne
- **Feedback personnalisé** pour l'immersion

## 📝 Notes de Version

### v1.0.0
- ✅ Système complet d'auto-rôles
- ✅ 10 rangs Valorant officiels
- ✅ Règles PP intégrées
- ✅ Boutons persistants
- ✅ Interface moderne
- ✅ Statistiques avancées

---

*Développé pour Spike Rush - Système d'auto-rôles Gaming* 🎮 
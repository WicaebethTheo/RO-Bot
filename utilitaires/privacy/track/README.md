# 📊 Track - Générateur de Channels de Tracking Discord

## 📋 Description
Système automatique de création et configuration de channels de tracking pour surveiller l'activité d'un serveur Discord. Génère une catégorie complète avec 10 channels spécialisés et configure automatiquement les permissions.

## ✨ Fonctionnalités

### 🎯 **Création Automatique**
- Génération automatique d'une catégorie "📊 Track"
- 10 channels de tracking spécialisés créés automatiquement
- Configuration automatique des permissions
- Sauvegarde des IDs générés

### 📺 **Channels Créés**
1. **📬 track-messages** - Messages texte généraux
2. **🖼️ track-images** - Images et fichiers partagés
3. **🗑️ track-deletes** - Messages supprimés
4. **🎤 track-voice** - Activité vocale
5. **📥 track-joins** - Arrivées de membres
6. **✏️ track-edits** - Messages modifiés
7. **📤 track-leaves** - Départs de membres
8. **🏷️ track-roles** - Modifications de rôles
9. **🔨 track-bans** - Bannissements et débans
10. **😀 track-reactions** - Réactions ajoutées/supprimées

### 🔐 **Gestion des Permissions**
- Permissions administrateur configurées automatiquement
- Accès restreint aux rôles autorisés
- Protection contre l'accès public

## 🚀 Installation & Utilisation

```bash
# Charger le cog
!load utilitaires.privacy.track

# Créer les channels de tracking
!track setup

# Voir la configuration
!track status
```

## 🎮 Commandes

### **Commandes Admin** (Permissions requises)
- `!track setup` - Créer tous les channels de tracking
- `!track status` - Voir la configuration actuelle
- `!track config` - Afficher les IDs générés

### **Exemple d'utilisation**
```bash
# Créer le système complet
!track setup

# Vérifier que tout fonctionne
!track status
```

## 🎯 Configuration Cible

**Serveur surveillé :** `1380564195631693915`

### **IDs des Channels Générés**
```
📬 messages:   1380568606668099714
🖼️ images:     1380568610409283618
🗑️ deletes:    1380568614511575120
🎤 voice:      1380568617464102923
📥 joins:      1380568620995707051
✏️ edits:      1380568624418390207
📤 leaves:     1380568627673043124
🏷️ roles:      1380568631121023091
🔨 bans:       1380568634979516576
😀 reactions:  1380568638251208918
```

## 🔧 Fonctionnement Technique

### **Processus de création :**
1. **Vérification** : Contrôle des permissions du bot
2. **Catégorie** : Création de la catégorie "📊 Track"
3. **Channels** : Génération des 10 channels spécialisés
4. **Permissions** : Configuration des droits d'accès
5. **Sauvegarde** : Enregistrement des IDs dans la config

### **Structure des permissions :**
```python
overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
}

# Ajout automatique des rôles admin
for role in guild.roles:
    if role.permissions.administrator:
        overwrites[role] = discord.PermissionOverwrite(read_messages=True)
```

## 📊 Utilisation avec d'Autres Cogs

Ce cog est conçu pour être utilisé avec le cog **Tracking** qui enverra automatiquement les logs dans ces channels :

```bash
# Charger aussi le système de surveillance
!load utilitaires.privacy.tracking
```

## 🎨 Aperçu de la Création

```
✅ Création de la catégorie Track
✅ Génération des channels de logging

📊 Track (Catégorie)
├── 📬 track-messages
├── 🖼️ track-images  
├── 🗑️ track-deletes
├── 🎤 track-voice
├── 📥 track-joins
├── ✏️ track-edits
├── 📤 track-leaves
├── 🏷️ track-roles
├── 🔨 track-bans
└── 😀 track-reactions

🔧 Permissions configurées
💾 IDs sauvegardés en configuration
```

## 🔒 Permissions Requises

**Bot :**
- `Manage Channels` - Créer et gérer les channels
- `Manage Permissions` - Configurer les permissions
- `View Channel` - Voir les channels
- `Send Messages` - Envoyer des messages

**Admin :**
- `Administrator` - Droits administrateur complets
- `Manage Guild` - Gérer le serveur

## 🔧 Configuration Avancée

### **Personnaliser les noms de channels**
Modifiez la liste `TRACK_CHANNELS` dans le code :

```python
TRACK_CHANNELS = [
    ("📬", "track-messages", "Messages texte"),
    ("🖼️", "track-images", "Images et fichiers"),
    # ... autres channels
]
```

### **Modifier les permissions**
Ajustez la fonction `create_track_overwrites()` pour personnaliser les droits d'accès.

### **Changer la catégorie**
Modifiez `CATEGORY_NAME = "📊 Track"` pour un autre nom.

## 🐛 Résolution de Problèmes

### Erreur de permissions
1. Vérifier que le bot a les droits `Manage Channels`
2. S'assurer d'être administrateur
3. Contrôler les permissions dans le serveur

### Channels non créés
1. Vérifier l'espace disponible (limite Discord)
2. Contrôler les noms de channels (pas de doublons)
3. Tester dans un autre serveur

### Configuration non sauvegardée
1. Vérifier les permissions d'écriture du bot
2. Redémarrer le bot si nécessaire
3. Recharger le cog : `!reload utilitaires.privacy.track`

## 📝 Maintenance

### **Nettoyage**
Pour supprimer tous les channels créés :
```bash
# Attention : supprime définitivement tous les channels track
!track cleanup
```

### **Recréation**
Si des channels sont supprimés manuellement :
```bash
# Recréer uniquement les channels manquants
!track repair
```

### **Sauvegarde**
Les IDs sont automatiquement sauvegardés. Pour une sauvegarde manuelle :
```bash
!track backup
```

## 🔄 Mises à Jour

### Version 1.0.0 (Actuelle)
- ✅ Création automatique de 10 channels
- ✅ Configuration des permissions
- ✅ Sauvegarde des IDs
- ✅ Commandes de gestion

### Améliorations futures
- 🔮 Customisation des noms de channels
- 🔮 Templates de permissions avancés
- 🔮 Interface de gestion web
- 🔮 Statistiques d'utilisation

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez les permissions du bot
2. Consultez `!track status`
3. Testez dans un serveur de développement
4. Contactez un développeur

## ⚠️ Avertissements

1. **Limite Discord** : Maximum 500 channels par serveur
2. **Permissions** : Droits administrateur requis
3. **Suppression** : Les channels supprimés manuellement ne sont pas récupérables
4. **Serveur cible** : Configuré pour un serveur spécifique (1380564195631693915)

## 🎯 Bonnes Pratiques

1. **Test préalable** dans un serveur de développement
2. **Sauvegarde** des configurations importantes
3. **Permissions minimales** pour les utilisateurs
4. **Surveillance** de l'espace disque des logs
5. **Nettoyage régulier** des anciens logs 
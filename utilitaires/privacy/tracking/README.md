# 📊 Tracking - Système de Surveillance Automatique Discord

## 📋 Description
Système de surveillance automatique en temps réel pour Discord qui capture et route intelligemment tous les événements d'un serveur vers des channels de logging spécialisés avec embeds détaillés.

## ✨ Fonctionnalités

### 🎯 **Surveillance Complète**
- Surveillance en temps réel de tous les événements Discord
- Routage intelligent vers les channels appropriés
- Embeds détaillés avec informations contextuelles
- Séparation automatique images/messages texte

### 📊 **Événements Surveillés**
1. **💬 Messages** - Messages texte avec contenu
2. **🖼️ Images** - Fichiers et images partagés
3. **🗑️ Suppressions** - Messages supprimés avec contenu
4. **✏️ Modifications** - Messages édités (avant/après)
5. **📥 Arrivées** - Nouveaux membres avec alertes sécurité
6. **📤 Départs** - Membres quittant avec historique
7. **🎤 Vocal** - Connexions/déconnexions/changements
8. **🏷️ Rôles** - Modifications de rôles des membres
9. **🔨 Bans** - Bannissements et débannissements
10. **😀 Réactions** - Réactions ajoutées/supprimées

### 🔐 **Sécurité & Alertes**
- Détection des comptes récents (< 7 jours)
- Alertes automatiques pour activités suspectes
- Logs détaillés avec timestamps précis
- Protection contre le spam de logs

## 🚀 Installation & Configuration

```bash
# Charger le cog
!load utilitaires.privacy.tracking

# Vérifier le statut
!tracking status

# Activer/désactiver
!tracking toggle
```

## 🎯 Configuration par Défaut

**Serveur surveillé :** `1380282831347122267`

### **Channels de Destination**
```
💬 Messages:   1380568606668099714
🖼️ Images:     1380568610409283618
🗑️ Suppressions: 1380568614511575120
🎤 Vocal:      1380568617464102923
📥 Arrivées:   1380568620995707051
✏️ Éditions:   1380568624418390207
📤 Départs:    1380568627673043124
🏷️ Rôles:      1380568631121023091
🔨 Bans:       1380568634979516576
😀 Réactions:  1380568638251208918
```

## 🎮 Commandes

### **Commandes Admin** (Permissions requises)
- `!tracking status` - Voir le statut et la configuration
- `!tracking toggle` - Activer/Désactiver le système
- `!tracking config` - Configuration avancée

### **Exemples d'utilisation**
```bash
# Voir le statut complet
!tracking status

# Désactiver temporairement
!tracking toggle

# Réactiver le tracking
!tracking toggle
```

## 🔧 Fonctionnement Technique

### **Architecture du Système**
```python
# Surveillance en temps réel
@commands.Cog.listener()
async def on_[event](self, ...):
    if not self.is_target_guild(guild_id):
        return
    
    # Génération embed
    embed = create_detailed_embed(event_data)
    
    # Routage intelligent
    await self.send_to_channel("channel_key", embed)
```

### **Routage Intelligent**
- **Messages texte** → Channel messages
- **Images/fichiers** → Channel images
- **Modifications** → Channel edits (avec avant/après)
- **Événements vocaux** → Channel voice
- **Gestion membres** → Channels joins/leaves

### **Système d'Embeds**
Chaque événement génère un embed avec :
- Titre descriptif avec emoji
- Couleur thématique (vert=ajout, rouge=suppression, etc.)
- Informations détaillées dans des fields
- Avatar et mention de l'utilisateur
- Timestamp précis
- Liens directs quand possible

## 🎨 Exemples d'Embeds

### **💬 Message Texte**
```
💬 Message envoyé
👤 Auteur: @wica
📍 Salon: #général
🆔 Message ID: 1234567890
💬 Contenu: Salut tout le monde !
```

### **🖼️ Image Partagée**
```
🖼️ Image/Fichier envoyé
👤 Auteur: @wica
📍 Salon: #partage
📁 Fichiers:
📎 [screenshot.png](https://cdn.discord.com/...)
💬 Contenu: Regardez ça !
```

### **📥 Nouveau Membre**
```
📥 Nouveau membre
👤 Membre: @nouvel_user
🆔 ID: 123456789
📅 Compte créé: 25/12/2024 à 15:30
🎯 Membres totaux: 156
⚠️ Alerte: Compte récent (2 jours)
```

### **🎤 Événement Vocal**
```
🎤 Connexion vocale
👤 Membre: @wica
📍 Salon: Général
👥 Membres: 3
```

## 🔒 Permissions Requises

**Bot :**
- `View Channel` - Voir les channels
- `Send Messages` - Envoyer des logs
- `Embed Links` - Créer des embeds
- `Read Message History` - Accéder à l'historique

**Admin :**
- `Manage Guild` - Gérer le serveur
- `Administrator` - Droits administrateur

## 📊 Statistiques & Monitoring

### **Métriques Surveillées**
- Volume de messages par heure
- Activité vocale (connexions/déconnexions)
- Taux d'arrivée/départ de membres
- Fréquence des modifications de messages
- Activité de modération (bans, rôles)

### **Alertes Sécurité**
- Comptes récents (< 7 jours)
- Connexions massives
- Activité suspecte de suppression
- Modifications de rôles importantes

## 🔧 Configuration Avancée

### **Personnaliser les Couleurs**
```python
# Dans le code
discord.Color.green()   # Événements positifs
discord.Color.red()     # Suppressions/départs
discord.Color.orange()  # Modifications
discord.Color.blue()    # Informations générales
```

### **Filtrer les Événements**
Modifier les conditions dans chaque listener :
```python
# Ignorer les bots
if user.bot:
    return

# Filtrer par channel
if channel.id in IGNORED_CHANNELS:
    return
```

### **Ajuster les Embeds**
Personnaliser les champs et informations affichées dans `generate_embed_for_event()`.

## 🐛 Résolution de Problèmes

### Le tracking ne fonctionne pas
1. Vérifier que le cog est chargé : `!loaded`
2. Contrôler la configuration : `!tracking status`
3. Vérifier que le tracking est activé
4. Tester les permissions dans les channels de destination

### Messages non loggés
1. Vérifier l'ID du serveur surveillé
2. Contrôler les permissions du bot
3. Vérifier que les channels de destination existent
4. Tester avec `!tracking toggle` (off puis on)

### Embeds malformés
1. Vérifier les permissions `Embed Links`
2. Contrôler la validité des URLs d'avatars
3. Tester dans un channel différent

### Performance lente
1. Le système est optimisé pour la vitesse
2. Vérifier la charge du serveur
3. Considérer filtrer certains événements

## 📝 Maintenance

### **Surveillance des Logs**
- Les logs s'accumulent rapidement (plusieurs centaines par jour)
- Prévoir un nettoyage périodique des anciens messages
- Surveiller l'espace disque des attachments

### **Optimisation**
```bash
# Désactiver temporairement pour maintenance
!tracking toggle

# Réactiver après maintenance
!tracking toggle
```

### **Sauvegarde**
Les configurations sont automatiquement sauvegardées. Pour backup manuel :
```bash
!tracking backup
```

## 🔄 Mises à Jour

### Version 1.0.0 (Actuelle)
- ✅ Surveillance de 10 types d'événements
- ✅ Embeds détaillés et stylés
- ✅ Routage intelligent des messages
- ✅ Alertes de sécurité intégrées
- ✅ Configuration flexible

### Améliorations futures
- 🔮 Filtres avancés par utilisateur/channel
- 🔮 Statistiques graphiques
- 🔮 Alertes webhook externes
- 🔮 Archive automatique des logs
- 🔮 Interface web de monitoring

## ⚠️ Considérations Importantes

### **Volume de Données**
- Peut générer **plusieurs centaines de logs par jour**
- Prévoir l'espace de stockage nécessaire
- Considérer la rotation automatique des logs

### **Confidentialité**
- Les messages privés ne sont **jamais** loggés
- Seuls les événements des channels publics sont surveillés
- Respect total des permissions Discord

### **Performance**
- Impact minimal sur les performances du bot
- Traitement asynchrone des événements
- Gestion intelligente des erreurs

## 🤝 Support

Pour assistance technique :
1. Vérifier `!tracking status`
2. Consulter les logs du bot
3. Tester dans un serveur de développement
4. Contacter l'équipe de développement

## 🎯 Bonnes Pratiques

1. **Monitoring régulier** du statut du système
2. **Nettoyage périodique** des anciens logs
3. **Permissions minimales** pour l'accès aux logs
4. **Sauvegarde** des configurations importantes
5. **Test préalable** avant déploiement en production
6. **Documentation** des changements de configuration

---

*Système de surveillance professionnel pour une sécurité et transparence maximales ! 🔍* 
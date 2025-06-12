# 📜 Règlement - Système d'Affichage des Règles Spike Rush

## 📋 Description
Système d'affichage du règlement du serveur Spike Rush avec design gaming moderne, embeds stylés et navigation intuitive.

## ✨ Fonctionnalités

### 📖 **Affichage du Règlement**
- Règlement complet et modernisé pour Spike Rush
- Design gaming avec emojis et mise en forme soignée
- Sections organisées et faciles à lire
- Version simplifiée sans surcharge d'emojis

### 🎨 **Design & Styling**
- Couleurs rouge gaming (discord.Color.red())
- Emojis thématiques pour chaque section
- Footer personnalisé avec timestamp
- Mise en page claire et professionnelle

### ⚙️ **Configuration**
- Channel par défaut : `1380560525871550502`
- Commande principale : `!reglement`
- Commandes admin pour la gestion

## 🚀 Installation

```bash
# Charger le cog
!load accueil.regles

# Afficher le règlement (utilisateurs)
!reglement

# Envoyer dans le channel configuré (admin)
!reglement send
```

## 🎮 Commandes

### **Commandes Utilisateur**
- `!reglement` - Afficher le règlement dans le channel actuel
- `!rules` - Alias pour `!reglement`

### **Commandes Admin** (Permissions requises)
- `!reglement send` - Envoyer le règlement dans le channel configuré
- `!reglement channel <channel>` - Définir le channel par défaut
- `!reglement config` - Voir la configuration actuelle

### **Exemples d'utilisation**
```bash
# Afficher le règlement
!reglement

# Configurer le channel (admin)
!reglement channel #règles

# Envoyer automatiquement (admin)
!reglement send
```

## 📋 Contenu du Règlement

### **Structure du règlement :**

1. **🎯 Respect & Comportement**
   - Respect mutuel obligatoire
   - Pas de harcèlement ou toxicité
   - Language approprié

2. **💬 Communication**
   - Utilisation correcte des channels
   - Pas de spam ou flood
   - Sujets appropriés

3. **🎮 Gaming & Activités**
   - Fair-play en jeu
   - Respect des équipes
   - Pas de triche

4. **🔒 Sécurité & Vie Privée**
   - Pas de partage d'infos personnelles
   - Signalement des problèmes
   - Protection des mineurs

5. **⚖️ Sanctions**
   - Système d'avertissements
   - Sanctions graduelles
   - Procédure d'appel

## 🎯 Configuration par Défaut

```python
Channel: 1380560525871550502
Couleur: Rouge (#ff0000)
Titre: "📜 Règlement du Serveur Spike Rush"
Footer: "Spike Rush - Respect du règlement obligatoire"
```

## 🔧 Fonctionnement Technique

1. **Commande** : Utilisateur tape `!reglement`
2. **Vérification** : Contrôle des permissions si admin
3. **Génération** : Création de l'embed complet
4. **Envoi** : Message posté dans le channel approprié
5. **Logs** : Enregistrement de l'action

## 🎨 Aperçu du Message

```
📜 Règlement du Serveur Spike Rush

🎯 RESPECT & COMPORTEMENT
• Respect mutuel obligatoire
• Aucune tolérance pour le harcèlement
• Language approprié en toutes circonstances

💬 COMMUNICATION
• Utilisez les bons channels
• Pas de spam ni de flood
• Restez dans le sujet

🎮 GAMING
• Fair-play obligatoire
• Respect des coéquipiers
• Pas de triche tolérée

🔒 SÉCURITÉ
• Protection de vos infos personnelles
• Signalez tout problème au staff
• Sécurité des mineurs prioritaire

⚖️ SANCTIONS
• Avertissements → Mute → Kick → Ban
• Sanctions selon gravité
• Possibilité d'appel

📅 Règlement mis à jour le: 25/12/2024
Spike Rush - Respect du règlement obligatoire
```

## 🔒 Permissions Requises

**Bot :**
- `Send Messages` - Envoyer des messages
- `Embed Links` - Intégrer des liens
- `Read Message History` - Lire l'historique

**Admin (commandes de gestion) :**
- `Manage Guild` - Gérer le serveur
- `Administrator` - Administrateur

**Utilisateurs :**
- Aucune permission spéciale pour `!reglement`

## 📝 Personnalisation

### Modifier le règlement
Le contenu est défini dans le code du cog. Pour modifier :

1. Éditer le fichier `reglement.py`
2. Modifier la variable `rules_content`
3. Recharger le cog : `!reload accueil.regles`

### Modifier le channel par défaut
```bash
!reglement channel #nouveau-channel-regles
```

### Changer les couleurs
Modifier `discord.Color.red()` dans le code pour une autre couleur.

## 🐛 Résolution de Problèmes

### Le règlement ne s'affiche pas
1. Vérifier que le cog est chargé : `!loaded`
2. Contrôler les permissions du bot
3. Tester dans un autre channel

### Erreur de permissions
1. Vérifier les permissions bot dans le channel
2. S'assurer que l'utilisateur a les droits admin (si commande admin)
3. Vérifier la configuration : `!reglement config`

### Channel introuvable
1. Vérifier que le channel existe
2. Reconfigurer : `!reglement channel #règles`
3. Vérifier l'ID du channel

## 📊 Statistiques d'Usage

Le cog peut être étendu pour tracker :
- Nombre d'affichages du règlement
- Utilisateurs ayant consulté les règles
- Fréquence d'utilisation par channel

## 🔄 Mises à Jour

### Version 1.0.0 (Actuelle)
- ✅ Affichage du règlement complet
- ✅ Commandes utilisateur et admin
- ✅ Configuration du channel
- ✅ Design gaming moderne
- ✅ Alias et raccourcis

### Améliorations futures
- 🔮 Système de confirmation de lecture
- 🔮 Règlement par sections
- 🔮 Traductions multiples
- 🔮 Historique des versions

## 🤝 Support

Pour toute question ou modification :
1. Consultez ce README
2. Testez avec `!reglement`
3. Vérifiez les permissions
4. Contactez un administrateur

## 🎯 Bonnes Pratiques

1. **Mise à jour régulière** du contenu
2. **Channels dédiés** pour les règles
3. **Rappel périodique** aux nouveaux membres
4. **Cohérence** avec les sanctions appliquées
5. **Communication** des changements de règlement 
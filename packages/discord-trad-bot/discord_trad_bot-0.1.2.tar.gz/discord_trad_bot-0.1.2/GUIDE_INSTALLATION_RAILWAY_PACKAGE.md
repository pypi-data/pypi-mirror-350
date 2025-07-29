# Guide d'Installation du Bot de Traduction Discord (Version Package)

Ce guide explique comment installer le bot de traduction Discord sur Railway en utilisant la version package. C'est plus simple que la version précédente !

---

## 1. Prérequis
- Un compte Discord avec droits d'administrateur sur le serveur
- Un compte Railway ([https://railway.app/](https://railway.app/))
- Un navigateur web (Chrome, Firefox, Safari, etc.)

> 💡 **Note importante** : Tu n'as pas besoin d'installer Python ou d'autres outils sur ton ordinateur. Tout se passe directement sur Railway !

---

## 2. Créer une Application et un Bot Discord

1. Va sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique sur "New Application"
3. Donne un nom à l'application (ex: "Trad-Bot")
4. Dans le menu à gauche, clique sur "Bot" puis sur "Add Bot"
5. Clique sur "Reset Token" et copie le Token (garde-le secret !)
6. Active les permissions suivantes :
   - PRESENCE INTENT
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT

---

## 3. Inviter le Bot sur ton Serveur Discord

1. Dans le menu à gauche, clique sur "OAuth2" > "URL Generator"
2. Coche les cases :
   - bot
   - applications.commands
3. Dans "Bot Permissions", coche :
   - VIEW CHANNELS
   - SEND MESSAGES
   - READ MESSAGE HISTORY
   - USE SLASH COMMANDS
4. Copie le lien généré en bas, ouvre-le dans ton navigateur, et invite le bot sur ton serveur.

---

## 4. Créer un Projet Railway

1. Va sur [https://railway.app/](https://railway.app/)
2. Clique sur "New Project"
3. Choisis "Start from scratch"

---

## 5. Configurer les Fichiers du Projet

1. Dans ton projet Railway, crée un nouveau fichier `requirements.txt` avec :
   ```
   discord-trad-bot==1.0.0
   ```

2. Crée un fichier `main.py` avec :
   ```python
   from discord_trad_bot import run_bot

   if __name__ == "__main__":
       run_bot()
   ```

---

## 6. Configurer les Variables d'Environnement

1. Dans Railway, va dans l'onglet "Variables"
2. Ajoute :
   - DISCORD_TOKEN (colle ici le token de ton bot Discord)
   - GOOGLE_TRANSLATE_API_KEY (laisse vide ou mets un texte bidon)

---

## 7. Configurer le Service Railway

1. Va dans l'onglet "Settings"
2. Configure :
   - INSTALL COMMAND : `pip install -r requirements.txt`
   - START COMMAND : `python main.py`

---

## 8. Déployer et Lancer le Bot

1. Clique sur "Deploy"
2. Vérifie les logs pour voir si tout fonctionne
3. Le bot devrait apparaître en ligne sur ton serveur Discord !

---

## 9. Mettre à Jour le Bot

Quand une nouvelle version est disponible :
1. Modifie simplement le numéro de version dans `requirements.txt`
2. Railway mettra à jour automatiquement le bot

---

## 10. Utiliser le Bot

Les commandes restent les mêmes :
- `!setlang fr` : Définir ta langue
- `!mylang` : Voir ta langue actuelle
- `!languages` : Voir les langues supportées
- `!settranschannel` : Définir le canal de traduction

---

## Besoin d'Aide ?

- Demande à Pierre ou envoie une capture d'écran du problème !

---

**Bon jeu et bonnes traductions !** 🎮🌍 
# Guide d'Installation et de Déploiement du Bot de Traduction Discord sur Railway

Ce guide explique étape par étape comment installer et faire tourner le bot de traduction Discord 24/7 sur Railway, sans avoir besoin de laisser son ordinateur allumé. Il est rédigé pour un utilisateur non technique.

---

## 1. Prérequis
- Un compte Discord avec droits d'administrateur sur le serveur où tu veux installer le bot
- Un compte GitHub (pour cloner le code du bot)
- Un compte Railway ([https://railway.app/](https://railway.app/))

---

## 2. Créer une Application et un Bot Discord

1. Va sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique sur "New Application" (Nouvelle application)
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

## 4. Cloner le Code du Bot

1. Va sur [https://github.com/PierreTsia/discord-trad-bot](https://github.com/PierreTsia/discord-trad-bot)
2. Clique sur "Code" > "Download ZIP" et extrais le dossier, **ou** utilise Git si tu sais faire :
   ```bash
   git clone https://github.com/PierreTsia/discord-trad-bot.git
   ```

---

## 5. Créer un Compte Railway et Déployer le Bot

1. Va sur [https://railway.app/](https://railway.app/) et crée un compte (connexion avec GitHub recommandée)
2. Clique sur "New Project" puis "Deploy from GitHub repo"
3. Sélectionne le dépôt du bot (discord-trad-bot)
4. Attends que Railway importe le projet

---

## 6. Configurer les Variables d'Environnement sur Railway

1. Va dans l'onglet "Variables" de Railway
2. Ajoute :
   - DISCORD_TOKEN (colle ici le token de ton bot Discord)
   - GOOGLE_TRANSLATE_API_KEY (laisse vide ou mets un texte bidon, ce n'est pas utilisé)

---

## 7. Configurer le Service Railway

1. Va dans l'onglet "Settings" de ton service
2. Vérifie ou modifie :
   - INSTALL COMMAND :
     ```
     pip install -r requirements.txt
     ```
   - START COMMAND :
     ```
     python -m src.main
     ```

---

## 8. Déployer et Lancer le Bot

1. Clique sur "Deploy" (ou attends, ça peut se lancer automatiquement)
2. Va dans l'onglet "Logs" pour vérifier que tout fonctionne
   - Tu dois voir un message du style :
     ```
     trad-bot#XXXX has connected to Discord!
     ```
3. Va sur ton serveur Discord : le bot doit apparaître en ligne !

---

## 9. Utiliser le Bot

- **Définir ta langue préférée :**
  ```
  !setlang fr
  ```
- **Voir ta langue actuelle :**
  ```
  !mylang
  ```
- **Voir les langues supportées :**
  ```
  !languages
  ```
- **Définir le canal de traduction (en tant qu'admin) :**
  Va dans le canal voulu et tape :
  ```
  !settranschannel
  ```
- **Traduction automatique :**
  Tout message posté dans ce canal sera traduit dans la langue préférée de chaque utilisateur.

---

## 10. Conseils et Problèmes Fréquents

- **Le bot n'apparaît pas ?**
  - Vérifie le token, les permissions, et que tu es bien admin sur le serveur.
- **Le bot ne répond pas ?**
  - Regarde les logs sur Railway (onglet "Logs").
- **Le bot s'arrête ?**
  - Sur le gratuit, tu as 500h/mois. Si tu veux plus, il faudra passer à une offre payante.
- **Les préférences sont perdues après un redéploiement ?**
  - C'est normal sur le gratuit. Pour garder les données, il faut une option payante (volume persistant).

---

## 11. Mise à Jour du Bot

- Pour mettre à jour le bot, il suffit de faire un "pull" des dernières modifications sur GitHub, ou de re-déployer sur Railway.
- Tu peux aussi modifier les variables d'environnement sur Railway si besoin.

---

## 12. Besoin d'Aide ?

- Demande à Pierre ou envoie une capture d'écran du problème !

---

**Bon jeu et bonnes traductions !** 🎮🌍 
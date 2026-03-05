# Projet PI2 — Chatbot Helpcenter

Ce projet met en place un Helpcenter interactif doté d'un chatbot. Il est construit autour d'une architecture moderne séparant le frontend, le backend et la base de données.

## 📋 Fonctionnalités Principales

- **Backend Python (FastAPI)** : Expose une API REST, notamment la route `/ask` pour interroger la logique du chatbot.
- **Frontend Vue.js (Vite)** : Interface de chat réactive et fluide pour l'utilisateur.
- **Base de données (MariaDB/MySQL)** : Stockage des historiques d'échanges (géré via XAMPP).

---

## 🏗️ Architecture et Flux de Données

- **Frontend** : `http://localhost:5173`
- **Backend** : `http://localhost:8000`
- **Base de données** : `localhost:3306`

**Flux d'interaction :**
1. L’utilisateur pose une question dans l'interface Vue.js.
2. Le frontend envoie une requête `POST /ask` au backend FastAPI.
3. FastAPI traite la requête via la logique Python du chatbot.
4. La réponse est renvoyée au frontend et affichée dans l’interface.
5. *(Optionnel)* Les échanges sont persistés dans la base de données.

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

### 1. Python
- Version 3.12 ou supérieure recommandée.
- Pour vérifier votre installation :
  ```bash
  py --version
  # ou python --version (selon votre système)

  ## 🌐 Frontend (Vue.js / Vite)


### 2.Node.js
Node.js et son gestionnaire de paquets (`npm`) doivent être installés sur votre machine.

Pour vérifier votre installation, ouvrez un terminal et tapez :
```bash
node -v
npm -v
```

cd chatbot-ui

# Installation des dépendances du projet (via le package.json)
npm install

# Installation d'Axios pour gérer les requêtes HTTP vers le backend
npm install axios

cd chatbot-ui
npm run dev

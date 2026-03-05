# Chatbot Helpcenter – Projet PI2

Ce projet met en place un chatbot accessible via une interface web.

Architecture :
- **Frontend** : Vue.js (Vite) 
- **Backend** : FastAPI (Python)
- **Base de données** : MariaDB / MySQL (via XAMPP)

---

# Prérequis

Installer :

- Python (≥ 3.12)
- Node.js (npm inclus) https://nodejs.org/fr/download
- XAMPP (MariaDB / MySQL) https://www.apachefriends.org/

Vérifier les installations :

```bash
python --version
node -v
npm -v
```
#Installation
BackEnd (Python)
Dans le dossier du projet :
```bash
pip install -r requirements.txt
```

Frontend (Vue)
```bash
cd chatbot-ui
npm install
npm install axios
```

#Lancer l'application
1. Ouvrir XAMPP et lancer MySQL.

2. Lancer le backEnd
```bash
py -m uvicorn api:app --reload
```

3. Lancer le frontend
```bash
cd chatbot-ui
npm run dev
```
Interface disponible sur : http://localhost:5173


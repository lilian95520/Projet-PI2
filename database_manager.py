import mysql.connector
from config import DB_CONFIG

def get_connection():
    """Crée une connexion en utilisant la config sécurisée."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialise la table si elle n'existe pas."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_interactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query_text TEXT,
                predicted_reply TEXT,
                confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Connexion MariaDB réussie via config sécurisée.")
    except Exception as e:
        print(f"❌ Erreur d'initialisation : {e}")

def log_interaction(query, response, score):
    """Enregistre une interaction."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO logs_interactions (query_text, predicted_reply, confidence_score) VALUES (%s, %s, %s)"
        cursor.execute(sql, (query, response, float(score)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement : {e}")
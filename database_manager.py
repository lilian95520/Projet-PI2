import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG

# Pool de connexions pour éviter les problèmes de connexion
_connection_pool = None

def get_pool():
    """Retourne le pool de connexions (singleton)."""
    global _connection_pool
    if _connection_pool is None:
        try:
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="helpcenter_pool",
                pool_size=5,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print("✅ Pool de connexions MySQL créé")
        except Exception as e:
            print(f"❌ Erreur création pool : {e}")
            _connection_pool = None
    return _connection_pool

def get_connection():
    """Récupère une connexion du pool."""
    pool = get_pool()
    if pool:
        return pool.get_connection()
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
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO logs_interactions (query_text, predicted_reply, confidence_score) VALUES (%s, %s, %s)"
        cursor.execute(sql, (query, response, float(score)))
        conn.commit()
        cursor.close()
        print(f"✅ Interaction enregistrée (score: {score:.4f})")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement : {e}")
    finally:
        if conn:
            conn.close()
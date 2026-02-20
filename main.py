import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
from database_manager import init_db, log_interaction 

# Configuration
FILE_PATH = "dataset.xlsx"
MODEL_NAME = 'intfloat/multilingual-e5-base'
SIMILARITY_THRESHOLD = 0.45

init_db()
model = SentenceTransformer(MODEL_NAME)
df = pd.read_excel(FILE_PATH)
knowledge_embeddings = model.encode(["passage: " + q for q in df['Title'].tolist()], convert_to_tensor=True)

def ask_helpcenter(query):
    query_embedding = model.encode("query: " + query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, knowledge_embeddings)[0]
    best_score, best_idx = torch.max(cos_scores, dim=0)
    
    score = best_score.item()
    
    if score < SIMILARITY_THRESHOLD:
        reply = "<p>Désolé, je n'ai pas trouvé de réponse précise...</p>"
    else:
        result = df.iloc[best_idx.item()]
        reply = result['Content']

    log_interaction(query, reply, score)
    
    return reply

print(ask_helpcenter("combien d'absences en tant qu'alternant max ?"))
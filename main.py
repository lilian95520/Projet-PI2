import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
from database_manager import init_db, log_interaction
import numpy as np
from sentence_transformers import CrossEncoder

#Configuration
reranker = CrossEncoder('BAAI/bge-reranker-v2-m3')
FILE_PATH = "dataset.xlsx"
MODEL_NAME = 'intfloat/multilingual-e5-base'
SIMILARITY_THRESHOLD = 0.1

init_db()
model = SentenceTransformer(MODEL_NAME)
df = pd.read_excel(FILE_PATH)
knowledge_embeddings = model.encode(["passage: " + q for q in df['Title'].tolist()], convert_to_tensor=True)

def ask_helpcenter(query):
    query_embedding = model.encode("query: " + query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, knowledge_embeddings)[0]
    top_k = torch.topk(cos_scores, k=5)
    indices = top_k.indices.tolist()
    
    pairs = [[query, df.iloc[idx]['Title']] for idx in indices]
    
    rerank_scores = reranker.predict(pairs)
    
    best_rerank_idx = np.argmax(rerank_scores)
    score = rerank_scores[best_rerank_idx]
    
    if score < SIMILARITY_THRESHOLD:
        reply = "<p>Désolé, je n'ai pas trouvé de réponse précise...</p>"
    else:
        result =  df.iloc[indices[best_rerank_idx]]
        reply = result['Content']

    log_interaction(query, reply, score)
    
    return reply

print("combien d'absences en tant qu'alternant max ? :", ask_helpcenter("combien d'absences en tant qu'alternant max ?"))
print("comment adopter un chien :", ask_helpcenter("comment adopter un chien"))
print("Je ne veux pas la bourse :", ask_helpcenter("Je ne veux pas la bourse"))
print("Je veux la bourse :",ask_helpcenter("Je veux la bourse"))
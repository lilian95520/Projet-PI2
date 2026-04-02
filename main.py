import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
from database_manager import init_db, log_interaction
from sentence_transformers import CrossEncoder
from langdetect import detect, DetectorFactory
import os

# on initialise le seed pour le détecteur de langue
DetectorFactory.seed = 0

reranker = CrossEncoder('BAAI/bge-reranker-v2-m3')
FILE_QUESTIONS = "dataset questions.csv"
FILE_VIDEOS = "dataset videos.csv"
FILE_TUTOS = "dataset tutoriels.csv"
MODEL_NAME = 'intfloat/multilingual-e5-base'
SIMILARITY_THRESHOLD = 0.1 

#système de cache pour ne pas reencoder les datasets à chaque fois
CACHE_DF = "data_processed.pkl"
CACHE_EMBEDDINGS = "embeddings.pt"

init_db()

model = SentenceTransformer(MODEL_NAME)

#on vérifie si les données sont dans le cache
if os.path.exists(CACHE_DF) and os.path.exists(CACHE_EMBEDDINGS):
    df = pd.read_pickle(CACHE_DF)
    knowledge_embeddings = torch.load(CACHE_EMBEDDINGS)
else:
    df_excel = pd.read_csv(FILE_QUESTIONS, sep=";", encoding='latin-1')
    df_videos = pd.read_csv(FILE_VIDEOS, sep=';', encoding='latin-1')
    df_tutos = pd.read_csv(FILE_TUTOS, sep=';', encoding='latin-1')
    
    df_all = pd.concat([df_excel, df_videos, df_tutos], ignore_index=True)
    df = df_all[df_all['Status'] == 'publish'].copy().reset_index(drop=True)
    
    #encodage
    knowledge_embeddings = model.encode(["passage: " + str(q) for q in df['Title'].tolist()], convert_to_tensor=True)

    #sauvergard dans le cache
    df.to_pickle(CACHE_DF)
    torch.save(knowledge_embeddings, CACHE_EMBEDDINGS)


def ask_helpcenter(query):
    #on cherche d'abord la langue
    try:
        detected_code = detect(query)
        target_lang = "English" if detected_code == 'en' else "Français"
    except:
        target_lang = "Français"

    #Bi-Encoder
    query_embedding = model.encode("query: " + query, convert_to_tensor=True)
    all_cos_scores = util.cos_sim(query_embedding, knowledge_embeddings)[0]

    #on garde la bonne langue
    lang_mask = torch.tensor([1 if l == target_lang else 0 for l in df['Langues'].tolist()], device=all_cos_scores.device)
    filtered_scores = all_cos_scores * lang_mask - (1 - lang_mask) * 1e9 
    print("gfgfg")
    # On prends les 5 meilleurs
    top_k = torch.topk(filtered_scores, k=min(5, len(filtered_scores)))
    indices = top_k.indices.tolist()
    print(top_k.values)
    # Reranking sur ces 5 meilleurs
    pairs = [[query, df.iloc[idx]['Title']] for idx in indices]
    rerank_scores = reranker.predict(pairs)

    # Sélection du meilleur
    best_idx_in_top = np.argmax(rerank_scores)
    final_score = rerank_scores[best_idx_in_top]
    best_global_idx = indices[best_idx_in_top]
    
    # On récupère la thématique
    best_theme = df.iloc[best_global_idx]['Thématiques']
    if pd.isna(best_theme) or str(best_theme).strip() == "":
        best_theme = "Général"

    if final_score < SIMILARITY_THRESHOLD:
        reply = f"Désolé, je n'ai pas trouvé de réponse précise. Veuillez pouvez peut-être rechercher dans cette thématique : {best_theme}"
        print("Aucun résultat pertinent trouvé, suggérant la thématique : " + best_theme)
    else:
        reply = df.iloc[best_global_idx]['Content']
        print("Réponse trouvée avec un score de " + str(final_score) + ", thématique : " + best_theme   )
    log_interaction(query, reply, final_score)

    return reply


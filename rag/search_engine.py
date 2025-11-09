import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearchEngine:
    def load_model(self, model_cache_dir='rag/model'):
        model_path = os.path.join(model_cache_dir, 'multilingual-e5-small')
        if not os.path.exists(model_path):
            raise FileNotFoundError("Модель не найдена. Сначала запустите create_model.py")
        self.model = SentenceTransformer(model_path)

    def load_embeddings(self):
        with open('rag/model/embeddings.pkl', 'rb') as f:
            self.embeddings = pickle.load(f)
        with open('rag/model/texts.pkl', 'rb') as f:
            self.texts = pickle.load(f)

    def search(self, query, top_k=5, min_score=0.0):
        query_embedding = self.model.encode([f"query: {query.strip()}"], normalize_embeddings=True)
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_score:
                results.append({
                    'text': self.texts[idx],
                    'score': score,
                    'index': int(idx)
                })
        
        return results

def create_search_engine():
    search_engine = SemanticSearchEngine()
    search_engine.load_model()
    search_engine.load_embeddings()
    return search_engine
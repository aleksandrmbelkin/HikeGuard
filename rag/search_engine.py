import numpy as np
import pickle, os
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
        with open('rag/model/docs.pkl', 'rb') as f:
            self.docs = pickle.load(f)

    def search(self, query, top_k=5, min_score=0.3):
        clean_query = ' '.join(query.strip().split())
        query_for_embedding = f"query: {clean_query}"
        
        query_embedding = self.model.encode(
            [query_for_embedding], 
            normalize_embeddings=True,
            show_progress_bar=False
        )
        
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_score and len(results) < top_k:
                doc = self.docs[idx]
                results.append({
                    'text': doc['text'],
                    'score': score,
                    'index': int(idx),
                    'source': doc['source'],
                    'chunk_id': doc['chunk_id']
                })
            elif len(results) >= top_k:
                break
        
        return results

def create_search_engine():
    search_engine = SemanticSearchEngine()
    search_engine.load_model()
    search_engine.load_embeddings()
    return search_engine
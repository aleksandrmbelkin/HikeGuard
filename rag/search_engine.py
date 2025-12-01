import numpy as np
import pickle, os
from sentence_transformers import SentenceTransformer

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

    def cosine_similarity_numpy(self, vec1, vec2):
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)
        
        # Нормализуем векторы
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2, axis=1)
        
        # Избегаем деления на ноль
        if norm_vec1 == 0 or np.any(norm_vec2 == 0):
            return np.zeros(vec2.shape[0])
        
        # Вычисляем косинусное сходство
        dot_products = np.dot(vec2, vec1.T).flatten()
        similarities = dot_products / (norm_vec2 * norm_vec1)
        
        return similarities

    def search(self, query, top_k=5, min_score=0.3):
        clean_query = ' '.join(query.strip().split())
        query_for_embedding = f"query: {clean_query}"
        
        query_embedding = self.model.encode(
            [query_for_embedding], 
            normalize_embeddings=True,
            show_progress_bar=False
        )
        
        similarities = self.cosine_similarity_numpy(query_embedding[0], self.embeddings)
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
                    'page': doc['page']
                })
            elif len(results) >= top_k:
                break
        
        return results

def create_search_engine():
    search_engine = SemanticSearchEngine()
    search_engine.load_model()
    search_engine.load_embeddings()
    return search_engine
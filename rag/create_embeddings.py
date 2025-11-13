import pickle
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import re

class EmbeddingCreator:
    def load_model(self, model_cache_dir='rag/model'):
        model_path = os.path.join(model_cache_dir, 'multilingual-e5-small')
        if not os.path.exists(model_path):
            raise FileNotFoundError("Модель не найдена. Сначала запустите create_model.py")
        self.model = SentenceTransformer(model_path)

    def create_embeddings(self, docs, batch_size=16, normalize_embeddings=True):
        texts = [doc["text"] for doc in docs]
        normalized_texts = [f"passage: {text.strip()}" for text in texts if text.strip()]
        embeddings = self.model.encode(
            normalized_texts,
            batch_size=batch_size,
            normalize_embeddings=normalize_embeddings,
            show_progress_bar=True,
            convert_to_tensor=False
        )
        return embeddings

    def save_embeddings(self, embeddings, docs):
        os.makedirs('rag/model', exist_ok=True)
        with open('rag/model/embeddings.pkl', 'wb') as f:
            pickle.dump(embeddings, f)
        with open('rag/model/docs.pkl', 'wb') as f:
            pickle.dump(docs, f)

def split_into_sentences(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def group_sentences(sentences, group_size=3):
    chunks = []
    for i in range(0, len(sentences), group_size):
        chunk = ' '.join(sentences[i:i + group_size])
        chunks.append(chunk)
    return chunks

def cutting_up_texts(manual_paths):
    docs = []
    for p in manual_paths:
        path = Path(p)
        if not path.exists():
            print(f"Файл не найден: {p}")
            continue
        
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        sentences = split_into_sentences(text)
        chunks = group_sentences(sentences, group_size=3)
        
        for i, chunk in enumerate(chunks):
            chunk = chunk.strip()
            if len(chunk) > 30:
                docs.append({
                    "source": str(path.name), 
                    "chunk_id": i, 
                    "text": chunk
                })
    
    print(f"Создано чанков: {len(docs)}")
    return docs

def create_default_embeddings():
    print('Создание эмбеддингов')
    files = [
        "osnovi.txt",
        "strategiya.txt"
    ]
    file_paths = [f'data/documents/{file}' for file in files]
    docs = cutting_up_texts(file_paths)
    
    print(f"Обработано документов: {len(docs)}")
    
    creator = EmbeddingCreator()
    creator.load_model()
    embeddings = creator.create_embeddings(docs)
    creator.save_embeddings(embeddings, docs)
    print(f'Эмбеддинги сохранены. Документов: {len(docs)}')

if __name__ == "__main__":
    create_default_embeddings()
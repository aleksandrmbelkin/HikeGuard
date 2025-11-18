import pickle, os, re
from pathlib import Path
from sentence_transformers import SentenceTransformer

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
    # Сохраняем знаки препинания при разделении
    sentences = re.split(r'([.!?]+)', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Объединяем предложения с их знаками препинания
    result = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and re.match(r'[.!?]+', sentences[i + 1]):
            result.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            result.append(sentences[i])
            i += 1
    
    return result

def group_sentences_by_paragraphs(paragraphs, group_size=3):
    """Группирует предложения внутри каждого абзаца отдельно"""
    all_chunks = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
            
        sentences = split_into_sentences(paragraph)
        
        # Группируем предложения внутри этого абзаца
        paragraph_chunks = []
        for i in range(0, len(sentences), group_size):
            chunk = ' '.join(sentences[i:i + group_size])
            paragraph_chunks.append(chunk)
        
        all_chunks.extend(paragraph_chunks)
    
    return all_chunks

def cutting_up_texts(manual_paths):
    docs = []
    for p in manual_paths:
        path = Path(p)
        if not path.exists():
            print(f"Файл не найден: {p}")
            continue
        
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        
        # Сначала разделяем на абзацы
        paragraphs = re.split(r'\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # Группируем предложения внутри каждого абзаца отдельно
        chunks = group_sentences_by_paragraphs(paragraphs, group_size=3)
        
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
    files = [f'data/documents/{file}' for file in os.listdir("data/documents")]
    docs = cutting_up_texts(files)
    
    creator = EmbeddingCreator()
    creator.load_model()
    embeddings = creator.create_embeddings(docs)
    creator.save_embeddings(embeddings, docs)
    print(f'Эмбеддинги сохранены.')

if __name__ == "__main__":
    create_default_embeddings()
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

def cutting_up_texts(manual_paths):
    docs = []
    for p in manual_paths:
        path = Path(p)
        if not path.exists():
            print(f"Файл не найден: {p}")
            continue
        
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        
        # Разделяем текст на страницы по разделителю
        page_separator = r'--------------------------- Страница \d+ ---------------------------'
        pages = re.split(page_separator, text)
        
        # Извлекаем номера страниц из разделителей
        page_numbers = re.findall(r'Страница (\d+)', text)
        
        for page_num, page_text in zip(page_numbers, pages[1:], strict=False):
            page_text = page_text.strip()
            if not page_text:
                continue
                
            # Разделяем страницу на абзацы по переносам строк
            paragraphs = page_text.split('\n')
            paragraphs = [p.strip() for p in paragraphs if p.strip()]
            
            for i, paragraph in enumerate(paragraphs):
                paragraph = paragraph.strip()
                docs.append({
                    "source": str(path.name), 
                    "page": int(page_num),
                    "text": paragraph
                })
    
    print(f"Создано чанков: {len(docs)}")
    return docs

def create_default_embeddings():
    print('Создание эмбеддингов')
    files = [f'data/documents/txt/{file}' for file in os.listdir("data/documents/txt")]
    docs = cutting_up_texts(files)
    
    creator = EmbeddingCreator()
    creator.load_model()
    embeddings = creator.create_embeddings(docs)
    creator.save_embeddings(embeddings, docs)
    print(f'Эмбеддинги сохранены. Документов: {len(docs)}')

if __name__ == "__main__":
    create_default_embeddings()
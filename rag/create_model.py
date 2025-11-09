import os
from sentence_transformers import SentenceTransformer

def create_model(model_name='intfloat/multilingual-e5-small', model_cache_dir='rag/model'):
    os.makedirs(model_cache_dir, exist_ok=True)
    model_path = os.path.join(model_cache_dir, 'multilingual-e5-small')
    
    if os.path.exists(model_path):
        print("Модель уже существует")
        return
    
    print("Создание модели...")
    model = SentenceTransformer(model_name)
    model.save(model_path)
    print("Модель сохранена")

if __name__ == "__main__":
    create_model()
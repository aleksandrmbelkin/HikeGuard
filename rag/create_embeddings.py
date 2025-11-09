import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

class EmbeddingCreator:
    def load_model(self, model_cache_dir='rag/model'):
        model_path = os.path.join(model_cache_dir, 'multilingual-e5-small')
        if not os.path.exists(model_path):
            raise FileNotFoundError("Модель не найдена. Сначала запустите create_model.py")
        self.model = SentenceTransformer(model_path)

    def create_embeddings(self, texts, batch_size=32, normalize_embeddings=True):        
        normalized_texts = [f"passage: {text.strip()}" for text in texts]
        embeddings = self.model.encode(normalized_texts,
                                     batch_size=batch_size,
                                     normalize_embeddings=normalize_embeddings,
                                     show_progress_bar=True)
        return embeddings

    def save_embeddings(self, embeddings, texts):
        with open('rag/model/embeddings.pkl', 'wb') as f:
            pickle.dump(embeddings, f)
        with open('rag/model/texts.pkl', 'wb') as f:
            pickle.dump(texts, f)

def get_default_texts(file_paths):
    if file_paths:
        texts = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_texts = [line.strip() for line in f if line.strip()]
                    texts.extend(file_texts)
            except Exception as e:
                print(f"Ошибка чтения файла {file_path}: {e}")
        return texts
    
    return [
        "Искусственный интеллект - это область компьютерных наук, занимающаяся созданием машин, способных выполнять задачи, требующие человеческого интеллекта.",
        "Машинное обучение является подразделом искусственного интеллекта и focuses на разработке алгоритмов, которые могут учиться на данных.",
        "Глубокое обучение использует нейронные сети с множеством слоев для обработки сложных паттернов в больших объемах данных.",
        "Python является популярным языком программирования для анализа данных и машинного обучения.",
        "Обработка естественного языка позволяет компьютерам понимать и интерпретировать человеческий язык.",
        "Компьютерное зрение дает машинам способность видеть и понимать визуальную информацию.",
        "Нейронные сети вдохновлены структурой человеческого мозга и состоят из взаимосвязанных узлов.",
        "Большие данные относятся к extremely большим наборам данных, которые могут быть analyzed computationally для выявления паттернов.",
        "Обучение с подкреплением является типом машинного обучения, где агент учится, взаимодействуя с окружающей средой.",
        "Тензорные вычисления являются основой современных библиотек глубокого обучения таких как PyTorch и TensorFlow.",
        "Трансформеры - это архитектура нейронных сетей, которая revolutionировала обработку естественного языка.",
        "Эмбеддинги представляют слова или предложения в виде векторов в многомерном пространстве.",
        "Косинусное сходство используется для измерения семантической близости между текстовыми эмбеддингами.",
        "Semantic поиск позволяет находить документы по их смысловому содержанию, а не точному совпадению слов.",
        "Мультиязычные модели могут обрабатывать текст на multiple языках в едином векторном пространстве."
    ]

def create_default_embeddings():
    print('Создание эмбеддингов')
    file_paths = None
    texts = get_default_texts(file_paths)

    creator = EmbeddingCreator()
    creator.load_model()
    embeddings = creator.create_embeddings(texts)
    creator.save_embeddings(embeddings, texts)
    print('Эмбеддинги сохранены')

if __name__ == "__main__":
    create_default_embeddings()
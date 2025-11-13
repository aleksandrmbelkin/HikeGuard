from rag.search_engine import create_search_engine

def test_search():
    query = input()
    search_engine = create_search_engine()
    
    print(f"Поиск...")
    results = search_engine.search(query, top_k=5)
    print(results)
    for i, result in enumerate(results, 1):
        print(f"  {i}. [{result['score']:.4f}]")
        print(f"     Файл: {result['source']}")
        print(f"     Чанк: {result['chunk_id']}")
        print(f"     Текст: {result['text'][:300]}...")

if __name__ == "__main__":
    test_search()
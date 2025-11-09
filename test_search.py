from rag.search_engine import create_search_engine
from rag.create_embeddings import create_default_embeddings

def test_search():
    search_engine = create_search_engine()
    
    query = input()
    print(f'Поиск: "{query}"')
    results = search_engine.search(query, top_k=3)
    for i, result in enumerate(results, 1):
        print(f"  {i}. [{result['score']:.4f}] {result['text']}")

if __name__ == "__main__":
    test_search()
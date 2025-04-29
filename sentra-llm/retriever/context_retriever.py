from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Инициализация модели и клиента один раз
model = SentenceTransformer('all-MiniLM-L6-v2')
client = QdrantClient(host="localhost", port=6333)
collection_name = "sentra_knowledge"

def retrieve_context(alert_description: str) -> str:
    """
    Находит наиболее релевантную политику для алерта через векторный поиск.

    Args:
        alert_description: Описание инцидента

    Returns:
        Политика реагирования (строка)
    """
    query_vector = model.encode(alert_description).tolist()

    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=1
    )

    if not search_result:
        return "No specific policy found."

    payload = search_result[0].payload
    return payload.get("policy", "No specific policy found.")

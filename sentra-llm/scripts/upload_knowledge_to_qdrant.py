import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Путь к базе знаний
KNOWLEDGE_PATH = "data/security_knowledge.json"

# Загружаем политики
with open(KNOWLEDGE_PATH, "r") as f:
    policies = json.load(f)

# Используем модель для эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

# Подключаемся к локальному Qdrant
client = QdrantClient(host="localhost", port=6333)

# Создаём коллекцию
collection_name = "sentra_knowledge"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Готовим данные для загрузки
points = []
for idx, policy in enumerate(policies):
    text = f"{policy['category']} ({policy['severity']}): {policy['policy']}"
    embedding = model.encode(text).tolist()
    points.append(
        PointStruct(id=idx, vector=embedding, payload=policy)
    )

# Загружаем все политики
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"✅ Uploaded {len(points)} policies to Qdrant.")

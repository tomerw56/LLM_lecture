from sentence_transformers  import SentenceTransformer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"  # if local
os.environ["TRANSFORMERS_VERBOSITY"] = "info"
os.environ["DIFFUSERS_VERBOSITY"] = "debug"

# Download from the 🤗 Hub
model = SentenceTransformer(r"d:\models\embeddinggemma-300m")

# Run inference with queries and documents
query = "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]
query_embeddings = model.encode_query(query)
document_embeddings = model.encode_document(documents)
print(query_embeddings.shape, document_embeddings.shape)
# (768,) (4, 768)

# Compute similarities to determine a ranking
similarities = list(model.similarity(query_embeddings, document_embeddings).flatten())
print(similarities)
max_index=similarities.index(max(similarities))
print(f"note the index {max_index} with most similarity - {documents[max_index]}")
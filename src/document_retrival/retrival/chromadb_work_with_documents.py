# rag_ollama.py
import os
import pprint

import requests
import chromadb
from chromadb.utils import embedding_functions

from sentence_transformers  import SentenceTransformer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"  # if local
os.environ["TRANSFORMERS_VERBOSITY"] = "info"
os.environ["DIFFUSERS_VERBOSITY"] = "debug"

# Download from the 🤗 Hub
model = SentenceTransformer(r"d:\models\embeddinggemma-300m")

# initialize chroma client
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("docs")

def get_embedding(text):
    document_embeddings = model.encode_document(text)
    return document_embeddings

def add_documents(folder="."):
    """Embed and store all .txt files."""
    for fn in os.listdir(folder):
        if fn.endswith(".txt"):
            path = os.path.join(folder, fn)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            emb = get_embedding(text)
            collection.add(
                documents=[text],
                embeddings=[emb],
                ids=[fn]
            )
            print(f"Added {fn}")
    print("✅ All documents embedded.")

def retrieve(query, n_results):
    """Find top-N relevant docs for a question."""
    q_emb = get_embedding(query)
    res = collection.query(query_embeddings=[q_emb], n_results=n_results)
    docs = res["documents"][0]
    ids = res["ids"][0]
    distances=res["distances"][0]
    return list(zip(ids, docs,distances))
if __name__ == "__main__":
    # Ingest
    add_documents(".")

    # Ask a few questions
    questions = [
        ("What can you tell me abput Deep learning?",1),
        ("What can you tell me abput Deep learning?", 2),
        ("Tell me a story about the sun",1),
        ("Did technology provide progress from letters.",1)
    ]

    for q,num_results in questions:
        results = retrieve(q, n_results=num_results)
        print(f"for question: {q} num results ={num_results} got {len(results)} results {pprint.pformat(results)}")
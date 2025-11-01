# create_docs.py
docs = {
    "doc1.txt": "The sun rose over the quiet valley. Birds started their morning songs. The village awoke slowly.",
    "doc2.txt": "Technology has transformed human communication. From letters to instant messaging, progress never stops.",
    "doc3.txt": "Deep learning enables computers to see, listen, and understand at a scale never seen before. Its impact is vast."
}

for name, text in docs.items():
    with open(name, "w", encoding="utf-8") as f:
        f.write(text)

print("Documents created:", list(docs.keys()))

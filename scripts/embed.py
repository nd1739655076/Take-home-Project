# scripts/embed.py
import openai
import numpy as np
import faiss
import pickle

openai.api_key = "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"

with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

texts = [item["content"] for item in metadata]
embeddings = []
for i in range(0, len(texts), 10):
    batch = texts[i:i+10]
    res = openai.embeddings.create(
        model="text-embedding-3-small",
        input=batch
    )
    embeddings.extend([e.embedding for e in res.data])

np.save("data/embeddings.npy", np.array(embeddings, dtype=np.float32))
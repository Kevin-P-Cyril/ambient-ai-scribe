import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading dataset...")

df = pd.read_csv("icd_clean.csv")

df = df[["ICDCode", "text"]].dropna()

print("Loading model... (this may take time first run)")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = df["text"].tolist()
codes = df["ICDCode"].tolist()

print("Generating embeddings in batch...")

embeddings = model.encode(texts, show_progress_bar=True).tolist()

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(path="icd_db")
collection = client.get_or_create_collection(name="icd10_codes")

print("Storing data into vector DB...")

BATCH_SIZE = 5000

for i in range(0, len(texts), BATCH_SIZE):
    batch_texts = texts[i:i+BATCH_SIZE]
    batch_codes = codes[i:i+BATCH_SIZE]
    batch_embeddings = embeddings[i:i+BATCH_SIZE]

    collection.add(
        ids=batch_codes,
        embeddings=batch_embeddings,
        documents=batch_texts,
        metadatas=[{"code": c} for c in batch_codes]
    )

    print(f"Added batch {i} → {i+BATCH_SIZE}")

print("✅ ICD-10 Vector DB created successfully!")
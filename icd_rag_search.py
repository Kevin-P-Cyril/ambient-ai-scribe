import chromadb
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to DB
client = chromadb.PersistentClient(path="icd_db")
collection = client.get_collection(name="icd10_codes")


def get_icd_codes(text):
    query_embedding = model.encode(text).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    seen = set()
    output = []

    for i in range(len(results["ids"][0])):
        code = results["metadatas"][0][i]["code"]

        if code not in seen:
            seen.add(code)
            output.append({
                "code": code,
                "description": results["documents"][0][i]
            })

        if len(output) == 3:
            break

    return output


# TEST
if __name__ == "__main__":
    test = "patient has high blood sugar and frequent urination"
    result = get_icd_codes(test)

    print("\nTOP ICD CODES:\n")
    for r in result:
        print(r["code"], ":", r["description"])
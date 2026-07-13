"""ICD-10 code recommendation via Retrieval-Augmented Generation.

Primary path: semantic search against the ChromaDB vector store built by
`build_icd_db.py` (embeddings from `all-MiniLM-L6-v2`, indexed from
`ICDCodeSet.csv`). This is the "RAG for ICD-10 Code Recommendation"
Week 3 deliverable.

Fallback path: if the vector DB hasn't been built yet (fresh checkout,
`icd_db/` missing) or chromadb/sentence-transformers aren't installed, we
fall back to a small hardcoded keyword map so the rest of the app (and
tests) keep working without error. A warning is logged once so it's
obvious in server logs that the app is running in degraded mode.
"""

import os
import warnings

BASE_DIR = os.path.dirname(__file__)
ICD_DB_PATH = os.path.join(BASE_DIR, "icd_db")
COLLECTION_NAME = "icd10_codes"

_embedder = None
_collection = None
_rag_ready = None  # tri-state: None = not checked yet, True/False after first check

_FALLBACK_ICD_MAP = [
    ('diabetes', 'E11.9', 'Type 2 diabetes mellitus without complications'),
    ('hypertension', 'I10', 'Essential (primary) hypertension'),
    ('asthma', 'J45.909', 'Unspecified asthma, uncomplicated'),
    ('pneumonia', 'J18.9', 'Pneumonia, unspecified organism'),
    ('chest pain', 'R07.9', 'Chest pain, unspecified'),
    ('headache', 'R51', 'Headache'),
    ('fever', 'R50.9', 'Fever, unspecified'),
    ('back pain', 'M54.5', 'Low back pain'),
    ('cough', 'R05.9', 'Cough, unspecified'),
    ('sore throat', 'J02.9', 'Acute pharyngitis, unspecified'),
    ('depression', 'F32.9', 'Major depressive disorder, single episode, unspecified'),
    ('anxiety', 'F41.9', 'Anxiety disorder, unspecified'),
]


def _fallback_lookup(text):
    normalized = (text or "").lower()
    results = []
    for keyword, code, description in _FALLBACK_ICD_MAP:
        if keyword in normalized:
            results.append({'code': code, 'description': description})
        if len(results) == 3:
            break
    if not results:
        results = [
            {'code': 'R69', 'description': 'Illness, unspecified'},
            {'code': 'Z71.1', 'description': 'Person with feared health complaint in whom no diagnosis is made'},
            {'code': 'Z00.00', 'description': 'Encounter for general adult medical examination without abnormal findings'},
        ]
    return results


def _init_rag():
    """Lazily connect to the pre-built Chroma collection. Returns True if
    RAG search is usable, False if we should fall back to keyword search."""
    global _embedder, _collection, _rag_ready

    if _rag_ready is not None:
        return _rag_ready

    if not os.path.isdir(ICD_DB_PATH):
        warnings.warn(
            f"ICD vector DB not found at '{ICD_DB_PATH}'. Run `python build_icd_db.py` "
            "after `python prepare_icd.py` to enable semantic ICD-10 search. "
            "Falling back to keyword matching for now."
        )
        _rag_ready = False
        return False

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer

        client = chromadb.PersistentClient(path=ICD_DB_PATH)
        _collection = client.get_collection(name=COLLECTION_NAME)
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        _rag_ready = True
    except Exception as exc:  # pragma: no cover - environment dependent
        warnings.warn(f"ICD RAG backend unavailable ({exc}); falling back to keyword matching.")
        _rag_ready = False

    return _rag_ready


def get_icd_codes(text, top_k=3):
    """Return the top_k most relevant ICD-10 codes for the given clinical
    assessment text, using semantic vector search when available."""
    if not text or not text.strip():
        return []

    if _init_rag():
        try:
            query_embedding = _embedder.encode([text]).tolist()
            res = _collection.query(query_embeddings=query_embedding, n_results=top_k)
            docs = (res.get("documents") or [[]])[0]
            metadatas = (res.get("metadatas") or [[]])[0]
            results = []
            for doc, meta in zip(docs, metadatas):
                code = (meta or {}).get("code", "")
                description = doc.split(" ", 1)[1] if " " in doc else doc
                results.append({"code": code, "description": description})
            if results:
                return results
        except Exception as exc:  # pragma: no cover - environment dependent
            warnings.warn(f"ICD RAG query failed ({exc}); falling back to keyword matching.")

    return _fallback_lookup(text)


if __name__ == "__main__":
    sample = "patient has high blood sugar and frequent urination"
    for r in get_icd_codes(sample):
        print(r["code"], ":", r["description"])

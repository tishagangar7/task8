# pipeline/retriever.py

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Path to your Prolog KB
KB_PATH = os.path.join(os.path.dirname(__file__), "..", "kb.pl")

def load_kb_docs() -> list[Document]:
    """Load each non-comment line of kb.pl as a Document."""
    with open(KB_PATH) as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith('%')]
    return [Document(page_content=line) for line in lines]

def get_vector_store(index_path: str | None = None) -> FAISS:
    """
    Build (or rebuild) a FAISS index over the KB docs.
    If index_path is provided, also save the index to that folder.
    """
    docs = load_kb_docs()
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    store = FAISS.from_documents(docs, embedder)
    if index_path:
        store.save_local(index_path)
    return store

# Optional convenience: load a previously saved index
def load_vector_store(index_path: str) -> FAISS:
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(index_path, embedder)


#!/usr/bin/env python3
"""
rag.py

Simplest RAG + Prolog demo over kb.pl:

1. InMemoryVectorStore for all facts
2. Naive NL→Prolog mapping for parents/cousins
3. pyswip execution
"""

import os, getpass, re
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API key: ").strip()

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

from pipeline.retriever import load_kb_docs
from pipeline.prolog_agent import query_prolog

def init_memory_store():
    raw = load_kb_docs()
    facts = [Document(page_content=d.page_content) for d in raw]
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return InMemoryVectorStore.from_documents(facts, embedding=embedder)

def get_top_facts(question: str, store, k: int = 3):
    return [doc.page_content for doc in store.similarity_search(question, k=k)]

def map_to_prolog(question: str) -> str:
    q = question.lower()
    m = re.search(r"who are ([a-z]+)[’']?s parents", q)
    if m:
        return f"parent(X, {m.group(1)})."
    m = re.search(r"parents of ([a-z]+)", q)
    if m:
        return f"parent(X, {m.group(1)})."
    m = re.search(r"who are ([a-z]+)[’']?s cousins", q)
    if m:
        return f"cousin(X, {m.group(1)})."
    m = re.search(r"cousins of ([a-z]+)", q)
    if m:
        return f"cousin(X, {m.group(1)})."
    return ""

def demo(question: str, store):
    print(f"\nQuestion: {question}")
    print("Context:")
    for fact in get_top_facts(question, store):
        print(fact)

    prolog_query = map_to_prolog(question)
    if not prolog_query:
        print("No mapping rule for this question.")
        return

    print(f"Query: {prolog_query}")
    results = query_prolog(prolog_query)
    if not results:
        print("No results.")
    else:
        seen = set()
        for binding in results:
            tup = tuple(binding.items())
            if tup in seen:
                continue
            seen.add(tup)
            print(", ".join(f"{var}={val}" for var, val in binding.items()))

if __name__ == "__main__":
    store = init_memory_store()
    questions = ["Who are Mary's parents?", "Who are Susan's cousins?"]
    for q in questions:
        demo(q, store)


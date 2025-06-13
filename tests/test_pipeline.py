import os
import pytest

from pipeline.retriever import load_kb_docs, get_vector_store
from pipeline.prolog_agent import query_prolog
from pipeline.llm_chain import ask_question

def test_load_kb_docs():
    docs = load_kb_docs()
    # You should have “parent(john, mary).” in your KB
    assert any("parent(john, mary)." in d.page_content for d in docs)

def test_vector_store_search():
    store = get_vector_store()
    results = store.similarity_search("Mary", k=3)
    assert len(results) == 3

def test_query_prolog_parent():
    res = query_prolog("parent(X, mary).")
    xs = {r["X"] for r in res}
    assert "john" in xs and "ann" in xs

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"),
                    reason="OPENAI_API_KEY not set")
def test_ask_question_parents():
    ans = ask_question("Who are Mary's parents?")
    low = ans.lower()
    assert "john" in low and "ann" in low


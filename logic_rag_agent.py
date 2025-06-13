#!/usr/bin/env python3
"""
logic_rag_agent.py

Retrieval‐Augmented Prolog chain over kb.pl:
 1. FAISS‐based RAG for context
 2. LLMChain to translate NL → Prolog
 3. pyswip to execute the query
"""

import os, getpass
from dotenv import load_dotenv

# 1) Load OpenAI API key
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API key: ").strip()

# 2) LangChain‐community imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 3) Your pipeline helpers
from pipeline.retriever import load_kb_docs
from pipeline.prolog_agent import query_prolog

def build_faiss_index(embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
    docs = load_kb_docs()
    embedder = HuggingFaceEmbeddings(model_name=embed_model)
    return FAISS.from_documents(docs, embedder)

def make_prolog_translator():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.0
    )
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Below are some KB facts:
{context}

Translate the user’s question into exactly one Prolog query 
(using only these predicates: parent/2, child/2, sibling/2, grandparent/2, cousin/2, aunt_uncle/2, niece_nephew/2). 
Output only the query and end with a period.

Question: {question}
Prolog:
"""
    )
    return LLMChain(llm=llm, prompt=prompt)

def main():
    index = build_faiss_index()
    translator = make_prolog_translator()

    samples = [
        "Who are Mary’s parents?",
        "Who are Susan’s cousins?"
    ]

    for question in samples:
        # 1) Retrieve context
        hits = index.similarity_search(question, k=3)
        print(f"\nQuestion: {question}")
        print("Context:")
        for hit in hits:
            print(hit.page_content)

        # 2) Translate to Prolog
        prolog_query = translator.run(context="\n".join(d.page_content for d in hits),
                                      question=question).strip()
        if not prolog_query.endswith("."):
            prolog_query += "."

        print(f"Generated query: {prolog_query}")

        # 3) Execute
        results = query_prolog(prolog_query)
        if not results:
            print("No solutions.")
        else:
            for binding in results:
                print(", ".join(f"{var}={val}" for var, val in binding.items()))

if __name__ == "__main__":
    main()


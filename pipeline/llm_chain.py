# pipeline/llm_chain.py

import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from pipeline.retriever import get_vector_store
from pipeline.prolog_agent import query_prolog

# 1) Load your OpenAI key (for ChatOpenAI)
load_dotenv()  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 2) Initialize the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
    temperature=0.0
)

prompt = PromptTemplate(
    input_variables=["context_snippets", "question"],
    template="""
You are a Prolog‐expert assistant. Below are some relevant facts:

{context_snippets}

Here are two examples of how to translate an English question into a Prolog query:

  Example 1:
    Question: Who are Mary’s parents?
    Prolog query: parent(X, mary).

  Example 2:
    Question: List all of Bob’s cousins.
    Prolog query: cousin(X, bob).

Now, translate the following question into exactly one Prolog query (ending with a period), using only these predicates: parent/2, child/2, sibling/2, grandparent/2, cousin/2, aunt_uncle/2, niece_nephew/2.

Question: {question}

Prolog query:
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def ask_question(question: str, k: int = 3) -> str:
    """
    1) Retrieve top-k facts from KB via FAISS.
    2) Ask the LLM to translate NL → Prolog.
    3) Run the Prolog query and format results.
    Returns a human-readable answer string.
    """
    # a) RAG retrieval
    store = get_vector_store()
    docs = store.similarity_search(question, k=k)
    context_snippets = "\n".join(f"- {d.page_content}" for d in docs)

    # b) Generate Prolog query
    prolog_query = chain.run(
        context_snippets=context_snippets,
        question=question
    ).strip()
    if not prolog_query.endswith("."):
        prolog_query += "."

    # c) Execute and format
    results = query_prolog(prolog_query)
    if not results:
        return f"No solutions for `{prolog_query}`"
    lines = [f"{var} = {val}" for res in results for var,val in res.items()]
    return f"Query: `{prolog_query}`\nResults:\n" + "\n".join(" - " + line for line in lines)


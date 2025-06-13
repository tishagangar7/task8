## run_demo.py
#
#from pipeline.retriever import get_vector_store
#from pipeline.prolog_agent import query_prolog
#
#def main():
#    # 1) Build the FAISS index in memory
#    store = get_vector_store()
#
#    # 2) Retrieve top-3 KB lines for a sample question
#    question = "Who are Mary’s parents?"
#    docs = store.similarity_search(question, k=3)
#    print("Retrieved facts:")
#    for d in docs:
#        print(" -", d.page_content)
#
#    # 3) Run the Prolog query
#    results = query_prolog("parent(X, mary).")
#    print("\nProlog bindings for parent(X, mary):")
#    for r in results:
#        print(" ", r)
#
#if __name__ == "__main__":
#    main()
#

# run_demo.py

from pipeline.llm_chain import ask_question

def main():
    q1 = "Who are Mary's parents?"
    print(ask_question(q1))

    q2 = "List all of Bob's cousins."
    print("\n" + ask_question(q2))

if __name__ == "__main__":
    main()


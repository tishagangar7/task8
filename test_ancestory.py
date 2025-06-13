# test_ancestor.py

from pipeline.prolog_agent import query_prolog

def main():
    # 1) Ground query: ancestor(alice, diana)?
    res1 = query_prolog("ancestor(alice, diana).")
    print("ancestor(alice, diana) →", res1)

    # 2) Variable query: ancestor(alice, Y)?
    res2 = query_prolog("ancestor(alice, Y).")
    print("ancestor(alice, Y) →", res2)

if __name__ == "__main__":
    main()


# pipeline/prolog_agent.py

import os
from pyswip import Prolog

# Initialize Prolog and consult the KB once at import time
prolog = Prolog()
KB_PATH = os.path.join(os.path.dirname(__file__), "..", "kb.pl")
prolog.consult(KB_PATH)

def query_prolog(query: str) -> list[dict]:
    """
    Run a Prolog query string (must end with a period).
    Returns a list of dicts with variable bindings.
    """
    query = query.strip()
    if not query.endswith('.'):
        query += '.'
    return list(prolog.query(query))


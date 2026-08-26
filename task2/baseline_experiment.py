import os
from openai import OpenAI
from pyswip import Prolog
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()  # reads OPENAI_API_KEY from .env automatically

def nl_to_prolog(nl_text):
    """Ask OpenAI to convert natural language into Prolog facts/rules and a query."""
    response = client.responses.create(
        model="gpt-4o",
        instructions=(
            "Convert the following into SWI-Prolog. "
            "Respond with ONLY valid Prolog code, no explanations, no markdown formatting, no code fences. "
            "Give the facts and rules first, each ending in a period, then on the last line give a query "
            "starting with '?- ' that tests something based on those facts."
        ),
        input=nl_text
    )
    return response.output_text.strip()

def run_prolog(prolog_code):
    """Take generated Prolog text, assert the facts/rules, run the query."""
    prolog = Prolog()

    # Remove comment lines first
    lines = [l for l in prolog_code.split('\n') if not l.strip().startswith('%')]
    text = ' '.join(lines)

    # Separate the query (starts with ?-) from the rest
    query_line = None
    if '?-' in text:
        text, query_part = text.split('?-', 1)
        query_line = query_part.strip().rstrip('.').strip()

    # Split remaining text into clauses by period
    clauses = [c.strip() for c in text.split('.') if c.strip()]

    for clause in clauses:
        prolog.assertz(clause)

    if query_line:
        results = list(prolog.query(query_line))
        return results
    return "No query found in generated code."

if __name__ == "__main__":
    nl_prompt = (
        "A student passes a class if they complete all assignments and pass the final exam. "
        "Maria completed all her assignments and passed her final exam. "
        "Does Maria pass the class?"
    )

    print("NL Input:", nl_prompt)

    prolog_code = nl_to_prolog(nl_prompt)
    print("\nGenerated Prolog:\n", prolog_code)

    result = run_prolog(prolog_code)
    print("\nResult:", result)

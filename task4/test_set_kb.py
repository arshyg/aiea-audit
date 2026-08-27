from pyswip import Prolog

prolog = Prolog()
prolog.consult("kb.pl")

queries = [
    "eligible(sluggy, cs201)",
    "eligible(anna, cs201)",
    "eligible(anna, math101)",
    "eligible(sluggy, cs101m)",
    "eligible(belle, cs101m)",
    "indirect_prereq(cs201, cs101)",
    "indirect_prereq(cs101m, cs101)"
]

for q in queries:
    result = list(prolog.query(q))
    is_true = len(result) > 0
    print(f"{q}: {is_true}")

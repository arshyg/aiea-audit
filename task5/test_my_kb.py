import sys
sys.path.insert(0, 'Logic-LLM/models/symbolic_solvers/pyke_solver')
from pyke_solver import Pyke_Program

# Restructured from my Task 4 KB (university course prerequisites)
# Original: prereq(cs102, cs101), completed(sluggy, cs101), eligible(Student, Course) :- forall(...)
# Restructured into Pyke's unary-predicate format (one subject + boolean per fact)

logic_program = """Predicates:
CompletedCS101($x, bool) ::: Has x completed CS101?
CompletedCS101m($x, bool) ::: Has x completed CS101m?
CompletedCS102($x, bool) ::: Has x completed CS102?
CompletedMath101($x, bool) ::: Has x completed Math101?
EligibleCS102($x, bool) ::: Is x eligible for CS102?
EligibleCS201($x, bool) ::: Is x eligible for CS201?

Facts:
CompletedCS101(sluggy, True) ::: sluggy completed CS101.
CompletedCS101m(sluggy, True) ::: sluggy completed CS101m.
CompletedCS102(sluggy, True) ::: sluggy completed CS102.
CompletedMath101(sluggy, True) ::: sluggy completed Math101.

Rules:
CompletedCS101($x, True) && CompletedCS101m($x, True) >>> EligibleCS102($x, True) ::: Completing CS101 and CS101m makes you eligible for CS102.
EligibleCS102($x, True) && CompletedMath101($x, True) >>> EligibleCS201($x, True) ::: Being eligible for CS102 and completing Math101 makes you eligible for CS201.

Query:
EligibleCS201(sluggy, True) ::: sluggy is eligible for CS201."""

pyke_program = Pyke_Program(logic_program, 'ProofWriter')
print("Parsed successfully:", pyke_program.flag)

result, error = pyke_program.execute_program()
print("Result:", result)
print("Error (if any):", error)

from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from pyswip import Prolog

from rag import build_retriever, get_relevant_facts

load_dotenv()

prolog = Prolog()
prolog.consult("kb.pl")
retriever = build_retriever("kb.pl", k=5)
llm = ChatOpenAI(model="gpt-4o", temperature=0)

query_chain = ChatPromptTemplate.from_messages([
    ("system", "Write ONLY a Prolog query answering the question, using the facts given. No explanation."),
    ("human", "Facts:\n{context}\n\nQuestion: {question}")
]) | llm | StrOutputParser()

relevance_chain = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY 'yes' or 'no': are these facts enough to answer the question?"),
    ("human", "Question: {question}\n\nFacts:\n{context}")
]) | llm | StrOutputParser()


class State(TypedDict):
    question: str
    facts: List[str]
    attempts: int
    is_relevant: bool
    query: str
    answer: object


def retrieve(state: State) -> State:
    print(f"  [retrieve] attempt {state['attempts'] + 1}", flush=True)
    state["facts"] = get_relevant_facts(retriever, state["question"])
    state["attempts"] += 1
    return state


def judge(state: State) -> State:
    print("  [judge] checking relevance...", flush=True)
    context = "\n".join(state["facts"])
    verdict = relevance_chain.invoke({"question": state["question"], "context": context})
    print(f"  [judge] verdict: {verdict}", flush=True)
    state["is_relevant"] = verdict.strip().lower().startswith("yes")
    return state


def route_after_judge(state: State) -> str:
    if state["is_relevant"] or state["attempts"] >= 2:
        return "generate"
    return "retrieve"


def generate(state: State) -> State:
    print("  [generate] writing query...", flush=True)
    context = "\n".join(state["facts"])
    state["query"] = query_chain.invoke({"context": context, "question": state["question"]}).strip()
    return state


def execute(state: State) -> State:
    print("  [execute] running query...", flush=True)
    state["answer"] = len(list(prolog.query(state["query"]))) > 0
    return state


graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("judge", judge)
graph.add_node("generate", generate)
graph.add_node("execute", execute)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "judge")
graph.add_conditional_edges("judge", route_after_judge, {"retrieve": "retrieve", "generate": "generate"})
graph.add_edge("generate", "execute")
graph.add_edge("execute", END)

app = graph.compile()


def ask(question):
    print(f"Question: {question}", flush=True)
    result = app.invoke(
        {"question": question, "facts": [], "attempts": 0, "is_relevant": False, "query": "", "answer": None},
        config={"recursion_limit": 10}
    )
    print(f"Attempts: {result['attempts']}")
    print(f"Facts: {result['facts']}")
    print(f"Query: {result['query']}")
    print(f"Answer: {result['answer']}")
    print()


if __name__ == "__main__":
    ask("Is sluggy eligible for cs201?")
    ask("Is bob eligible for cs102?")

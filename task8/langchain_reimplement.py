"""
task 8: langchain reimplementation of task 5
NL question -> RAG -> LLM generates Prolog -> PySwip executes
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pyswip import Prolog

from rag import build_retriever, get_relevant_facts

load_dotenv()

prolog = Prolog()
prolog.consult("kb.pl")

retriever = build_retriever("kb.pl")

#chain: context + question ->prolog query
llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Given the Prolog facts/rules below, write ONLY a single Prolog query "
     "that answers the question. No explanation, no period, no markdown. "
     "Example: eligible(sluggy, cs201)"),
    ("human", "Facts:\n{context}\n\nQuestion: {question}")
])

chain = prompt | llm | StrOutputParser()


def ask(question):
    facts = get_relevant_facts(retriever, question)
    context = "\n".join(facts)

    query = chain.invoke({"context": context, "question": question}).strip()

   # try:
    results = list(prolog.query(query))
    answer = len(results) > 0
    

    print(f"Question: {question}")
    print(f"Retrieved facts: {facts}")
    print(f"Generated query: {query}")
    print(f"Answer: {answer}")
    print()


if __name__ == "__main__":
    ask("Is sluggy eligible for cs201?")
    ask("Is bob eligible for cs102?")

"""
task 8: RAG
load kb as text, embed, and retrieve the relevant lines
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def load_kb_lines(path="kb.pl"):
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('%')]
    return lines

#retriever
def build_retriever(path="kb.pl", k=5):
    lines = load_kb_lines(path)
    docs = [Document(page_content=line) for line in lines]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})


def get_relevant_facts(retriever, question):
    docs = retriever.invoke(question)
    return [d.page_content for d in docs]


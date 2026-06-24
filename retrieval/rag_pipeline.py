from vector_store.chroma_store import ChromaStore

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from retrieval.prompts import RAG_PROMPT
from retrieval.hybrid_retriever import build_retriever

from dotenv import load_dotenv

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
        self.retriever = build_retriever(k=8)
        self.chain = self._build_chain()

    def _format_context(self, docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    def _build_chain(self):
        retrieval_chain = {
            "context": self.retriever | RunnableLambda(self._format_context),
            "question": RunnablePassthrough()
        }

        return retrieval_chain | self.prompt | self.llm | StrOutputParser()

    def query(self, question):
        docs = self.retriever.invoke(question)

        context = self._format_context(docs)
        answer = (self.prompt | self.llm | StrOutputParser()).invoke({
            "context": context,
            "question": question
        })

        sources = list(dict.fromkeys(
            doc.metadata["source"] for doc in docs if "source" in doc.metadata
        ))

        return answer, sources
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage


from retrieval.prompts import RAG_PROMPT
from retrieval.hybrid_retriever import build_retriever
from retrieval.query_rewriter import build_query_rewriter

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
        self.query_rewriter = build_query_rewriter()
        # self.chain = self._build_chain()
        self.chat_history = []


    def _format_context(self, docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    # def _build_chain(self):
    #     retrieval_chain = {
    #         "context": self.retriever | RunnableLambda(self._format_context),
    #         "question": RunnablePassthrough()
    #     }

    #     return retrieval_chain | self.prompt | self.llm | StrOutputParser()

    def _format_history(self):
        lines = []
        for msg in self.chat_history[-4:]:  # last 2 exchanges
            if isinstance(msg, HumanMessage):
                lines.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                lines.append(f"Assistant: {msg.content}")
        return "\n".join(lines)

    def query(self, question):

        history = self._format_history()
        full_question = f"{history}\nUser: {question}" if history else question

        rewritten = self.query_rewriter.invoke({"question": full_question})
        print(f"Rewritten query: {rewritten}")

        docs = self.retriever.invoke(rewritten)
        context = self._format_context(docs)

        answer = (self.prompt | self.llm | StrOutputParser()).invoke({
            "context": context,
            "question": question
        })

        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))

        sources = list(dict.fromkeys(
            doc.metadata["source"] for doc in docs if "source" in doc.metadata
        ))

        contexts = [doc.page_content for doc in docs]

        return answer, sources, contexts
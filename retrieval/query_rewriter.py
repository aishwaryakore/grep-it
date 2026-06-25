from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from retrieval.prompts import REWRITE_PROMPT

def build_query_rewriter():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(REWRITE_PROMPT)

    return prompt | llm | StrOutputParser()



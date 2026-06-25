import streamlit as st
from retrieval.rag_pipeline import RAGPipeline

@st.cache_resource
def load_pipeline():
    return RAGPipeline()

rag = load_pipeline()

if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)

    answer, sources, _ = rag.query(user_input)

    st.session_state['message_history'].append({"role": "assistant", "content": answer})
    with st.chat_message('assistant'):
        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for url in sources:
                    st.markdown(f"- [{url}]({url})")
from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

load_dotenv()

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Vedeți mai jos &#9660;\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

st.header("🤖 Asistenta Decolandia", divider='rainbow')
st.markdown(
    """
    <div style="text-align: center; font-size: 24px; color: #1f4e79; font-weight: bold; 
              width:24rem;
              border: 2px solid #1f4e79; padding: 10px; border-radius: 48px;">
        👋 Buna ziua! Cu ce vă pot ajuta?
    </div>
    """,
    unsafe_allow_html=True
)


if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []
    st.session_state["chatbot_open"] = True  # Set to True directly to open the chatbot

if st.session_state["chatbot_open"]:
    prompt = st.chat_input("Ce e sus?")
    if prompt:
        with st.spinner("Se generează răspuns..."):
            generated_response = run_llm(
                query=prompt, chat_history=st.session_state["chat_history"]
            )

            sources = set(
                [doc.metadata["source"] for doc in generated_response["source_documents"]]
            )
            response_message = f"{generated_response['answer']} \n\n {create_sources_string(sources)}"

        # Update chat history after response generation
        st.session_state.chat_history.append((prompt, generated_response["answer"]))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(response_message)

        # Add a button to contact a human operator
        
    if st.session_state["chat_answers_history"]:
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(
                user_query,
                is_user=True,
            )
            message(generated_response)

            st.write(f'''
            <a  href="https://www.decolandia.ro" target="_blank">
                <button style="background-color: #7373d9; 
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 10px;
        cursor: pointer;">
                    Doriți să contactați un operator uman?
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
else:
    st.markdown("")




from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

st.markdown("<h1>🤖 Website Read Chat bot</h1>", unsafe_allow_html=True)

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []
    st.session_state["chatbot_open"] = False

chat_button_clicked = st.button("Chat")  # Button to toggle the chatbot

if chat_button_clicked:
    st.session_state["chatbot_open"] = not st.session_state.get("chatbot_open", False)

if st.session_state["chatbot_open"]:
    # prompt = st.text_input("", placeholder="Enter your message here...")
    with st.form(key='my_form', clear_on_submit=True):
        prompt = st.text_area("You:", key='input', height=50)
        submit_button = st.form_submit_button(label='Send')
    if prompt:
            with st.spinner("Generating response..."):
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
else:
    st.markdown("")

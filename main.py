# from typing import Set
# from backend.core import run_llm
# from ingestion import ingest_docs
# import streamlit as st
# from streamlit_chat import message

# def create_sources_string(source_urls: Set[str]) -> str:
#     if not source_urls:
#         return ""
#     sources_list = list(source_urls)
#     sources_list.sort()
#     sources_string = "sources:\n"
#     for i, source in enumerate(sources_list):
#         sources_string += f"{i+1}. {source}\n"
#     return sources_string

# st.markdown("<h1>🤖 Website Read Chat bot</h1>", unsafe_allow_html=True)

# if (
#     "chat_answers_history" not in st.session_state
#     and "user_prompt_history" not in st.session_state
#     and "chat_history" not in st.session_state
# ):
#     st.session_state["chat_answers_history"] = []
#     st.session_state["user_prompt_history"] = []
#     st.session_state["chat_history"] = []


# prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
#     "Submit"
# )
# if prompt:
#     with st.spinner("Generating response..."):
#         generated_response = run_llm(
#             query=prompt, chat_history=st.session_state["chat_history"]
#         )

#         sources = set(
#             [doc.metadata["source"] for doc in generated_response["source_documents"]]
#         )
#         formatted_response = (
#             f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
#         )

#         st.session_state.chat_history.append((prompt, generated_response["answer"]))
#         st.session_state.user_prompt_history.append(prompt)
#         st.session_state.chat_answers_history.append(formatted_response)

# if st.session_state["chat_answers_history"]:
#     for generated_response, user_query in zip(
#         st.session_state["chat_answers_history"],
#         st.session_state["user_prompt_history"],
#     ):
#         message(
#             user_query,
#             is_user=True,
#         )
#         message(generated_response)



from typing import Set
from backend.core import run_llm
from ingestion import ingest_docs
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

st.markdown("<h1> Website Read Chat bot</h1>", unsafe_allow_html=True)
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


prompt = st.text_input("Prompt", placeholder="Enter your message here...")

if prompt:
    yes_button = st.button("Yes")
    no_button = st.button("No")

    if (
        yes_button
        and ("Do you have radiant heat flooring?" in prompt.lower() or "Aveți pardoseală cu încălzire radiantă?" in prompt.lower())
    ):
        response_message = "Yes, we do, please see here"
    elif no_button:  # If the No button is clicked, regardless of prompt
        response_message = "Exiting chat."  # Indicate exit
        st.session_state.chat_answers_history = []  # Clear chat history
        st.session_state.user_prompt_history = []
        st.session_state.chat_history = []
    else:
          if yes_button:
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

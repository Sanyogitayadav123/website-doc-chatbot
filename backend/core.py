import os
from typing import Any, Dict, List

# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
# from langchain.vectorstores import Pinecone
from langchain_community.vectorstores import Pinecone
import pinecone



pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)

INDEX_NAME = "website-doc"

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=INDEX_NAME,
    )
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo-0613",
        verbose=True,
        temperature=0,
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )

    return qa({"question": query, "chat_history": chat_history})

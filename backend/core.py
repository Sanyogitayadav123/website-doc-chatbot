
import os
from typing import Any, Dict, List
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Pinecone
import pinecone

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


INDEX_NAME = "website-doc"

# Define your static prompts and responses
static_prompts = {
    "Do you have radiant heat flooring?": "Yes, we do, please see here: https://www.decolandia.ro/parchet-pentru-incalzire-prin-pardoseala",
    "Do you have engineered flooring, 10 mm thick, tongue and grove?": "Yes, we have. Please check here: https://www.decolandia.ro/parchet-stratificat/filtrare/grosime-f3,10-mm-v25/tip-prindere-f6,nut-si-feder-v45",
    "which one is in stock?": "For these products, we only have stock at the external provider, meaning a delivery term of 5-10 days for https://www.decolandia.ro/parchet-stratificat/filtrare/grosime-f3,10-mm-v25/tip-prindere-f6,nut-si-feder-v45?stoc=1",
}

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    # Use the static response if the query is in the static prompts
    if query in static_prompts:
        return {"answer": static_prompts[query], "source_documents": []}

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

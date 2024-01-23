
import os
from typing import Any, Dict, List
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Pinecone
from langchain_core.prompts import PromptTemplate
import pinecone
# Create a Pinecone Index with your API key and environment
index = pinecone.Index(
    index_name="website-doc",
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
    host='https://website-doc-o4higtn.svc.gcp-starter.pinecone.io'
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
    qa_template = """
        You are a website supporter to help customer about ecommerce products and other webiste related information: 
     You the following pieces of context to answers the question at the end: 

        question: Do you have radiant heat flooring?
        Yes, we do, please see here

        question: Do you have engineered flooring, 10 mm thick, tongue and grove?
        Yes, we have. Please check here

        question: which one is in stock?     
        For these products we only have stock at the external provider, meaning a delivery term of 5-10 days for

        question: Do you offer installation services?
        we have installation team partners that we may recommend to you, but they are not part of our company. And if he continues: 
        May I have their contact? The answer: For this I will pass you to a human assistant or you may call us.




        context: {context}
        =========
        
        question: {question}
        ======
        👋
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])



    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(),
         return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': QA_PROMPT}
    )

    return qa({"question": query, "chat_history": chat_history})

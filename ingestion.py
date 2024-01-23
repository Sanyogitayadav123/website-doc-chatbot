import os
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain_community.document_loaders.sitemap import SitemapLoader
import pinecone

# pinecone.init(
#     api_key=os.environ["PINECONE_API_KEY"],
#     environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
# )
index = pinecone.Index(
    index_name="website-doc",
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
    host='https://website-doc-o4higtn.svc.gcp-starter.pinecone.io'
)
INDEX_NAME = "website-doc"

def ingest_docs():
    # loader = ReadTheDocsLoader("website-doc/www.decolandia.ro/index.html")
    # print("loader=>",loader)
    sitemap_loader = SitemapLoader(web_path="https://www.decolandia.ro/sitemap.xml")
    raw_documents = sitemap_loader.load()
    # raw_documents = loader.load()
    print("raw_documents=>",raw_documents)
    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("website-doc", "https:/")
        doc.metadata.update({"source": new_url})
#
    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Pinecone")
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorestore done ***")


if __name__ == "__main__":
    ingest_docs()
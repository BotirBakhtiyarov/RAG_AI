# bot/chatbot_logic.py
import os
from openai import OpenAI

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

def load_knowledge_base(folder_path):
    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, file_name), encoding="utf-8")
            raw_documents = loader.load()

            # Split large documents into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            documents.extend(text_splitter.split_documents(raw_documents))

    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(
        documents, embeddings, persist_directory="media/chroma_store"
    )
    return vector_store

def create_rag_chain(vector_store):
    retriever = vector_store.as_retriever()
    llm = ChatOpenAI(model="gpt-4", temperature=0.5)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def update_knowledge_base(vector_store, file_path):
    """
    Updates the vector store with new documents from the given file.

    Parameters:
    - vector_store: The Chroma vector store instance.
    - file_path: Path to the file containing new documents.

    Notes:
    - Only .txt files are supported.
    - The new document is split into smaller chunks before being added to the vector store.
    """
    if file_path.endswith(".txt"):
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            raw_documents = loader.load()

            # Split the document into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            new_documents = text_splitter.split_documents(raw_documents)

            # Add the new documents to the vector store
            vector_store.add_documents(new_documents)

            # Optionally persist changes to disk
            vector_store.persist()

            print(f"Knowledge base successfully updated with file: {file_path}")
        except Exception as e:
            print(f"Error updating knowledge base: {str(e)}")
    else:
        print("Error: Only .txt files are supported.")


client = OpenAI()

def genImage(query):
    response = client.images.generate(
        model = "dall-e-3",
        prompt= query,
        size = "1024x1024",
        n=1
    )
    return response.data[0].url
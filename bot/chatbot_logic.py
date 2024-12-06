# chatbot/chatbot_logic.py
import os
from openai import OpenAI

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from django.conf import settings


# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

def load_knowledge_base(folder_path):
    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, file_name), encoding="utf-8")
            documents.extend(loader.load())
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
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        new_documents = loader.load()
        vector_store.add_documents(new_documents)
        print(f"Knowledge base updated with file: {file_path}")
    else:
        print("Error: Only .txt files are supported.")


# # Define the LLM and chain for generating the image prompt
# llm = OpenAI(temperature=0.9)
# prompt = PromptTemplate(
#     input_variables=["image_desc"],
#     template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
# )
# chain = LLMChain(llm=llm, prompt=prompt)
#
# # Function to generate an image URL using DALL-E
# def generate_dalle_image(query):
#     try:
#         # Shorten the prompt if it's too long
#         max_prompt_length = 1000
#         if len(query) > max_prompt_length:
#             query = query[:max_prompt_length]
#
#         # Use the DALL-E wrapper to generate an image based on the prompt
#         image_url = DallEAPIWrapper().run(chain.run(query))
#         return image_url
#     except Exception as e:
#         print(f"Error generating DALL-E image: {e}")
#         return None

client = OpenAI()

def genImage(query):
    response = client.images.generate(
        model = "dall-e-3",
        prompt= query,
        size = "1024x1024",
        n=1
    )
    return response.data[0].url
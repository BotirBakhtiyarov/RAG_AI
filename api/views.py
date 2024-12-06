from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bot.chatbot_logic import load_knowledge_base, create_rag_chain, genImage
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.schema import AIMessage
from .serializers import ChatResponseSerializer

# chatbot/views.py


class ChatbotAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Load the knowledge base and create RAG chain
        knowledge_base_folder = "media/data"
        vector_store = load_knowledge_base(knowledge_base_folder)
        qa_chain = create_rag_chain(vector_store)

        # Create a fallback ChatGPT chain using LLMChain
        fallback_llm = ChatOpenAI(model="gpt-4", temperature=0.8)
        prompt_template = "You are a helpful assistant. Answer the following question: {query}"
        prompt = PromptTemplate(input_variables=["query"], template=prompt_template)

        # Create fallback chain using RunnableLambda
        fallback_chain = RunnableLambda(fallback_llm, prompt)

        query = request.data.get("query", "").strip()
        llm_mode = request.data.get("llm", "chatgpt")  # Default to ChatGPT if not provided

        if not query:
            return Response({"response": "Please enter a valid query."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the mode and fetch response
        if llm_mode == "base_knowledge":
            # Use the knowledge base for the response
            response = qa_chain.invoke({"query": query})["result"]
        elif llm_mode == "dall-e":
            # Use DALL-E to generate an image
            image_url = genImage(query)
            if image_url:
                response = f"Here is your image: <img src='{image_url}' alt='Generated Image' />"
            else:
                response = "Error generating image."
        else:
            # Use fallback ChatGPT chain
            response = fallback_chain.invoke(query)

        # Check if response is an AIMessage object and extract the content
        if isinstance(response, AIMessage):
            response = response.content  # Extract the content from AIMessage

        # Serialize the response using the ChatResponseSerializer
        serializer = ChatResponseSerializer({"response": response})

        return Response(serializer.data)


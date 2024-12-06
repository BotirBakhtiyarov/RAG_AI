# AI Chatbot with Knowledge Base and Image Generation  

This project is a versatile AI-powered chatbot built using **Django REST Framework** and **LangChain**, designed to provide intelligent and dynamic responses. The chatbot integrates multiple modes of interaction, enabling it to retrieve knowledge-based answers, generate conversational responses, and even create custom AI-generated images using DALL-E.  

## Features  

- **Knowledge Base (RAG):**  
  Retrieve accurate answers from a preloaded knowledge base using **Retrieval-Augmented Generation (RAG)**.  

- **Dynamic Conversational AI:**  
  Use ChatGPT (powered by GPT-4) as a fallback mechanism for conversational queries, offering helpful and insightful responses.  

- **AI Image Generation:**  
  Generate images based on textual prompts with seamless integration of DALL-E for creative tasks.  

- **Flexible Query Handling:**  
  Supports three modes of operation:
  - `base_knowledge` for knowledge-base responses.  
  - `dall-e` for image generation.  
  - `chatgpt` (default) for conversational AI.  

- **RESTful API:**  
  Built with Django REST Framework, allowing easy integration with web or mobile applications.  

## How It Works  

1. **Knowledge Base Setup:**  
   Preload data into the chatbot using the `load_knowledge_base` function, which creates a vectorized knowledge store.  

2. **Query Handling:**  
   - User sends a query via the `/chat/` API endpoint.  
   - The chatbot processes the query based on the specified mode.  
   - Responses are serialized and returned in JSON format.  

3. **Modes:**  
   - `base_knowledge`: Fetches results from the knowledge base.  
   - `dall-e`: Generates an image and returns the URL for rendering.  
   - `chatgpt`: Uses GPT-4 to generate conversational responses.  

## Technologies Used  

- **Backend:** Django REST Framework  
- **AI Integration:** LangChain (ChatOpenAI, RAG Chains), DALL-E  
- **Serialization:** DRF Serializers  
- **Hosting:** Designed to work locally or deployable via Docker  

## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/BotirBakhtiyarov/RAG_AI.git
   cd RAG_AI  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Configure your OpenAI API key in the environment variables.  

4. Start the server:  
   ```bash  
   python manage.py runserver  
   ```  

## API Endpoints  

### `POST /api/chat/`  

**Request Body:**  
```json  
{  
    "query": "What is LangChain?",  
    "llm": "base_knowledge"  
}  
```  

**Response:**  
```json  
{  
    "response": "LangChain is a framework for building applications with LLMs..."  
}  
```  

## Future Enhancements  

- Add multi-language support for global accessibility.  
- Enhance the knowledge base with dynamic data sources.  
- Improve image rendering with additional AI models.  
- Build a frontend interface for an intuitive user experience.  

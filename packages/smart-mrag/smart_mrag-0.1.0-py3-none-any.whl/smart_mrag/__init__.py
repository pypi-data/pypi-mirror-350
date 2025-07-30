import os
from typing import Optional, List, Dict
import numpy as np
import faiss
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import fitz
from PIL import Image
import base64
import io
from .core import SmartMRAG
from .utils import ModelConfig

__version__ = "0.1.0"

# Define recommended model combinations
RECOMMENDED_MODELS = {
    "openai": {
        "llm_models": [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-4-32k",
            "gpt-4-turbo-preview",
            "gpt-4-vision-preview",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4o-turbo"
        ],
        "embedding_models": [
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-3-large-256"
        ],
        "requires": ["openai_api_key"]
    },
    "anthropic": {
        "llm_models": ["claude-3-opus", "claude-3-sonnet", "claude-2.1"],
        "embedding_models": ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"],
        "requires": ["anthropic_api_key", "openai_api_key"]
    },
    "google": {
        "llm_models": ["gemini-pro", "gemini-ultra"],
        "embedding_models": ["textembedding-gecko", "textembedding-gecko-multilingual"],
        "requires": ["google_api_key"]
    }
}

def get_recommended_models():
    """Returns a dictionary of recommended model combinations."""
    return RECOMMENDED_MODELS

def get_required_api_keys(llm_model, embedding_model):
    """
    Returns the API keys required for the given model combination.
    
    Args:
        llm_model (str): The LLM model name
        embedding_model (str): The embedding model name
        
    Returns:
        list: List of required API key names
    """
    required_keys = set()
    
    # Check OpenAI models
    if any(model in llm_model for model in ["gpt-3.5", "gpt-4"]):
        required_keys.add("openai_api_key")
    if any(model in embedding_model for model in ["text-embedding"]):
        required_keys.add("openai_api_key")
        
    # Check Anthropic models
    if any(model in llm_model for model in ["claude"]):
        required_keys.add("anthropic_api_key")
        
    # Check Google models
    if any(model in llm_model for model in ["gemini"]):
        required_keys.add("google_api_key")
    if any(model in embedding_model for model in ["textembedding-gecko"]):
        required_keys.add("google_api_key")
        
    return list(required_keys)

__all__ = ["SmartMRAG", "ModelConfig", "get_recommended_models", "get_required_api_keys"]

class SmartMRAG:
    # Define default model combinations
    DEFAULT_MODELS = {
        "gpt-4o": {
            "embedding_model": "text-embedding-ada-002",
            "provider": "openai"
        },
        "gpt-4": {
            "embedding_model": "text-embedding-ada-002",
            "provider": "openai"
        },
        "gpt-4-turbo": {
            "embedding_model": "text-embedding-ada-002",
            "provider": "openai"
        },
        "gpt-4-vision": {
            "embedding_model": "text-embedding-ada-002",
            "provider": "openai"
        },
        "gpt-3.5-turbo": {
            "embedding_model": "text-embedding-ada-002",
            "provider": "openai"
        }
    }

    def __init__(
        self,
        file_path: str,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o",
        embedding_model: Optional[str] = None,
        embedding_api_key: Optional[str] = None
    ):
        """
        Initialize the SmartMRAG reader.
        
        Args:
            file_path (str): Path to the PDF file
            api_key (str, optional): API key. If not provided, will look for OPENAI_API_KEY in environment variables
            model_name (str, optional): Model name. Defaults to "gpt-4o"
            embedding_model (str, optional): Embedding model name. If not provided, will use default for the selected model
            embedding_api_key (str, optional): API key for embedding model if different from main API key
        """
        self.file_path = file_path
        self.model_name = model_name
        
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get API key from environment or provided value
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Please provide it or set OPENAI_API_KEY environment variable")
        
        # Handle embedding model
        if embedding_model:
            # If user provided embedding model, validate it
            if model_name in self.DEFAULT_MODELS and embedding_model != self.DEFAULT_MODELS[model_name]["embedding_model"]:
                # If different from default, require embedding API key
                if not embedding_api_key:
                    raise ValueError(f"Embedding API key is required when using custom embedding model: {embedding_model}")
                self.embedding_api_key = embedding_api_key
            else:
                self.embedding_api_key = self.api_key
        else:
            # Use default embedding model for the selected model if it's a default model
            if model_name in self.DEFAULT_MODELS:
                embedding_model = self.DEFAULT_MODELS[model_name]["embedding_model"]
            else:
                raise ValueError("Embedding model is required when using a non-default model")
            self.embedding_api_key = self.api_key
        
        self.embedding_model = embedding_model
        
        # Initialize OpenAI clients
        self.client = OpenAI(api_key=self.api_key)
        self.llm = ChatOpenAI(api_key=self.api_key, model=model_name)
        self.embedding_client = OpenAI(api_key=self.embedding_api_key)
        
        # Initialize document processing
        self.docs = self._load_documents()
        self.chunks = self._break_into_chunks()
        self.vector_store = self._create_vector_store()
    
    def _load_documents(self) -> List:
        """Load and validate the PDF document."""
        try:
            loader = PyPDFLoader(self.file_path)
            return loader.load()
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
    
    def _break_into_chunks(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
        """Split document into chunks."""
        try:
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            return text_splitter.split_documents(self.docs)
        except Exception as e:
            raise Exception(f"Error splitting document: {str(e)}")
    
    def _get_vector_embeddings(self, text: str) -> List[float]:
        """Get vector embeddings for text."""
        try:
            response = self.embedding_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return [r.embedding for r in response.data][0]
        except Exception as e:
            raise Exception(f"Error getting embeddings: {str(e)}")
    
    def _create_vector_store(self):
        """Create FAISS vector store from document chunks."""
        try:
            # Get embeddings for all chunks
            embeddings = [self._get_vector_embeddings(chunk.page_content) for chunk in self.chunks]
            embeddings = np.array(embeddings).astype('float32')
            
            # Create and train FAISS index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            
            return index
        except Exception as e:
            raise Exception(f"Error creating vector store: {str(e)}")
    
    def _get_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        """Get most relevant chunks for a query."""
        try:
            # Get query embedding
            query_embedding = self._get_vector_embeddings(query)
            query_embedding = np.array([query_embedding]).astype('float32')
            
            # Search for similar chunks
            distances, indices = self.vector_store.search(query_embedding, k)
            
            # Return relevant chunks
            return [self.chunks[i].page_content for i in indices[0]]
        except Exception as e:
            raise Exception(f"Error getting relevant chunks: {str(e)}")
    
    def ask_question(self, question: str) -> str:
        """
        Ask a question about the document.
        
        Args:
            question (str): The question to ask
            
        Returns:
            str: The answer to the question
        """
        try:
            # Get relevant chunks
            relevant_chunks = self._get_relevant_chunks(question)
            
            # Create context from chunks
            context = "\n\n".join(relevant_chunks)
            
            # Create prompt
            prompt = f"""Based on the following context, please answer the question. 
            If the answer cannot be found in the context, say "I cannot find the answer in the document."

            Context:
            {context}

            Question: {question}
            """
            
            # Get answer from LLM
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            
            return response.content
        except Exception as e:
            raise Exception(f"Error getting answer: {str(e)}") 
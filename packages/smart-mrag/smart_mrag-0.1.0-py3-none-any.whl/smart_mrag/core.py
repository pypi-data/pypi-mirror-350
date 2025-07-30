from .utils import ModelConfig

class SmartMRAG:
    def __init__(
        self,
        openai_api_key=None,
        anthropic_api_key=None,
        google_api_key=None,
        llm_model="gpt-3.5-turbo",
        embedding_model="text-embedding-ada-002",
        chunk_size=1000,
        chunk_overlap=200,
        similarity_threshold=0.7,
        max_tokens=4000,
        temperature=0.7,
        top_k=5
    ):
        """
        Initialize the SmartMRAG system with specified models and parameters.
        
        Args:
            openai_api_key (str, optional): OpenAI API key. Required for OpenAI models and embeddings.
            anthropic_api_key (str, optional): Anthropic API key. Required for Claude models.
            google_api_key (str, optional): Google API key. Required for Gemini models.
            llm_model (str): The LLM model to use. Defaults to "gpt-3.5-turbo".
            embedding_model (str): The embedding model to use. Defaults to "text-embedding-ada-002".
            chunk_size (int): Size of text chunks for processing. Defaults to 1000.
            chunk_overlap (int): Overlap between chunks. Defaults to 200.
            similarity_threshold (float): Threshold for similarity matching. Defaults to 0.7.
            max_tokens (int): Maximum tokens for context. Defaults to 4000.
            temperature (float): Model temperature. Defaults to 0.7.
            top_k (int): Number of chunks to retrieve. Defaults to 5.
            
        Raises:
            ValueError: If required API keys are missing for the chosen models.
        """
        # Get required API keys for this combination
        required_keys = get_required_api_keys(llm_model, embedding_model)
        
        # Validate API keys
        missing_keys = []
        if "openai_api_key" in required_keys and not openai_api_key:
            missing_keys.append("openai_api_key")
        if "anthropic_api_key" in required_keys and not anthropic_api_key:
            missing_keys.append("anthropic_api_key")
        if "google_api_key" in required_keys and not google_api_key:
            missing_keys.append("google_api_key")
            
        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}\n"
                f"This model combination requires: {', '.join(required_keys)}"
            )
            
        # Get recommended models for guidance
        recommended_models = get_recommended_models()
        is_recommended = False
        for provider, models in recommended_models.items():
            if llm_model in models["llm_models"] and embedding_model in models["embedding_models"]:
                is_recommended = True
                break
                
        if not is_recommended:
            print(
                "Warning: Using a non-recommended model combination.\n"
                "For best results, consider using one of these recommended combinations:\n"
                f"{recommended_models}"
            )
            
        # Initialize model configuration
        self.model_config = ModelConfig(
            llm_model=llm_model,
            embedding_model=embedding_model,
            openai_api_key=openai_api_key,
            anthropic_api_key=anthropic_api_key,
            google_api_key=google_api_key,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            similarity_threshold=similarity_threshold,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k
        )
        
        # Initialize document store and other components
        self.documents = []
        self.vector_store = None
        self.retriever = None
        
    def load_document(self, file_path):
        """
        Load and process a document.
        
        Args:
            file_path (str): Path to the document file.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file type is not supported.
        """
        # Implementation remains the same
        pass
        
    def ask(self, question):
        """
        Ask a question about the loaded documents.
        
        Args:
            question (str): The question to ask.
            
        Returns:
            str: The answer to the question.
            
        Raises:
            ValueError: If no documents are loaded.
        """
        # Implementation remains the same
        pass 
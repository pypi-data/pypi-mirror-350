from pydantic import BaseModel
from typing import Optional

class ModelConfig(BaseModel):
    """Configuration for the RAG model, allowing user customization."""
    model_name: str = "gpt-4-vision-preview"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    chunk_size: int = 1000
    chunk_overlap: int = 200 
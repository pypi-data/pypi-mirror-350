from typing import Dict, List, Optional
from pydantic import BaseModel


class TokenUsage(BaseModel):
    """
    Token usage when generating the result of the prompt.
    """

    input_tokens: int
    completion_tokens: int
    total_tokens: int


class ModelMetadata(BaseModel):
    provider: str
    model: str
    parameters: Dict = {}


class Generation(BaseModel):
    """Container for generation output and metadata."""

    prompt: Optional[str] = None
    output: str
    retrieval_context: List[str] = []
    token_usage: TokenUsage
    metadata: Optional[ModelMetadata]

"""
TokenLens Tokenizers Module.

This module contains implementations of different tokenizers for various LLM models.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Token:
    """Represents a token from a tokenized text."""
    content: str
    start_position: int
    end_position: int


@dataclass
class TokenizeResult:
    """Result of tokenizing text."""
    total_tokens: int
    unique_tokens: int
    token_efficiency: float
    tokens: List[Token]


from .gpt_tokenizer import gpt_tokenizer
from .claude_tokenizer import claude_tokenizer
from .llama_tokenizer import llama_tokenizer
from .gemini_tokenizer import gemini_tokenizer
from .mistral_tokenizer import mistral_tokenizer
from .cohere_tokenizer import cohere_tokenizer

__all__ = [
    "Token", 
    "TokenizeResult", 
    "gpt_tokenizer", 
    "claude_tokenizer", 
    "llama_tokenizer",
    "gemini_tokenizer",
    "mistral_tokenizer",
    "cohere_tokenizer"
]
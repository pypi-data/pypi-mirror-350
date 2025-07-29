"""
GPT Tokenizer Implementation

This module provides tokenization functionality for GPT models using tiktoken.
"""

from typing import List, Optional
import re
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

from . import Token


def gpt_tokenizer(text: str, model_name: Optional[str] = None) -> List[Token]:
    """
    Tokenize text using GPT tokenization (via tiktoken if available).
    
    Args:
        text: The text to tokenize
        model_name: Optional specific GPT model name (e.g., "gpt-4", "gpt-3.5-turbo")
                    If not provided, uses "cl100k_base" encoding
    
    Returns:
        List of Token objects with content, start and end positions
    """
    if TIKTOKEN_AVAILABLE:
        return _tiktoken_tokenize(text, model_name)
    else:
        return _fallback_tokenize(text)


def _tiktoken_tokenize(text: str, model_name: Optional[str] = None) -> List[Token]:
    """Use tiktoken for accurate GPT tokenization."""
    # Get the appropriate encoding based on model name
    encoding_name = "cl100k_base"  # Default for gpt-4, gpt-3.5-turbo
    
    if model_name:
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # If model isn't recognized, use default encoding
            encoding = tiktoken.get_encoding(encoding_name)
    else:
        encoding = tiktoken.get_encoding(encoding_name)
    
    # Handle empty text case
    if not text:
        return []
        
    try:
        # Tokenize the text
        token_integers = encoding.encode(text)
        
        # Convert to Token objects with positions
        tokens = []
        cumulative_position = 0
        
        for token_int in token_integers:
            # Decode the token to get its string representation
            try:
                token_str = encoding.decode([token_int])
                
                # Find the token in the original text from the current position
                if token_str in text[cumulative_position:]:
                    start_pos = text.find(token_str, cumulative_position)
                    end_pos = start_pos + len(token_str)
                    
                    tokens.append(Token(
                        content=token_str,
                        start_position=start_pos,
                        end_position=end_pos
                    ))
                    
                    cumulative_position = end_pos
                else:
                    # For special tokens or whitespace handling edge cases
                    # This is a simplification that might not be 100% accurate
                    tokens.append(Token(
                        content=token_str,
                        start_position=cumulative_position,
                        end_position=cumulative_position + len(token_str)
                    ))
                    cumulative_position += len(token_str)
            except Exception:
                # If decoding a specific token fails, use a generic representation
                tokens.append(Token(
                    content=f"<token_{token_int}>",
                    start_position=cumulative_position,
                    end_position=cumulative_position + 1
                ))
                cumulative_position += 1
    except Exception:
        # If tiktoken encoding fails completely, fall back to our simpler method
        return _fallback_tokenize(text)
    
    return tokens


def _fallback_tokenize(text: str) -> List[Token]:
    """
    Fallback tokenization when tiktoken is not available.
    This is a simple approximation and not as accurate as tiktoken.
    """
    tokens = []
    position = 0
    
    # Simple regex pattern to split on whitespace, punctuation, and common boundaries
    pattern = r'(\s+|[.,!?;:\'"\(\)\[\]\{\}<>]|\w+)'
    
    for match in re.finditer(pattern, text):
        content = match.group(0)
        start_position = match.start()
        end_position = match.end()
        
        # Special handling for longer words - split them like GPT might
        if len(content) > 6 and re.match(r'\w+', content):
            # Split long words into smaller chunks of ~4 characters
            for i in range(0, len(content), 4):
                chunk = content[i:min(i+4, len(content))]
                tokens.append(Token(
                    content=chunk,
                    start_position=start_position + i,
                    end_position=start_position + i + len(chunk)
                ))
        else:
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
    
    return tokens
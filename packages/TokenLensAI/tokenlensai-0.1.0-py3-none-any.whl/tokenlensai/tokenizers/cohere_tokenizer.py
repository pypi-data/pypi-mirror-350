"""
Cohere Tokenizer Implementation

This module provides tokenization functionality for Cohere models.
"""

from typing import List
import re

from . import Token


def cohere_tokenizer(text: str) -> List[Token]:
    """
    Tokenize text using Cohere tokenization approximation.
    
    Note: This is an approximation since Cohere's tokenizer is not publicly available.
    For production use, you would integrate with Cohere's official tokenizer when available.
    
    Args:
        text: The text to tokenize
    
    Returns:
        List of Token objects with content, start and end positions
    """
    tokens = []
    
    # Cohere uses a BPE-based tokenizer with some custom rules
    # This is a simplified approximation
    
    # Basic tokenization heuristics
    position = 0
    
    # Simplified regex pattern for tokenization
    pattern = r'(\s+|[.,!?;:\'"\(\)\[\]\{\}<>]|\w+|\S+)'
    
    for match in re.finditer(pattern, text):
        content = match.group(0)
        start_position = match.start()
        end_position = match.end()
        
        # Handle different types of content
        if re.match(r'^\s+$', content):
            # Whitespace is usually kept as a single token
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
        elif re.match(r'^[.,!?;:\'"\(\)\[\]\{\}<>]$', content):
            # Punctuation marks are typically individual tokens
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
        elif re.match(r'^\d+$', content):
            # Numbers might be tokenized digit by digit or in small groups
            if len(content) <= 2:
                # Short numbers as a single token
                tokens.append(Token(
                    content=content,
                    start_position=start_position,
                    end_position=end_position
                ))
            else:
                # Longer numbers in groups of 2-3 digits
                i = 0
                while i < len(content):
                    group_size = min(3, len(content) - i)
                    tokens.append(Token(
                        content=content[i:i+group_size],
                        start_position=start_position + i,
                        end_position=start_position + i + group_size
                    ))
                    i += group_size
        elif re.match(r'^\w+$', content):
            # Word tokenization with BPE-like rules
            if len(content) <= 4:
                # Short words often stay as single tokens
                tokens.append(Token(
                    content=content,
                    start_position=start_position,
                    end_position=end_position
                ))
            else:
                # Apply BPE-like segmentation for longer words
                # This is a heuristic approximation
                
                # Cohere tends to handle common subwords effectively
                # so we'll try to mimic that behavior
                
                # Check for common word parts
                word_parts = []
                remaining = content
                
                # Common subwords that might be in Cohere's vocabulary
                prefixes = ["re", "un", "in", "dis", "pre", "post", "sub", "super", "anti"]
                suffixes = ["ing", "ed", "ly", "er", "est", "tion", "ment", "ness", "able", "ible"]
                
                # Check for prefix
                prefix_found = False
                for prefix in prefixes:
                    if remaining.lower().startswith(prefix) and len(remaining) > len(prefix) + 2:
                        word_parts.append(remaining[:len(prefix)])
                        remaining = remaining[len(prefix):]
                        prefix_found = True
                        break
                
                # Check for suffix
                suffix_found = False
                for suffix in suffixes:
                    if remaining.lower().endswith(suffix) and len(remaining) > len(suffix) + 2:
                        suffix_part = remaining[-len(suffix):]
                        remaining = remaining[:-len(suffix)]
                        suffix_found = True
                        break
                
                # Process the remaining part
                while remaining:
                    # Take chunks based on approximate syllable boundaries
                    # This is a very simplified approach
                    chunk_size = min(4, len(remaining))
                    word_parts.append(remaining[:chunk_size])
                    remaining = remaining[chunk_size:]
                
                # Add suffix if found
                if suffix_found:
                    word_parts.append(suffix_part)
                
                # Create tokens from word parts
                current_pos = 0
                for part in word_parts:
                    tokens.append(Token(
                        content=part,
                        start_position=start_position + current_pos,
                        end_position=start_position + current_pos + len(part)
                    ))
                    current_pos += len(part)
        else:
            # Other content as a single token
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
    
    return tokens
"""
Llama Tokenizer Implementation

This module provides tokenization functionality for Llama models.
"""

from typing import List
import re

from . import Token


def llama_tokenizer(text: str) -> List[Token]:
    """
    Tokenize text using Llama tokenization approximation.
    
    Note: This is an approximation since Meta's tokenizer may not be available.
    For production use, you would integrate with Meta's official tokenizer when available.
    
    Args:
        text: The text to tokenize
    
    Returns:
        List of Token objects with content, start and end positions
    """
    tokens = []
    
    # Llama's tokenizer is based on BPE (Byte-Pair Encoding)
    # This is a simplified approximation
    
    # Basic tokenization heuristics
    position = 0
    
    # Simplified regex pattern for tokenization
    pattern = r'(\s+|[.,!?;:\'"\(\)\[\]\{\}<>]|\w+|\S+)'
    
    for match in re.finditer(pattern, text):
        content = match.group(0)
        start_position = match.start()
        end_position = match.end()
        
        # Llama handles whitespace and special characters differently
        if re.match(r'^\s+$', content):
            # Keep whitespace as a single token
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
        # Special handling for longer words to mimic BPE tokenization
        elif len(content) > 4 and re.match(r'\w+', content):
            # Attempt to mimic BPE tokenization by breaking at common subword boundaries
            current_pos = 0
            remaining = content
            
            while remaining:
                # Split on frequent English prefixes and suffixes
                prefixes = ["un", "re", "in", "dis", "en", "non", "im", "il", "ir", "pre", "pro"]
                suffixes = ["ing", "ed", "s", "ly", "tion", "ment", "ness", "er", "est", "ity", "al"]
                
                # Check for prefixes
                prefix_match = None
                for prefix in prefixes:
                    if remaining.startswith(prefix) and len(remaining) > len(prefix):
                        prefix_match = prefix
                        break
                
                if prefix_match:
                    tokens.append(Token(
                        content=prefix_match,
                        start_position=start_position + current_pos,
                        end_position=start_position + current_pos + len(prefix_match)
                    ))
                    current_pos += len(prefix_match)
                    remaining = remaining[len(prefix_match):]
                    continue
                
                # Check for suffixes
                suffix_match = None
                for suffix in suffixes:
                    if remaining.endswith(suffix) and len(remaining) > len(suffix):
                        suffix_match = suffix
                        break
                
                if suffix_match:
                    # First tokenize the part before the suffix
                    before_suffix = remaining[:-len(suffix_match)]
                    tokens.append(Token(
                        content=before_suffix,
                        start_position=start_position + current_pos,
                        end_position=start_position + current_pos + len(before_suffix)
                    ))
                    current_pos += len(before_suffix)
                    
                    # Then tokenize the suffix
                    tokens.append(Token(
                        content=suffix_match,
                        start_position=start_position + current_pos,
                        end_position=start_position + current_pos + len(suffix_match)
                    ))
                    current_pos += len(suffix_match)
                    remaining = ""
                    continue
                
                # If no prefix/suffix matches, take a chunk based on length
                chunk_size = min(len(remaining), 3 + (len(remaining) % 2))
                chunk = remaining[:chunk_size]
                
                tokens.append(Token(
                    content=chunk,
                    start_position=start_position + current_pos,
                    end_position=start_position + current_pos + len(chunk)
                ))
                
                current_pos += len(chunk)
                remaining = remaining[chunk_size:]
        else:
            # Keep shorter words, numbers, and symbols intact
            tokens.append(Token(
                content=content,
                start_position=start_position,
                end_position=end_position
            ))
    
    return tokens
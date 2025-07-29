"""
Token Counter Agent

This agent is responsible for counting and analyzing tokens in text
using various tokenization methods.
"""

from typing import Dict, Any, Optional
from ..tokenizers import TokenizeResult


class TokenCounterAgent:
    """
    Agent responsible for token counting and basic token statistics.
    """
    
    def analyze_tokens(self, text: str, model_type: str, tokenize_fn) -> Dict[str, Any]:
        """
        Analyze tokens in the provided text using the specified model.
        
        Args:
            text: The text to analyze
            model_type: The model type to use
            tokenize_fn: Function to tokenize the text
            
        Returns:
            Dictionary with token analysis results
        """
        # Tokenize the text
        result = tokenize_fn(text, model_type)
        
        # Calculate statistics
        stats = self.calculate_token_statistics(result)
        
        # Combine results
        return {
            'total_tokens': result.total_tokens,
            'unique_tokens': result.unique_tokens,
            'token_efficiency': result.token_efficiency,
            'tokens': [
                {
                    'content': t.content,
                    'start_position': t.start_position,
                    'end_position': t.end_position
                }
                for t in result.tokens
            ],
            'statistics': stats,
            'model': model_type
        }
    
    def calculate_token_statistics(self, result: TokenizeResult) -> Dict[str, Any]:
        """
        Calculate additional statistics about tokenization results.
        
        Args:
            result: TokenizeResult from tokenization
            
        Returns:
            Dictionary with token statistics
        """
        tokens = result.tokens
        
        # Calculate average token length
        total_chars = sum(len(t.content) for t in tokens)
        avg_token_length = total_chars / len(tokens) if tokens else 0
        
        # Calculate distribution of token lengths
        token_lengths = [len(t.content) for t in tokens]
        length_distribution = {}
        for length in token_lengths:
            length_distribution[length] = length_distribution.get(length, 0) + 1
        
        # Calculate character efficiency (characters per token)
        char_efficiency = avg_token_length
        
        # Count whitespace tokens
        whitespace_tokens = sum(1 for t in tokens if t.content.isspace())
        whitespace_percentage = (whitespace_tokens / len(tokens)) * 100 if tokens else 0
        
        # Count punctuation tokens
        punctuation_chars = set('.,!?;:\'"`~@#$%^&*()-_=+[]{}\\|/<>')
        punctuation_tokens = sum(1 for t in tokens if all(c in punctuation_chars for c in t.content))
        punctuation_percentage = (punctuation_tokens / len(tokens)) * 100 if tokens else 0
        
        return {
            'avg_token_length': avg_token_length,
            'length_distribution': length_distribution,
            'char_efficiency': char_efficiency,
            'whitespace_tokens': whitespace_tokens,
            'whitespace_percentage': whitespace_percentage,
            'punctuation_tokens': punctuation_tokens,
            'punctuation_percentage': punctuation_percentage
        }
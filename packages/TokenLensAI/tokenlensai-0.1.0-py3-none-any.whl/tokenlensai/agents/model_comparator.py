"""
Model Comparator Agent

This agent is responsible for comparing tokenization results across
different LLM models and identifying differences.
"""

from typing import Dict, Any, List, Set, Tuple
from collections import defaultdict

from ..tokenizers import Token, TokenizeResult


class ModelComparatorAgent:
    """
    Agent responsible for comparing tokenization across different models.
    """
    
    def compare_models(self, text: str, model_types: List[str], tokenize_fn=None) -> Dict[str, Any]:
        """
        Compare tokenization of the same text across different models.
        
        Args:
            text: The text to compare
            model_types: List of model types to compare
            tokenize_fn: Function to tokenize text (if provided by TokenLens)
            
        Returns:
            Dictionary with comparison results
        """
        if len(model_types) < 2:
            return {
                'models': model_types,
                'token_counts': [0],
                'difference_percentages': [0],
                'difference_details': []
            }
        
        # Use the provided tokenize function
        # This is just a placeholder, the actual implementation would use the 
        # tokenize function from TokenLens or any provided function
        if tokenize_fn is None:
            return self._dummy_compare(text, model_types)
        
        tokens_by_model = {}
        token_counts = []
        
        # Tokenize text with each model
        for model in model_types:
            result = tokenize_fn(text, model)
            tokens_by_model[model] = result.tokens
            token_counts.append(result.total_tokens)
        
        # Calculate differences between models
        difference_details = self._find_tokenization_differences(text, tokens_by_model)
        
        # Calculate percentage differences relative to first model
        base_count = token_counts[0] if token_counts else 0
        difference_percentages = []
        
        for count in token_counts:
            if base_count == 0:
                difference_percentages.append(0)
            else:
                diff_pct = ((count - base_count) / base_count) * 100
                difference_percentages.append(round(diff_pct, 1))
        
        return {
            'models': model_types,
            'token_counts': token_counts,
            'difference_percentages': difference_percentages,
            'difference_details': difference_details
        }
    
    def _find_tokenization_differences(self, text: str, tokens_by_model: Dict[str, List[Token]]) -> List[Dict[str, Any]]:
        """
        Find specific differences in tokenization between models.
        
        Args:
            text: The original text
            tokens_by_model: Dictionary mapping model types to token lists
            
        Returns:
            List of differences with details
        """
        differences = []
        
        # Map to track positions that are tokenized differently
        position_differences = defaultdict(set)
        
        # Identify positions that are tokenized differently across models
        for model, tokens in tokens_by_model.items():
            for token in tokens:
                for pos in range(token.start_position, token.end_position):
                    position_differences[pos].add(model)
        
        # Find contiguous regions that are tokenized differently
        different_regions = []
        current_region = None
        
        for pos in sorted(position_differences.keys()):
            models_at_pos = position_differences[pos]
            
            # If not all models tokenize this position the same way
            if len(models_at_pos) < len(tokens_by_model):
                if current_region is None:
                    current_region = {'start': pos, 'end': pos + 1, 'models': models_at_pos}
                elif current_region['end'] == pos:
                    # Extend current region
                    current_region['end'] = pos + 1
                    current_region['models'] = current_region['models'].union(models_at_pos)
                else:
                    # Start a new region
                    different_regions.append(current_region)
                    current_region = {'start': pos, 'end': pos + 1, 'models': models_at_pos}
        
        if current_region is not None:
            different_regions.append(current_region)
        
        # For each different region, extract tokens from each model
        for region in different_regions:
            region_text = text[region['start']:region['end']]
            
            if not region_text.strip():
                continue  # Skip whitespace-only regions
            
            region_diff = {
                'text': region_text,
                'models': {},
                'position': (region['start'], region['end'])
            }
            
            for model, tokens in tokens_by_model.items():
                # Extract tokens that overlap with this region
                region_tokens = []
                
                for token in tokens:
                    # Check if token overlaps with the region
                    if (token.start_position < region['end'] and 
                        token.end_position > region['start']):
                        region_tokens.append(token.content)
                
                if region_tokens:
                    region_diff['models'][model] = region_tokens
            
            differences.append(region_diff)
        
        # Format the differences more nicely for the API
        formatted_differences = []
        for model in tokens_by_model.keys():
            model_diffs = []
            
            for diff in differences:
                if model in diff['models']:
                    model_diffs.append({
                        'text': diff['text'],
                        'tokenized_as': diff['models'][model]
                    })
            
            if model_diffs:
                formatted_differences.append({
                    'model': model,
                    'different_tokens': model_diffs
                })
        
        return formatted_differences
    
    def _dummy_compare(self, text: str, model_types: List[str]) -> Dict[str, Any]:
        """
        Dummy implementation for when no tokenize function is provided.
        This simulates differences between models for testing.
        
        Args:
            text: The text to analyze
            model_types: List of model types
            
        Returns:
            Simulated comparison result
        """
        # Simple character-count-based simulation
        token_counts = []
        char_count = len(text)
        
        # Simulate different token counts for different models
        for i, model in enumerate(model_types):
            if 'gpt' in model.lower():
                # GPT models: approx 1 token per 4 chars
                token_counts.append(char_count // 4 + (i % 2))
            elif 'claude' in model.lower():
                # Claude models: slightly different tokenization
                token_counts.append(char_count // 3.8 + (i % 3))
            elif 'llama' in model.lower():
                # Llama models: another tokenization pattern
                token_counts.append(char_count // 3.5 + (i % 2))
            else:
                # Generic fallback
                token_counts.append(char_count // 4)
        
        # Calculate percentage differences
        base_count = token_counts[0] if token_counts else 0
        difference_percentages = []
        
        for count in token_counts:
            if base_count == 0:
                difference_percentages.append(0)
            else:
                diff_pct = ((count - base_count) / base_count) * 100
                difference_percentages.append(round(diff_pct, 1))
        
        # Create dummy difference details
        dummy_differences = []
        for i, model in enumerate(model_types):
            diff_tokens = []
            
            # Add some example differences
            if i > 0:  # Skip first model (reference point)
                diff_tokens.append({
                    'text': 'example',
                    'tokenized_as': ['ex', 'ample'] if i % 2 == 0 else ['exa', 'mple']
                })
                
                if len(text) > 20:
                    sample_text = text[10:20]
                    diff_tokens.append({
                        'text': sample_text,
                        'tokenized_as': [sample_text[:3], sample_text[3:]] 
                                        if i % 2 == 0 else [sample_text]
                    })
            
            if diff_tokens:
                dummy_differences.append({
                    'model': model,
                    'different_tokens': diff_tokens
                })
        
        return {
            'models': model_types,
            'token_counts': token_counts,
            'difference_percentages': difference_percentages,
            'difference_details': dummy_differences
        }
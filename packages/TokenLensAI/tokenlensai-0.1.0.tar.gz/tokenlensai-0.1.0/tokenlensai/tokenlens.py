"""
TokenLens Core Implementation

This module provides the main TokenLens class, which coordinates all functionality
of the TokenLens library using an agentic AI architecture.
"""

from typing import Dict, List, Any, Optional, Union, Callable
import re
import os
from collections import Counter

from .tokenizers import (
    Token, TokenizeResult, 
    gpt_tokenizer, claude_tokenizer, llama_tokenizer,
    gemini_tokenizer, mistral_tokenizer, cohere_tokenizer
)

from .agents.token_counter import TokenCounterAgent
from .agents.text_processor import TextProcessorAgent
from .agents.model_comparator import ModelComparatorAgent
from .agents.coordinator import CoordinatorAgent
from .agents.results_aggregator import ResultsAggregatorAgent

from .config import load_config, get_model_config, get_available_models, get_model_aliases


class TokenLens:
    """
    TokenLens is an agentic AI-based library for token counting and analysis
    across multiple LLM standards.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a new TokenLens instance.
        
        Args:
            config: Optional configuration dictionary with the following keys:
                - default_model: Default model to use for tokenization
                - models: List of models to include in comparisons
                - debug: Whether to print debug information
                - api_keys: Dictionary mapping provider names to API keys
                - config_path: Path to custom models.yaml configuration
        """
        self._config = config or {}
        self._debug = self._config.get('debug', False)
        self._api_keys = self._config.get('api_keys', {})
        
        # Load model configurations
        config_path = self._config.get('config_path')
        self._model_config = load_config(config_path)
        self._model_aliases = get_model_aliases(self._model_config)
        
        # Set default model and model list
        self._default_model = self._config.get('default_model', 'gpt')
        self._models = self._config.get('models', ['gpt', 'claude', 'llama'])
        
        # Map of tokenizer functions by type
        self._tokenizer_map = {
            'gpt': gpt_tokenizer,
            'claude': claude_tokenizer,
            'llama': llama_tokenizer,
            'gemini': gemini_tokenizer,
            'mistral': mistral_tokenizer,
            'cohere': cohere_tokenizer
        }
        
        # Initialize the tokenizers dictionary with model-specific mappings
        self._tokenizers = {}
        self._initialize_tokenizers()
        
        # Initialize agents
        self._token_counter = TokenCounterAgent()
        self._text_processor = TextProcessorAgent()
        self._model_comparator = ModelComparatorAgent()
        self._results_aggregator = ResultsAggregatorAgent()
        self._coordinator = CoordinatorAgent(
            token_counter=self._token_counter,
            text_processor=self._text_processor,
            model_comparator=self._model_comparator,
            results_aggregator=self._results_aggregator
        )
    
    def _initialize_tokenizers(self):
        """Initialize tokenizers for all supported models."""
        available_models = get_available_models(self._model_config)
        
        # Add all models from the configuration
        for model_name, model_info in available_models.items():
            tokenizer_type = model_info.get('tokenizer')
            if tokenizer_type in self._tokenizer_map:
                self._tokenizers[model_name] = self._tokenizer_map[tokenizer_type]
        
        # Add models from aliases
        for alias, model_name in self._model_aliases.items():
            if model_name in self._tokenizers and alias not in self._tokenizers:
                self._tokenizers[alias] = self._tokenizers[model_name]
        
        # Add base tokenizer types directly
        for tokenizer_type, tokenizer_fn in self._tokenizer_map.items():
            if tokenizer_type not in self._tokenizers:
                self._tokenizers[tokenizer_type] = tokenizer_fn

    def tokenize_text(self, text: str, model_type: Optional[str] = None) -> TokenizeResult:
        """
        Tokenize text using the specified model's tokenizer.
        
        Args:
            text: The text to tokenize
            model_type: The model type to use (defaults to self._default_model)
            
        Returns:
            TokenizeResult object with tokenization results
        """
        # Handle None or empty text
        if text is None:
            text = ""
            
        # Convert non-string types to string
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception:
                text = ""
        
        model = model_type or self._default_model
        
        # Ensure model is a string (fixes the KeyError with None)
        if not isinstance(model, str):
            model = str(model)
            
        if model not in self._tokenizers:
            if self._debug:
                print(f"Warning: Unknown model '{model}', falling back to '{self._default_model}'")
            model = self._default_model
            
        # Get the appropriate tokenizer function
        tokenizer_fn = self._tokenizers.get(model, self._tokenizers.get(self._default_model))
        
        # Additional fallback if tokenizer still not found
        if tokenizer_fn is None:
            tokenizer_fn = self._tokenizer_map.get('gpt', lambda x: [])
        
        try:
            # Tokenize the text
            tokens = tokenizer_fn(text)
            
            # Handle case where tokenizer returns None
            if tokens is None:
                tokens = []
            
            # Calculate metrics
            total_tokens = len(tokens)
            unique_token_contents = set(t.content for t in tokens)
            unique_tokens = len(unique_token_contents)
            token_efficiency = unique_tokens / total_tokens if total_tokens > 0 else 0
            
            return TokenizeResult(
                total_tokens=total_tokens,
                unique_tokens=unique_tokens,
                token_efficiency=token_efficiency,
                tokens=tokens
            )
        except Exception:
            # Last-resort fallback that always returns something usable
            return TokenizeResult(
                total_tokens=0,
                unique_tokens=0,
                token_efficiency=0.0,
                tokens=[]
            )
    
    def count_tokens(self, text: str, model_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Count tokens in the provided text using the specified model.
        
        Args:
            text: The text to analyze
            model_type: The model type to use (defaults to self._default_model)
            
        Returns:
            Dictionary with token count and analysis
        """
        result = self.tokenize_text(text, model_type)
        model = model_type or self._default_model
        
        # Calculate estimated cost always, using fallback methods if needed
        estimated_cost = 0.0
        
        # Use hardcoded default values based on model name patterns
        base_rate = 0.002  # Default rate per 1K tokens
        
        # Apply model-specific default rates for better estimates even without config
        model_lower = model.lower()
        if 'gpt-4' in model_lower:
            base_rate = 0.03  # GPT-4 ~ $0.03 per 1K tokens
        elif 'gpt-3.5' in model_lower or 'gpt3.5' in model_lower:
            base_rate = 0.0015  # GPT-3.5 ~ $0.0015 per 1K tokens
        elif 'claude' in model_lower and 'opus' in model_lower:
            base_rate = 0.015  # Claude Opus ~ $0.015 per 1K tokens
        elif 'claude' in model_lower and 'sonnet' in model_lower:
            base_rate = 0.003  # Claude Sonnet ~ $0.003 per 1K tokens
        elif 'claude' in model_lower and 'haiku' in model_lower:
            base_rate = 0.00025  # Claude Haiku ~ $0.00025 per 1K tokens
        elif 'mistral' in model_lower and ('large' in model_lower or 'medium' in model_lower):
            base_rate = 0.007  # Mistral Large/Medium ~ $0.007 per 1K tokens
        elif 'gemini' in model_lower and 'pro' in model_lower:
            base_rate = 0.001  # Gemini Pro ~ $0.001 per 1K tokens
        
        # Try to get more specific pricing from config if available
        try:
            if hasattr(self, '_model_config') and self._model_config and 'models' in self._model_config:
                # Try exact model match
                model_data = self._model_config.get('models', {}).get(model, {})
                # If not found, try finding partial match
                if not model_data:
                    for cfg_model, cfg_data in self._model_config.get('models', {}).items():
                        if cfg_model in model or model in cfg_model:
                            model_data = cfg_data
                            break
                
                # If we found model data, extract price
                if model_data:
                    price_per_1k = model_data.get('price_per_1k_tokens', 
                                                model_data.get('input_cost_per_1k', base_rate))
                    base_rate = price_per_1k
        except Exception as e:
            # Silently continue with the default rate if there's an error
            if self._debug:
                print(f"Warning: Using default pricing due to error: {e}")
        
        # Calculate final cost
        estimated_cost = (result.total_tokens / 1000) * base_rate
        
        # Convert to dictionary format
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
            'model': model,
            'estimated_cost': estimated_cost  # Always included now
        }
    
    def analyze_text(self, text: str, model_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze text for token optimization opportunities.
        
        Args:
            text: The text to analyze
            model_type: The model type to use (defaults to self._default_model)
            
        Returns:
            Dictionary with optimization suggestions and metrics
        """
        # First tokenize the text
        token_result = self.tokenize_text(text, model_type)
        
        # Use the text processor agent to analyze the text
        return self._text_processor.process_text(text, token_result)
    
    def compare_models(self, text: str, model_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare tokenization across different models.
        
        Args:
            text: The text to compare
            model_types: List of model types to compare (defaults to self._models)
            
        Returns:
            Dictionary with comparison results
        """
        models = model_types or self._models
        
        # Ensure all models are valid
        valid_models = [m for m in models if m in self._tokenizers]
        if len(valid_models) < len(models):
            if self._debug:
                print(f"Warning: Some models were invalid and removed from comparison")
        
        if not valid_models:
            valid_models = [self._default_model]
        
        # Use the model comparator agent to compare models
        return self._model_comparator.compare_models(text, valid_models)
    
    def full_analysis(self, text: str, model_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run a full analysis using the coordinated agent approach.
        
        Args:
            text: The text to analyze
            model_types: List of model types to analyze (defaults to self._models)
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        models = model_types or self._models
        
        # Use the coordinator agent to orchestrate a complete analysis
        return self._coordinator.coordinate_analysis(text, models)
    
    @property
    def utils(self) -> Dict[str, Callable]:
        """
        Get utility functions for token analysis.
        
        Returns:
            Dictionary of utility functions
        """
        return {
            'find_most_common_tokens': self._find_most_common_tokens,
            'estimate_token_count': self._estimate_token_count,
            'highlight_inefficient_patterns': self._highlight_inefficient_patterns,
            'detect_repetition': self._detect_repetition
        }
    
    def _find_most_common_tokens(self, token_result: Union[TokenizeResult, Dict[str, Any]], n: int = 5) -> List[Dict[str, Any]]:
        """
        Find the most common tokens in a tokenization result.
        
        Args:
            token_result: The result from tokenize_text or count_tokens
            n: Number of top tokens to return
            
        Returns:
            List of dictionaries with token and count information
        """
        if isinstance(token_result, TokenizeResult):
            tokens = [t.content for t in token_result.tokens]
        else:
            tokens = [t['content'] for t in token_result.get('tokens', [])]
        
        counter = Counter(tokens)
        most_common = counter.most_common(n)
        
        return [{'token': token, 'count': count} for token, count in most_common]
    
    def _estimate_token_count(self, text: str) -> int:
        """
        Quickly estimate token count without full tokenization.
        
        This is a rough approximation based on common patterns.
        
        Args:
            text: The text to estimate
            
        Returns:
            Estimated token count
        """
        # A very simple estimation heuristic
        # Based on average English token length of ~4 characters
        # Adjusting for whitespace and punctuation
        
        # Count words
        words = len(re.findall(r'\b\w+\b', text))
        
        # Count punctuation and special characters
        punctuation = len(re.findall(r'[.,!?;:\'"\(\)\[\]\{\}<>]', text))
        
        # Count whitespace
        whitespace = len(re.findall(r'\s+', text))
        
        # Estimate total tokens (words are often split into multiple tokens)
        estimated_word_tokens = words * 1.3  # Empirical multiplier for subword tokenization
        
        return int(estimated_word_tokens + punctuation + whitespace)
    
    def _highlight_inefficient_patterns(self, text: str, model_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Identify patterns in text that are inefficient for tokenization.
        
        Args:
            text: The text to analyze
            model_type: The model type to consider
            
        Returns:
            List of inefficient patterns with explanations
        """
        inefficient_patterns = []
        
        # Check for repeated phrases (4+ words)
        repeated_phrases = re.findall(r'\b(\w+\s+\w+\s+\w+\s+\w+\s+\w+)(?=.*\1)', text)
        if repeated_phrases:
            inefficient_patterns.append({
                'pattern': 'repeated_phrases',
                'examples': list(set(repeated_phrases))[:3],
                'explanation': 'Repeated phrases consume unnecessary tokens'
            })
        
        # Check for very long identifiers
        long_identifiers = re.findall(r'\b[A-Za-z0-9_]{20,}\b', text)
        if long_identifiers:
            inefficient_patterns.append({
                'pattern': 'long_identifiers',
                'examples': list(set(long_identifiers))[:3],
                'explanation': 'Very long identifiers are tokenized inefficiently'
            })
        
        # Check for unusual character combinations 
        unusual_chars = re.findall(r'[^\w\s]{3,}', text)
        if unusual_chars:
            inefficient_patterns.append({
                'pattern': 'unusual_character_sequences',
                'examples': list(set(unusual_chars))[:3],
                'explanation': 'Unusual character sequences often use more tokens'
            })
        
        return inefficient_patterns
    
    def _detect_repetition(self, text: str) -> Dict[str, Any]:
        """
        Detect various forms of repetition in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with repetition analysis
        """
        # Word repetition
        words = re.findall(r'\b\w+\b', text.lower())
        word_counter = Counter(words)
        repeated_words = [word for word, count in word_counter.items() if count > 2 and len(word) > 3]
        
        # Phrase repetition (2+ words)
        phrases_2 = re.findall(r'\b(\w+\s+\w+)\b', text.lower())
        phrases_3 = re.findall(r'\b(\w+\s+\w+\s+\w+)\b', text.lower())
        
        phrase_counter_2 = Counter(phrases_2)
        phrase_counter_3 = Counter(phrases_3)
        
        repeated_phrases_2 = [phrase for phrase, count in phrase_counter_2.items() if count > 1]
        repeated_phrases_3 = [phrase for phrase, count in phrase_counter_3.items() if count > 1]
        
        return {
            'has_repetition': bool(repeated_words or repeated_phrases_2 or repeated_phrases_3),
            'repeated_words': repeated_words[:5],  # Top 5
            'repeated_phrases': {
                'bigrams': repeated_phrases_2[:3],  # Top 3
                'trigrams': repeated_phrases_3[:3]  # Top 3
            },
            'total_repetition_instances': len(repeated_words) + len(repeated_phrases_2) + len(repeated_phrases_3)
        }
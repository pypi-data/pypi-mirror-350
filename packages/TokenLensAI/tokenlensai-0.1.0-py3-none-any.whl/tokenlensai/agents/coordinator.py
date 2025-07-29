"""
Coordinator Agent

This agent is responsible for coordinating the activities of other agents
to produce a comprehensive token analysis.
"""

from typing import Dict, Any, List, Optional

from .token_counter import TokenCounterAgent
from .text_processor import TextProcessorAgent
from .model_comparator import ModelComparatorAgent
from .results_aggregator import ResultsAggregatorAgent


class CoordinatorAgent:
    """
    Agent responsible for coordinating the overall token analysis process.
    """
    
    def __init__(self,
                token_counter: TokenCounterAgent,
                text_processor: TextProcessorAgent,
                model_comparator: ModelComparatorAgent,
                results_aggregator: ResultsAggregatorAgent):
        """
        Initialize the coordinator agent with references to other agents.
        
        Args:
            token_counter: Agent for token counting
            text_processor: Agent for text processing and optimization
            model_comparator: Agent for comparing models
            results_aggregator: Agent for aggregating results
        """
        self._token_counter = token_counter
        self._text_processor = text_processor
        self._model_comparator = model_comparator
        self._results_aggregator = results_aggregator
    
    def coordinate_analysis(self, text: str, model_types: List[str], tokenize_fn=None) -> Dict[str, Any]:
        """
        Coordinate a complete analysis of the provided text.
        
        Args:
            text: The text to analyze
            model_types: List of model types to include
            tokenize_fn: Function to tokenize text (if provided by TokenLens)
            
        Returns:
            Comprehensive analysis results
        """
        # Placeholder for actual implementation that would use the tokenize_fn
        # Since the actual implementation depends on how TokenLens works, this is a stub
        
        # Step 1: Token counting for the primary model
        primary_model = model_types[0] if model_types else 'gpt'
        token_analysis = {
            'total_tokens': 0,
            'unique_tokens': 0,
            'token_efficiency': 0,
            'tokens': [],
            'statistics': {}
        }
        
        if tokenize_fn:
            # Real implementation would use tokenize_fn here
            try:
                token_result = tokenize_fn(text, primary_model)
                token_analysis = self._token_counter.analyze_tokens(text, primary_model, tokenize_fn)
            except Exception:
                # If tokenization fails, create a default token result
                token_result = None
                token_analysis = {
                    'total_tokens': 0,
                    'unique_tokens': 0,
                    'token_efficiency': 0,
                    'tokens': [],
                    'statistics': {}
                }
        
        # Step 2: Text processing for optimization
        # Define token_result to ensure it's always bound
        token_result = None
        if tokenize_fn:
            try:
                token_result = tokenize_fn(text, primary_model)
            except Exception:
                # If tokenization fails, token_result remains None
                pass
                
        # Pass token_result to the text processor
        processing_result = self._text_processor.process_text(text, token_result)
        
        # Step 3: Model comparison
        comparison_result = self._model_comparator.compare_models(text, model_types, tokenize_fn)
        
        # Step 4: Aggregate results
        aggregated_result = self._results_aggregator.aggregate_results(
            token_analysis, processing_result, comparison_result, model_types
        )
        
        return aggregated_result
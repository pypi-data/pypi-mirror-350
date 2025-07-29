"""
Results Aggregator Agent

This agent is responsible for aggregating results from other agents
and creating a comprehensive analysis report.
"""

from typing import Dict, Any, List
from ..tokenizers import TokenizeResult


class ResultsAggregatorAgent:
    """
    Agent responsible for aggregating and presenting analysis results.
    """
    
    def aggregate_results(self, 
                         token_analysis: Dict[str, Any],
                         processing_result: Dict[str, Any],
                         comparison_result: Dict[str, Any],
                         model_ids: List[str]) -> Dict[str, Any]:
        """
        Aggregate results from different analysis agents.
        
        Args:
            token_analysis: Results from token counter agent
            processing_result: Results from text processor agent
            comparison_result: Results from model comparator agent
            model_ids: List of model IDs used in the analysis
            
        Returns:
            Comprehensive aggregated analysis
        """
        # Generate a summary of the analysis
        summary = self._generate_summary(token_analysis, processing_result, comparison_result)
        
        # Prepare token breakdown by model
        token_breakdown = self._prepare_token_breakdown(comparison_result)
        
        # Compile optimization suggestions
        optimization_suggestions = processing_result.get('optimization_suggestions', [])
        
        # Create the aggregated result with optimization_suggestions at the top level
        return {
            'optimization_suggestions': optimization_suggestions,  # Make this accessible at the top level
            'token_reduction': processing_result.get('token_reduction', 0),
            'analysis': {
                'summary': summary,
                'total_tokens': token_analysis.get('total_tokens', 0),
                'token_breakdown': token_breakdown
            },
            'tokenization': {
                'tokens': token_analysis.get('tokens', []),
                'statistics': token_analysis.get('statistics', {})
            },
            'comparison': comparison_result,
            'models': comparison_result.get('models', []),
            'token_counts': comparison_result.get('token_counts', [])
        }
    
    def _generate_summary(self, 
                         token_analysis: Dict[str, Any],
                         processing_result: Dict[str, Any],
                         comparison_result: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the analysis results.
        
        Args:
            token_analysis: Results from token counter agent
            processing_result: Results from text processor agent
            comparison_result: Results from model comparator agent
            
        Returns:
            Summary text
        """
        total_tokens = token_analysis.get('total_tokens', 0)
        token_efficiency = token_analysis.get('token_efficiency', 0) * 100
        
        model_names = comparison_result.get('models', [])
        token_counts = comparison_result.get('token_counts', [])
        model_count = len(model_names)
        
        # Base summary with token count
        summary = f"Analysis of {total_tokens} tokens with {token_efficiency:.1f}% token efficiency."
        
        # Add model comparison info if available
        if model_count > 1 and len(token_counts) > 1:
            min_count = min(token_counts)
            max_count = max(token_counts)
            diff_percent = ((max_count - min_count) / min_count) * 100 if min_count > 0 else 0
            
            min_model = model_names[token_counts.index(min_count)]
            max_model = model_names[token_counts.index(max_count)]
            
            summary += f" Compared across {model_count} models: {min_model} used {min_count} tokens"
            
            if diff_percent > 1:  # Only mention if difference is notable
                summary += f" while {max_model} used {max_count} tokens ({diff_percent:.1f}% more)."
            else:
                summary += "."
        
        # Add optimization information if available
        token_reduction = processing_result.get('token_reduction', 0)
        if token_reduction > 0:
            summary += f" Potential token reduction of up to {token_reduction:.1f}% with optimizations."
        
        return summary
    
    def _prepare_token_breakdown(self, comparison_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prepare breakdown of tokens by model.
        
        Args:
            comparison_result: Results from model comparator agent
            
        Returns:
            List of dictionaries with model breakdown information
        """
        models = comparison_result.get('models', [])
        token_counts = comparison_result.get('token_counts', [])
        
        # Create the breakdown structure
        breakdown = []
        
        for i, model in enumerate(models):
            if i < len(token_counts):
                count = token_counts[i]
                
                # Calculate percentage relative to the first model
                percentage = 100.0
                if i > 0 and token_counts[0] > 0:
                    percentage = (count / token_counts[0]) * 100
                
                breakdown.append({
                    'model_id': i,
                    'model_name': model,
                    'token_count': count,
                    'percentage': round(percentage, 1)
                })
        
        return breakdown
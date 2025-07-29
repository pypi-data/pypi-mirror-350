"""
Text Processor Agent

This agent is responsible for analyzing text for optimization opportunities
and generating suggestions to improve token efficiency.
"""

import re
from typing import Dict, Any, List, Optional
from collections import Counter

from ..tokenizers import TokenizeResult


class TextProcessorAgent:
    """
    Agent responsible for text analysis and optimization suggestions.
    """
    
    def process_text(self, text: str, token_analysis: Optional[TokenizeResult] = None) -> Dict[str, Any]:
        """
        Process text to identify optimization opportunities.
        
        Args:
            text: The text to analyze
            token_analysis: Tokenization result (can be None)
            
        Returns:
            Dictionary with processing results including optimization suggestions
        """
        # Handle the case when token_analysis is None
        if token_analysis is None:
            # Create default suggestions without token analysis
            suggestions = [
                "Use abbreviations like 'LLM' instead of 'large language model'",
                "Remove filler words and phrases",
                "Use direct language instead of verbose constructions",
                "Combine related points to reduce redundancy",
                "Remove unnecessary explanatory text"
            ]
            
            # Default empty patterns when no token analysis is available
            efficient_patterns = []
            inefficient_patterns = []
        else:
            # Generate optimization suggestions with token analysis
            suggestions = self.generate_optimization_suggestions(text, token_analysis)
            
            # Identify efficient and inefficient patterns
            efficient_patterns = self.identify_efficient_patterns(token_analysis)
            inefficient_patterns = self.identify_inefficient_patterns(token_analysis)
        
        # Estimate potential token reduction
        token_reduction = self.estimate_token_reduction(text, suggestions)
        
        return {
            'optimization_suggestions': suggestions,
            'token_reduction': token_reduction,
            'efficient_patterns': efficient_patterns,
            'inefficient_patterns': inefficient_patterns
        }
    
    def generate_optimization_suggestions(self, text: str, token_analysis: Optional[TokenizeResult] = None) -> List[str]:
        """
        Generate suggestions for optimizing token usage.
        
        Args:
            text: The text to analyze
            token_analysis: Tokenization result (can be None)
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        # Safety check for text
        if not text:
            return ["Provide text content to analyze"]
        
        # Check for repeated phrases
        if self.has_repeated_phrases(text):
            suggestions.append(
                "Eliminate repeated phrases to reduce token count. "
                "Try rephrasing or referencing earlier statements."
            )
        
        # Check for verbose structures
        if self.has_verbose_structures(text):
            suggestions.append(
                "Simplify verbose language constructs. "
                "Use more direct phrasing and avoid unnecessary qualifiers."
            )
        
        # Check for long sequences of special characters
        if re.search(r'[^\w\s]{3,}', text):
            suggestions.append(
                "Consider simplifying sequences of special characters, "
                "which can tokenize inefficiently."
            )
        
        # Check for very long identifiers
        if re.search(r'\b[A-Za-z0-9_]{20,}\b', text):
            suggestions.append(
                "Break down very long identifiers into shorter ones. "
                "Long identifiers are often tokenized inefficiently."
            )
        
        # Checks that require token analysis
        if token_analysis:
            # Check for high token-to-character ratio (indicates inefficient tokenization)
            if hasattr(token_analysis, 'tokens') and len(token_analysis.tokens) > len(text) / 2:
                suggestions.append(
                    "Your text has a high token-to-character ratio. "
                    "Consider using more common English words and simpler phrasing."
                )
            
            # Check for low token efficiency (many repeated tokens)
            if hasattr(token_analysis, 'token_efficiency') and token_analysis.token_efficiency < 0.5:
                suggestions.append(
                    "Text contains many repeated tokens. "
                    "Try varying vocabulary for better token efficiency."
                )
        
        # Common optimization patterns that don't require token analysis
        if "large language model" in text.lower():
            suggestions.append("Replace \"large language model\" with \"LLM\"")
            
        if "artificial intelligence" in text.lower():
            suggestions.append("Replace \"artificial intelligence\" with \"AI\"")
        
        if "please provide" in text.lower():
            suggestions.append("Remove \"please provide\" and use direct requests")
        
        # Add general suggestions if we don't have many specific ones
        if len(suggestions) < 2:
            suggestions.append(
                "For general token efficiency, prefer common English words "
                "and avoid rare terms, abbreviations, or specialized notation."
            )
        
        return suggestions
    
    def has_repeated_phrases(self, text: str) -> bool:
        """
        Check if text contains repeated phrases.
        
        Args:
            text: The text to analyze
            
        Returns:
            True if repeated phrases are found, False otherwise
        """
        # Look for repeated sequences of 4+ words
        phrases = re.findall(r'\b(\w+\s+\w+\s+\w+\s+\w+)\b', text.lower())
        phrase_counter = Counter(phrases)
        
        return any(count > 1 for count in phrase_counter.values())
    
    def has_verbose_structures(self, text: str) -> bool:
        """
        Check if text contains verbose or redundant structures.
        
        Args:
            text: The text to analyze
            
        Returns:
            True if verbose structures are found, False otherwise
        """
        # Common verbose phrases
        verbose_patterns = [
            r'due to the fact that',
            r'in order to',
            r'for the purpose of',
            r'in the event that',
            r'in the process of',
            r'on the grounds that',
            r'with regard to',
            r'in the absence of',
            r'in the vicinity of',
            r'it should be noted that',
            r'it is important to note that',
            r'it is worth noting that',
            r'it goes without saying that'
        ]
        
        pattern = '|'.join(verbose_patterns)
        return bool(re.search(pattern, text.lower()))
    
    def estimate_token_reduction(self, text: str, suggestions: List[str]) -> float:
        """
        Estimate potential token reduction percentage if suggestions are applied.
        
        Args:
            text: The text to analyze
            suggestions: List of optimization suggestions
            
        Returns:
            Estimated token reduction percentage
        """
        # Base reduction estimate on number and types of suggestions
        base_reduction = 3.0 * len(suggestions)
        
        # Adjust based on specific suggestion types
        if any("repeated phrases" in s.lower() for s in suggestions):
            # Count repeated phrases for a more accurate estimate
            phrases = re.findall(r'\b(\w+\s+\w+\s+\w+\s+\w+)\b', text.lower())
            phrase_counter = Counter(phrases)
            repeated_phrases = sum(count - 1 for count in phrase_counter.values() if count > 1)
            
            # Estimate higher reduction for texts with many repeated phrases
            if repeated_phrases > 0:
                base_reduction += 2.0 * repeated_phrases
        
        if any("verbose" in s.lower() for s in suggestions):
            # Check for presence of common verbose phrases
            verbose_patterns = [
                r'due to the fact that', r'in order to', r'for the purpose of',
                r'in the event that', r'in the process of'
            ]
            
            verbose_count = sum(
                len(re.findall(pattern, text.lower())) 
                for pattern in verbose_patterns
            )
            
            if verbose_count > 0:
                base_reduction += 1.5 * verbose_count
        
        # Cap the reduction percentage at a reasonable value
        return min(base_reduction, 30.0)
    
    def identify_efficient_patterns(self, token_analysis: Optional[TokenizeResult] = None) -> List[str]:
        """
        Identify patterns in the text that tokenize efficiently.
        
        Args:
            token_analysis: Tokenization result (can be None)
            
        Returns:
            List of efficient patterns
        """
        efficient_patterns = []
        
        # If token_analysis is None, return empty list
        if token_analysis is None or not hasattr(token_analysis, 'tokens'):
            return efficient_patterns
        
        # Make sure tokens is not None and not empty
        if not token_analysis.tokens:
            return efficient_patterns
            
        # Calculate token content lengths
        token_lengths = [len(t.content) for t in token_analysis.tokens]
        
        # If no tokens, return empty list
        if not token_lengths:
            return efficient_patterns
            
        avg_length = sum(token_lengths) / len(token_lengths) if token_lengths else 0
        
        # Find tokens with above-average character length
        try:
            long_tokens = [
                t.content for t in token_analysis.tokens 
                if len(t.content) > avg_length * 1.5 and not t.content.isspace()
            ]
            
            # Count occurrences of each long token
            long_token_counter = Counter(long_tokens)
            
            # Identify the most efficient patterns (tokens that capture many characters)
            for token, count in long_token_counter.most_common(3):
                if len(token) > 4:  # Only consider significant tokens
                    efficient_patterns.append(token)
        except (AttributeError, TypeError):
            # If any errors occur, return empty list
            pass
        
        return efficient_patterns
    
    def identify_inefficient_patterns(self, token_analysis: Optional[TokenizeResult] = None) -> List[str]:
        """
        Identify patterns in the text that tokenize inefficiently.
        
        Args:
            token_analysis: Tokenization result (can be None)
            
        Returns:
            List of inefficient patterns
        """
        inefficient_patterns = []
        
        # If token_analysis is None, return empty list
        if token_analysis is None or not hasattr(token_analysis, 'tokens'):
            return inefficient_patterns
            
        # Make sure tokens is not None and not empty
        if not token_analysis.tokens:
            return inefficient_patterns
            
        try:
            # Find frequently occurring short tokens (excluding whitespace and common punctuation)
            short_tokens = [
                t.content for t in token_analysis.tokens 
                if 1 < len(t.content) < 3 and not t.content.isspace() 
                and not all(c in '.,!?;:\'"`' for c in t.content)
            ]
            
            # Count occurrences of each short token
            short_token_counter = Counter(short_tokens)
            
            # Identify the most inefficient patterns (short tokens that appear frequently)
            for token, count in short_token_counter.most_common(3):
                if count > 2:  # Only consider tokens that appear multiple times
                    inefficient_patterns.append(token)
        except (AttributeError, TypeError):
            # If any errors occur, return empty list
            pass
            
        return inefficient_patterns
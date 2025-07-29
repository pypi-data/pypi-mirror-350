"""
TokenLens Configuration Module

This module handles configuration loading and access for the TokenLens library.
"""

import os
import yaml
from typing import Dict, Any, Optional

# Default path to the models configuration file
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "models.yaml")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file. If None, uses the default.
        
    Returns:
        Configuration dictionary
    """
    path = config_path or DEFAULT_CONFIG_PATH
    
    try:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        # Return a minimal default configuration
        return {
            "models": {
                "gpt": {
                    "provider": "openai",
                    "tokenizer": "gpt",
                    "description": "GPT model fallback"
                },
                "claude": {
                    "provider": "anthropic",
                    "tokenizer": "claude",
                    "description": "Claude model fallback"
                },
                "llama": {
                    "provider": "meta",
                    "tokenizer": "llama",
                    "description": "Llama model fallback"
                }
            },
            "aliases": {
                "gpt": "gpt",
                "claude": "claude",
                "llama": "llama"
            }
        }


def get_model_config(model_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get configuration for a specific model.
    
    Args:
        model_name: Name of the model
        config: Optional configuration dictionary. If None, loads from file.
        
    Returns:
        Model configuration dictionary
    """
    if config is None:
        config = load_config()
    
    models = config.get("models", {})
    aliases = config.get("aliases", {})
    
    # Try to get the model directly
    if model_name in models:
        return models[model_name]
    
    # Check if it's an alias
    if model_name in aliases:
        aliased_name = aliases[model_name]
        if aliased_name in models:
            return models[aliased_name]
    
    # If model not found, use a simplified config based on tokenizer type
    if model_name in ["gpt", "gpt3", "gpt4", "davinci"]:
        return {
            "provider": "openai",
            "tokenizer": "gpt",
            "description": f"Generic {model_name} model"
        }
    elif model_name in ["claude", "anthropic"]:
        return {
            "provider": "anthropic",
            "tokenizer": "claude",
            "description": f"Generic {model_name} model"
        }
    elif model_name in ["llama", "meta"]:
        return {
            "provider": "meta",
            "tokenizer": "llama",
            "description": f"Generic {model_name} model"
        }
    elif model_name in ["gemini", "google"]:
        return {
            "provider": "google",
            "tokenizer": "gemini",
            "description": f"Generic {model_name} model"
        }
    elif model_name in ["mistral", "mixtral"]:
        return {
            "provider": "mistral",
            "tokenizer": "mistral",
            "description": f"Generic {model_name} model"
        }
    elif model_name in ["cohere", "command"]:
        return {
            "provider": "cohere",
            "tokenizer": "cohere",
            "description": f"Generic {model_name} model"
        }
    
    # Default fallback
    return {
        "provider": "generic",
        "tokenizer": "gpt",  # Default to GPT tokenizer
        "description": f"Unknown model: {model_name}"
    }


def get_available_models(config: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Get all available models from configuration.
    
    Args:
        config: Optional configuration dictionary. If None, loads from file.
        
    Returns:
        Dictionary of model configurations
    """
    if config is None:
        config = load_config()
    
    return config.get("models", {})


def get_model_aliases(config: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Get model aliases from configuration.
    
    Args:
        config: Optional configuration dictionary. If None, loads from file.
        
    Returns:
        Dictionary of model aliases
    """
    if config is None:
        config = load_config()
    
    return config.get("aliases", {})
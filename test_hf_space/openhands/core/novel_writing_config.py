"""
Novel Writing Mode Configuration for OpenHands
"""

from dataclasses import dataclass
from typing import Dict, Any
from openhands.core.config.llm_config import LLMConfig

@dataclass
class NovelWritingConfig:
    """Configuration for Novel Writing Mode"""
    
    # Model selection based on budget
    budget_model: str = "openrouter/anthropic/claude-3-haiku-20240307"  # Claude 3.5 Haiku for budget
    premium_model: str = "openrouter/anthropic/claude-3-opus-20240229"  # Claude 3 Opus for premium
    
    # Optimal parameters for creative writing
    temperature: float = 0.8
    max_output_tokens: int = 4000
    top_p: float = 0.9
    
    # OpenRouter specific settings
    openrouter_site_url: str = "https://docs.all-hands.dev/"
    openrouter_app_name: str = "OpenHands-NovelWriting"

def create_novel_writing_llm_config(
    base_config: LLMConfig, 
    is_premium: bool = False,
    api_key: str | None = None
) -> LLMConfig:
    """
    Create an LLM config optimized for novel writing mode.
    
    Args:
        base_config: Base LLM configuration
        is_premium: Whether to use premium model (Claude Opus) or budget model (Claude Haiku)
        api_key: OpenRouter API key (will be handled as SecretStr)
    
    Returns:
        LLMConfig optimized for creative writing
    """
    from pydantic import SecretStr
    import os
    
    novel_config = NovelWritingConfig()
    
    # Create a copy of base config
    config_dict = base_config.model_dump()
    
    # Override with novel writing specific settings
    config_dict.update({
        "model": novel_config.premium_model if is_premium else novel_config.budget_model,
        "temperature": novel_config.temperature,
        "max_output_tokens": novel_config.max_output_tokens,
        "top_p": novel_config.top_p,
        "openrouter_site_url": novel_config.openrouter_site_url,
        "openrouter_app_name": novel_config.openrouter_app_name,
    })
    
    # Handle API key as SecretStr for security
    if api_key:
        config_dict["api_key"] = SecretStr(api_key)
    elif not config_dict.get("api_key"):
        # Fallback to environment variable
        env_api_key = os.environ.get('OPENROUTER_API_KEY') or os.environ.get('LLM_API_KEY')
        if env_api_key:
            config_dict["api_key"] = SecretStr(env_api_key)
    
    # Ensure we're using OpenRouter
    if not config_dict.get("base_url"):
        config_dict["base_url"] = "https://openrouter.ai/api/v1"
    
    # Remove any None values to avoid validation errors
    config_dict = {k: v for k, v in config_dict.items() if v is not None}
    
    return LLMConfig(**config_dict)

def get_novel_writing_model_info(is_premium: bool = False) -> Dict[str, Any]:
    """
    Get information about the model being used for novel writing.
    
    Args:
        is_premium: Whether using premium model
        
    Returns:
        Dictionary with model information
    """
    novel_config = NovelWritingConfig()
    
    if is_premium:
        return {
            "model": novel_config.premium_model,
            "name": "Claude 3 Opus",
            "provider": "Anthropic via OpenRouter",
            "tier": "Premium",
            "strengths": ["Highest quality creative writing", "Complex reasoning", "Nuanced character development"],
            "cost": "Higher cost per token",
            "recommended_for": ["Professional writing", "Complex narratives", "Literary fiction"]
        }
    else:
        return {
            "model": novel_config.budget_model,
            "name": "Claude 3.5 Haiku",
            "provider": "Anthropic via OpenRouter", 
            "tier": "Budget",
            "strengths": ["Fast responses", "Good creative writing", "Cost effective"],
            "cost": "Lower cost per token",
            "recommended_for": ["Draft writing", "Brainstorming", "Quick feedback"]
        }

def should_use_premium_model(template_used: str | None = None, content_length: int = 0) -> bool:
    """
    Determine whether to use premium model based on template and content complexity.
    
    Args:
        template_used: The template being used
        content_length: Length of the content being processed
        
    Returns:
        Boolean indicating whether to use premium model
    """
    import os
    
    # Get configurable thresholds from environment variables
    content_threshold = int(os.environ.get('NOVEL_PREMIUM_CONTENT_THRESHOLD', '1500'))
    
    # Define template complexity levels
    template_complexity = {
        'character-development': 1,
        'dialogue-writing': 1,
        'plot-structure': 2,
        'world-building': 2,
        'style-voice': 3,
        'theme-symbolism': 3,
        'editing-revision': 3,
    }
    
    # Get premium template threshold from environment
    premium_complexity_threshold = int(os.environ.get('NOVEL_PREMIUM_COMPLEXITY_THRESHOLD', '3'))
    
    # Check content length threshold
    if content_length > content_threshold:
        return True
        
    # Check template complexity
    if template_used and template_used in template_complexity:
        complexity = template_complexity[template_used]
        if complexity >= premium_complexity_threshold:
            return True
    
    # Force premium mode if environment variable is set
    if os.environ.get('NOVEL_FORCE_PREMIUM_MODE', '').lower() == 'true':
        return True
        
    return False
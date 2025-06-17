"""
Hugging Face Spaces specific routes for debugging and monitoring
"""
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse

app = APIRouter(prefix='/api/hf', tags=['hf-spaces'])


@app.get('/status')
async def hf_spaces_status():
    """Get HF Spaces specific status and configuration"""
    return JSONResponse({
        'status': 'running',
        'environment': 'huggingface-spaces',
        'storage_type': {
            'settings': os.getenv('SETTINGS_STORE_TYPE', 'file'),
            'secrets': os.getenv('SECRETS_STORE_TYPE', 'file')
        },
        'default_config': {
            'llm_model': os.getenv('DEFAULT_LLM_MODEL'),
            'llm_base_url': os.getenv('DEFAULT_LLM_BASE_URL'),
            'agent': os.getenv('DEFAULT_AGENT'),
            'language': os.getenv('DEFAULT_LANGUAGE'),
            'max_iterations': os.getenv('MAX_ITERATIONS'),
            'max_budget': os.getenv('MAX_BUDGET_PER_TASK')
        },
        'security': {
            'auth_disabled': os.getenv('OPENHANDS_DISABLE_AUTH'),
            'security_disabled': os.getenv('DISABLE_SECURITY'),
            'auto_lint_disabled': os.getenv('ENABLE_AUTO_LINT') == 'false'
        },
        'api_key_configured': bool(os.getenv('OPENROUTER_API_KEY')),
        'skip_settings_modal': os.getenv('SKIP_SETTINGS_MODAL') == 'true'
    })


@app.get('/environment')
async def hf_spaces_environment():
    """Get environment variables (safe ones only)"""
    safe_env_vars = [
        'OPENHANDS_RUNTIME',
        'CORS_ALLOWED_ORIGINS',
        'SERVE_FRONTEND',
        'FILE_STORE_PATH',
        'CACHE_DIR',
        'SETTINGS_STORE_TYPE',
        'SECRETS_STORE_TYPE',
        'DEFAULT_LLM_MODEL',
        'DEFAULT_LLM_BASE_URL',
        'DEFAULT_AGENT',
        'DEFAULT_LANGUAGE',
        'CONFIRMATION_MODE',
        'ENABLE_AUTO_LINT',
        'MAX_ITERATIONS',
        'MAX_BUDGET_PER_TASK',
        'SKIP_SETTINGS_MODAL',
        'OPENHANDS_DISABLE_AUTH',
        'DISABLE_SECURITY'
    ]
    
    env_info = {}
    for var in safe_env_vars:
        env_info[var] = os.getenv(var, 'not_set')
    
    return JSONResponse({
        'environment_variables': env_info,
        'total_env_vars': len(os.environ),
        'safe_vars_shown': len(safe_env_vars)
    })


@app.get('/ready')
async def hf_spaces_ready():
    """Check if the system is ready for chat"""
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    settings_store_type = os.getenv('SETTINGS_STORE_TYPE')
    
    ready = bool(openrouter_key and settings_store_type == 'memory')
    
    return JSONResponse({
        'ready': ready,
        'can_skip_setup': ready,
        'reasons': {
            'api_key_configured': bool(openrouter_key),
            'memory_storage_enabled': settings_store_type == 'memory',
            'auth_disabled': os.getenv('OPENHANDS_DISABLE_AUTH') == 'true'
        },
        'next_steps': [
            'Add OPENROUTER_API_KEY to environment' if not openrouter_key else 'API key configured ✓',
            'Memory storage enabled ✓' if settings_store_type == 'memory' else 'Enable memory storage',
            'Ready to chat! 🎉' if ready else 'Complete setup to start chatting'
        ]
    })
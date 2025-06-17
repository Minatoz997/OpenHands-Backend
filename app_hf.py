"""
OpenHands Backend optimized for Hugging Face Spaces deployment
"""
import os
import secrets
import tempfile
import uvicorn

# Configure for Hugging Face Spaces BEFORE importing app
def setup_hf_environment():
    """Setup environment variables for Hugging Face Spaces"""
    
    # Set default environment variables for HF Spaces
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    os.environ.setdefault("SERVE_FRONTEND", "false")
    
    # Create writable directories
    file_store_path = "/tmp/openhands"
    cache_dir = "/tmp/cache"
    
    # Ensure directories exist with proper permissions
    os.makedirs(file_store_path, mode=0o755, exist_ok=True)
    os.makedirs(cache_dir, mode=0o755, exist_ok=True)
    
    # Set file store path to a writable directory in HF Spaces
    os.environ.setdefault("FILE_STORE_PATH", file_store_path)
    
    # Set cache directory to a writable location
    os.environ.setdefault("CACHE_DIR", cache_dir)
    
    # Generate JWT secret if not provided (for HF Spaces)
    if not os.getenv("JWT_SECRET"):
        jwt_secret = secrets.token_urlsafe(32)
        os.environ["JWT_SECRET"] = jwt_secret
        print(f"🔐 Generated JWT secret for session")
    
    # Set other HF-specific configs
    os.environ.setdefault("DISABLE_SECURITY", "true")  # For public API
    os.environ.setdefault("SANDBOX_RUNTIME_CONTAINER_IMAGE", "")  # Disable Docker
    os.environ.setdefault("SANDBOX_USER_ID", "1000")
    os.environ.setdefault("WORKSPACE_BASE", "/tmp/workspace")
    
    # Additional security bypass for HF Spaces
    os.environ.setdefault("OPENHANDS_DISABLE_AUTH", "true")
    os.environ.setdefault("ENABLE_AUTO_LINT", "false")
    os.environ.setdefault("ENABLE_SECURITY_ANALYSIS", "false")
    
    # Use memory-based storage for read-only environments
    os.environ.setdefault("SETTINGS_STORE_TYPE", "memory")
    os.environ.setdefault("SECRETS_STORE_TYPE", "memory")
    
    # Pre-configure default LLM settings for easy access
    os.environ.setdefault("DEFAULT_LLM_MODEL", "openrouter/anthropic/claude-3-haiku-20240307")
    os.environ.setdefault("DEFAULT_LLM_BASE_URL", "https://openrouter.ai/api/v1")
    os.environ.setdefault("SKIP_SETTINGS_MODAL", "true")  # Skip setup wizard if API key available
    
    # Enhanced user experience settings
    os.environ.setdefault("DEFAULT_AGENT", "CodeActAgent")
    os.environ.setdefault("DEFAULT_LANGUAGE", "en")
    os.environ.setdefault("CONFIRMATION_MODE", "false")
    os.environ.setdefault("ENABLE_AUTO_LINT", "false")
    
    # Performance optimizations for HF Spaces
    os.environ.setdefault("MAX_ITERATIONS", "30")  # Reasonable limit for public usage
    os.environ.setdefault("MAX_BUDGET_PER_TASK", "10.0")  # Cost control
    
    # Create workspace directory
    workspace_dir = "/tmp/workspace"
    os.makedirs(workspace_dir, mode=0o755, exist_ok=True)
    
    return file_store_path, cache_dir

if __name__ == "__main__":
    # Setup environment before importing anything
    file_store_path, cache_dir = setup_hf_environment()
    
    # Now import the app after environment is configured
    from openhands.server.app import app
    
    # Hugging Face Spaces specific configuration
    port = int(os.getenv("PORT", 7860))  # HF Spaces default port
    host = "0.0.0.0"
    
    print("🤗 Starting OpenHands Backend for Hugging Face Spaces")
    print(f"🚀 Server will run on {host}:{port}")
    print(f"🔧 Runtime: {os.getenv('OPENHANDS_RUNTIME')}")
    print(f"🌐 CORS: {os.getenv('CORS_ALLOWED_ORIGINS')}")
    print(f"📁 File Store: {file_store_path}")
    print(f"💾 Cache Dir: {cache_dir}")
    print(f"🔑 LLM API Key: {'✅ Set' if os.getenv('LLM_API_KEY') else '❌ Missing'}")
    print(f"🔐 JWT Secret: {'✅ Set' if os.getenv('JWT_SECRET') else '❌ Missing'}")
    print(f"🛡️ Security Disabled: {os.getenv('DISABLE_SECURITY')}")
    print(f"🔓 Auth Disabled: {os.getenv('OPENHANDS_DISABLE_AUTH')}")
    print("📡 API Endpoints:")
    print("   GET  /health")
    print("   GET  /api/options/config")
    print("   POST /api/conversations") 
    print("🌍 Ready for frontend integration!")
    
    # Debug environment
    print("\n🔍 Debug Info:")
    print(f"   LLM_MODEL: {os.getenv('LLM_MODEL', 'Not set')}")
    print(f"   LLM_BASE_URL: {os.getenv('LLM_BASE_URL', 'Not set')}")
    print(f"   WORKSPACE_BASE: {os.getenv('WORKSPACE_BASE', 'Not set')}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
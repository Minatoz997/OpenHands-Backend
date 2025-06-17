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
    print("📡 API Endpoints:")
    print("   GET  /api/options/config")
    print("   POST /api/conversations") 
    print("   GET  /health")
    print("🌍 Ready for frontend integration!")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
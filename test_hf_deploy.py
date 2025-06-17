#!/usr/bin/env python3
"""
Script untuk testing deployment ke Hugging Face Space secara lokal
"""
import os
import shutil
import subprocess
from pathlib import Path

def test_file_preparation():
    """Test apakah semua file yang diperlukan ada"""
    print("🔍 Checking required files...")
    
    required_files = [
        "openhands/",
        "app_hf.py",
        "requirements.txt", 
        "Dockerfile_HF",
        "README_HF.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files found!")
    return True

def simulate_workflow():
    """Simulate workflow file preparation"""
    print("\n🚀 Simulating workflow file preparation...")
    
    # Create temporary directory
    hf_space_dir = Path("./test_hf_space")
    if hf_space_dir.exists():
        shutil.rmtree(hf_space_dir)
    hf_space_dir.mkdir()
    
    try:
        # Copy files as workflow would do
        print("📁 Copying openhands folder...")
        shutil.copytree("./openhands", hf_space_dir / "openhands")
        
        print("📄 Copying app files...")
        shutil.copy2("./app_hf.py", hf_space_dir / "app_hf.py")
        shutil.copy2("./app_hf.py", hf_space_dir / "app.py")  # Entry point
        
        print("📋 Copying requirements...")
        shutil.copy2("./requirements.txt", hf_space_dir / "requirements.txt")
        
        print("🐳 Copying Dockerfile...")
        shutil.copy2("./Dockerfile_HF", hf_space_dir / "Dockerfile")
        
        # Create README with metadata
        print("📖 Creating README with metadata...")
        readme_content = """---
title: OpenHands Backend API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

"""
        with open("README_HF.md", "r") as f:
            readme_content += f.read()
        
        with open(hf_space_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        # Copy .env if exists
        if os.path.exists(".env.hf"):
            print("⚙️ Copying environment template...")
            shutil.copy2(".env.hf", hf_space_dir / ".env")
        
        print(f"\n📊 Files prepared in {hf_space_dir}:")
        for item in sorted(hf_space_dir.rglob("*")):
            if item.is_file():
                size = item.stat().st_size
                print(f"  {item.relative_to(hf_space_dir)} ({size} bytes)")
        
        print(f"\n✅ Simulation completed! Check {hf_space_dir} directory")
        return True
        
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        return False

def check_hf_token():
    """Check if HF_TOKEN is available"""
    print("\n🔑 Checking Hugging Face token...")
    
    token = os.getenv("HF_TOKEN")
    if not token:
        print("⚠️ HF_TOKEN not found in environment variables")
        print("   For actual deployment, set this in GitHub Secrets")
        return False
    
    print("✅ HF_TOKEN found!")
    return True

def test_app_startup():
    """Test if app_hf.py can be imported without errors"""
    print("\n🧪 Testing app startup configuration...")
    
    try:
        # Test environment setup function
        import sys
        sys.path.insert(0, '.')
        
        # Import the setup function
        from app_hf import setup_hf_environment
        
        # Test the setup
        file_store_path, cache_dir = setup_hf_environment()
        
        print(f"✅ Environment setup successful")
        print(f"   File store: {file_store_path}")
        print(f"   Cache dir: {cache_dir}")
        print(f"   JWT Secret: {'✅ Set' if os.getenv('JWT_SECRET') else '❌ Missing'}")
        
        # Check if directories were created
        if os.path.exists(file_store_path) and os.path.exists(cache_dir):
            print("✅ Directories created successfully")
        else:
            print("❌ Directory creation failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

def main():
    print("🧪 Testing Hugging Face Space Deployment Setup\n")
    
    # Test file preparation
    if not test_file_preparation():
        print("\n❌ File preparation test failed!")
        return
    
    # Test app startup configuration
    if not test_app_startup():
        print("\n❌ App startup test failed!")
        return
    
    # Simulate workflow
    if not simulate_workflow():
        print("\n❌ Workflow simulation failed!")
        return
    
    # Check token (optional for testing)
    check_hf_token()
    
    print("\n🎉 All tests passed!")
    print("\n📝 Next steps:")
    print("1. Set HF_TOKEN in GitHub repository secrets")
    print("2. Set LLM_API_KEY in HF Space environment variables")
    print("3. Push changes to main branch to trigger auto-deploy")
    print("4. Or run workflow manually from GitHub Actions tab")
    print("\n💡 JWT Secret will be auto-generated, no need to set manually!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Deploy to HF Spaces with automatic restart
"""
import os
import sys
import argparse
import requests
from huggingface_hub import HfApi, upload_file
import time

def restart_space(space_name, token):
    """Force restart HF Space"""
    try:
        print(f"🔄 Restarting HF Space: {space_name}")
        
        # Use HF API to restart space
        api = HfApi(token=token)
        api.restart_space(repo_id=space_name)
        
        print(f"✅ Space restart triggered successfully!")
        print(f"⏱️  Space will restart in 30-60 seconds")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not restart space automatically: {e}")
        print(f"🔧 Manual restart: https://huggingface.co/spaces/{space_name}/settings")
        return False

def deploy_to_hf_spaces(space_name, token=None):
    """Deploy files to HF Spaces"""
    
    if not token:
        token = os.getenv('HF_TOKEN')
    
    if not token:
        print("❌ Error: HF_TOKEN not found!")
        print("Set HF_TOKEN environment variable or pass --token")
        return False
    
    try:
        print(f"🚀 Starting deployment to {space_name}")
        
        # Initialize HF API
        api = HfApi(token=token)
        
        # Files to deploy
        files_to_deploy = [
            'app.py',
            'requirements.txt', 
            'Dockerfile',
            'README.md'
        ]
        
        # Check if files exist
        missing_files = []
        for file in files_to_deploy:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        
        # Upload each file with overwrite to avoid duplicates
        for file in files_to_deploy:
            print(f"📤 Uploading {file}...")
            try:
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=space_name,
                    repo_type="space",
                    token=token
                )
                print(f"✅ {file} uploaded successfully")
            except Exception as e:
                print(f"❌ Failed to upload {file}: {e}")
                return False
        
        print(f"🎉 All files uploaded successfully!")
        
        # Force restart the space
        restart_success = restart_space(space_name, token)
        
        if restart_success:
            print(f"🔄 Space is restarting with new files...")
            print(f"⏱️  Wait 2-3 minutes for restart to complete")
        else:
            print(f"⚠️  Please manually restart the space:")
            print(f"🔧 Go to: https://huggingface.co/spaces/{space_name}/settings")
            print(f"🔄 Click 'Restart this Space' button")
        
        print(f"")
        print(f"🌐 Your space: https://huggingface.co/spaces/{space_name}")
        print(f"📊 Logs: https://huggingface.co/spaces/{space_name}?logs=container")
        print(f"🔗 App URL: https://{space_name.replace('/', '-').lower()}.hf.space/health")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Deploy to HF Spaces with restart')
    parser.add_argument('--space-name', required=True, help='HF Space name (e.g., username/space-name)')
    parser.add_argument('--token', help='HF Token (optional, uses HF_TOKEN env var)')
    
    args = parser.parse_args()
    
    success = deploy_to_hf_spaces(args.space_name, args.token)
    
    if not success:
        sys.exit(1)
    
    print(f"✅ Deployment completed successfully!")

if __name__ == "__main__":
    main()
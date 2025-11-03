#!/usr/bin/env python3
"""
Simple script to test the backend API without the Android app.
"""

import requests
import sys

def test_backend_health():
    """Test if the backend is running."""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("   Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_upload_sample(file_path):
    """Test uploading a file to the backend."""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            response = requests.post("http://localhost:8000/upload", files=files)
            
            if response.status_code == 200:
                print("✅ Upload successful!")
                result = response.json()
                print(f"\n📊 Recommendation: {result.get('recommendation')}")
                print(f"🎯 Confidence: {result.get('confidence')}")
                print(f"\n💭 Reasoning:\n{result.get('reasoning')}")
                print(f"\n📋 Suggested Actions:")
                for i, action in enumerate(result.get('suggested_actions', []), 1):
                    print(f"   {i}. {action}")
                return True
            else:
                print(f"❌ Upload failed with status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing MedDiagnose Backend API\n")
    
    # Test health endpoint
    if not test_backend_health():
        sys.exit(1)
    
    print()
    
    # Test upload if file path provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"📤 Testing upload with file: {file_path}\n")
        test_upload_sample(file_path)
    else:
        print("ℹ️  To test file upload, provide a file path:")
        print("   python test_backend.py /path/to/test/file.pdf")


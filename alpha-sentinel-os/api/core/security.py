# Security and Key Management
import os

def validate_api_key(key):
    return key == os.environ.get("API_SECRET_KEY")

"""
Example: Configuration and Authentication
"""

import os
from voyado import VoyadoClient
from voyado.exceptions import VoyadoAuthenticationError, VoyadoAPIError

# Method 1: Direct configuration
print("Method 1: Direct configuration")
client = VoyadoClient(
    api_key="your-api-key-here",
    base_url="https://your-instance.voyado.com",
    user_agent="MyApp/1.0"
)

# Method 2: Using environment variables (recommended)
print("\nMethod 2: Using environment variables")
# Set these in your environment:
# export VOYADO_API_KEY="your-api-key"
# export VOYADO_BASE_URL="https://your-instance.voyado.com"

api_key = os.getenv('VOYADO_API_KEY')
base_url = os.getenv('VOYADO_BASE_URL')

if api_key and base_url:
    client = VoyadoClient(
        api_key=api_key,
        base_url=base_url,
        user_agent="MyApp/1.0"
    )
    print("✓ Client configured from environment variables")
else:
    print("✗ Missing environment variables")

# Method 3: Using a configuration file
print("\nMethod 3: Using configuration file")
try:
    # You could use python-dotenv or similar
    from dotenv import load_dotenv
    load_dotenv('.env')  # Load from .env file
    
    client = VoyadoClient(
        api_key=os.getenv('VOYADO_API_KEY'),
        base_url=os.getenv('VOYADO_BASE_URL'),
        user_agent=os.getenv('VOYADO_USER_AGENT', 'MyApp/1.0')
    )
    print("✓ Client configured from .env file")
except ImportError:
    print("⚠ python-dotenv not installed")

# Testing the connection
print("\nTesting API connection...")
try:
    if client.test_connection():
        print("✓ API connection successful!")
        
        # Get some basic information
        contact_count = client.contacts.get_count()
        print(f"  Total contacts: {contact_count}")
        
except VoyadoAuthenticationError as e:
    print(f"✗ Authentication failed: {e}")
    print("  Check your API key")
except VoyadoAPIError as e:
    print(f"✗ API error: {e}")
    print(f"  Status code: {e.status_code}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Example .env file content:
print("\nExample .env file:")
print("---")
print("VOYADO_API_KEY=your-api-key-here")
print("VOYADO_BASE_URL=https://your-instance.voyado.com")
print("VOYADO_USER_AGENT=MyApp/1.0")
print("---")

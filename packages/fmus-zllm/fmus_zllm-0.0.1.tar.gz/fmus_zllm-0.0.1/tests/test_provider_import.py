import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add the current directory to the path
sys.path.insert(0, os.path.abspath('.'))

from zllm.providers import get_provider_class, get_provider

# Print available providers
providers = get_provider_class()
print(f"Available providers: {list(providers.keys())}")

# Try to get the groq provider
try:
    groq_provider = get_provider("groq")
    print(f"Successfully loaded groq provider: {groq_provider}")
except Exception as e:
    print(f"Error loading groq provider: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

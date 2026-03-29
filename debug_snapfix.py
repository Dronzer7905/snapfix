import snapfix
import os
from pathlib import Path
from snapfix.config import load_config
from snapfix.llm.handler import LLMHandler

print(f"--- SNAPFIX DIAGNOSTICS ---")
print(f"Module file: {snapfix.__file__}")
print(f"CWD: {os.getcwd()}")
print(f"Config path: {Path.home() / '.snapfix' / 'config.toml'}")
print(f"Config exists: {(Path.home() / '.snapfix' / 'config.toml').exists()}")

try:
    config = load_config()
    print(f"Loaded Provider: {config.llm.provider}")
    print(f"Loaded Model: {config.llm.model}")
    print(f"API Key present: {bool(config.llm.api_key)}")
    
    handler = LLMHandler(config)
    print(f"Handler actual model: {handler._model}")
except Exception as e:
    print(f"Error loading config: {e}")

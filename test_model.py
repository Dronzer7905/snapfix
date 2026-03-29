import litellm
import os

# Set the API key
os.environ["GEMINI_API_KEY"] = "AIzaSyAHQkiSg3YAEFPcwVrcf2bhfSqQBRTTDFo"

# Test common model identifiers
models_to_try = [
    "gemini/gemini-1.5-flash-latest",
    "gemini/gemini-1.5-flash-v1.5",
    "gemini/gemini-pro"
]

for model in models_to_try:
    print(f"Testing {model}...")
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Hi, are you working?"}]
        )
        print(f"✅ Success with {model}!")
        print(f"Response: {response['choices'][0]['message']['content']}")
        break
    except Exception as e:
        print(f"❌ Failed with {model}: {e}")

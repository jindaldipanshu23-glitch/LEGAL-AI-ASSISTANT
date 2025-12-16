import google.generativeai as genai
import toml

# Load secret
try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["general"]["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    print("Checking available models for your API key...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Error: {e}")

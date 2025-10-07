import google.generativeai as genai
import toml
from pathlib import Path

# --- Load API Key from secrets.toml ---
try:
    # Construct the path to the secrets file
    secrets_path = Path(".streamlit/secrets.toml")
    
    # Read the secrets file
    secrets = toml.load(secrets_path)
    
    # Get the API key
    API_KEY = "GOOGLE_API_KEY"
    
except FileNotFoundError:
    print("--- ERROR ---")
    print("Could not find the secrets.toml file.")
    print("Please make sure you have created the '.streamlit/secrets.toml' file and added your API key to it.")
    exit()
except KeyError:
    print("--- ERROR ---")
    print("Your 'secrets.toml' file is missing the 'GOOGLE_API_KEY'.")
    print("Please make sure the file contains a line like: GOOGLE_API_KEY = 'your_key_here'")
    exit()

# --- Main Test Logic ---
print(" Secrets file loaded successfully.")
print("Attempting to configure the Gemini API...")

try:
    genai.configure(api_key=API_KEY)

    model_name_to_test = "gemini-2.5-flash"
    
    print(f"Configuration successful. Attempting to use model: '{model_name_to_test}'...")
    
    model = genai.GenerativeModel(model_name_to_test)
    
    prompt = "Tell me a very short, one-paragraph story about a robot discovering music."
    
    print("Model selected. Generating content...")
    
    response = model.generate_content(prompt)
    
    print("\n--- SUCCESS! ---")
    print("The API call was successful. Here is the response:")
    print(response.text)
    print("\nThis confirms your API key and environment are working correctly.")

except Exception as e:
    print("\n--- FAILED ---")
    print("An error occurred after loading the API key.")
    print("Please copy the entire error message below and share it.")
    print(f"\nDETAILED ERROR: {e}")
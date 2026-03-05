import ollama
import os
from dotenv import load_dotenv
from langsmith import traceable

# Load variables from .env
load_dotenv()

# Verify the key is loaded correctly
api_key = os.getenv("LANGSMITH_API_KEY")
if not api_key:
    print("❌ Error: LANGSMITH_API_KEY not found in .env file.")
else:
    print("✅ LangSmith API Key loaded successfully.")

# Configure LangSmith Environment
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "My-Local-Llama-Bot"

@traceable
def get_llama_response(messages):
    # This call is now 'wrapped' and will show up in your dashboard
    response = ollama.chat(model='llama3.2', messages=messages)
    return response['message']['content']

def local_chat():
    messages = [{"role": "system", "content": "You are a helpful AI."}]
    print("\n--- Llama Chat: Traceable with LangSmith ---")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']: break
        
        messages.append({"role": "user", "content": user_input})
        
        # The traceable decorator handles the logging automatically
        answer = get_llama_response(messages)
        print(f"Assistant: {answer}")
        
        messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    local_chat()
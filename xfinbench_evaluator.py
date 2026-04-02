import os
from dotenv import load_dotenv

load_dotenv()

# DEBUG: Check if the key is actually being loaded
api_key = os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGSMITH_API_KEY")
if api_key:
    print(f"✅ Key found! Starts with: {api_key[:7]}...")
else:
    print("❌ ERROR: No API key found. Check your .env file location.")






import ollama
from langsmith import Client, evaluate

# 1. Define the "Target" function (how the test calls your bot)
def predict(inputs: dict):
    # LangSmith sends the 'question' from your dataset here
    response = ollama.chat(
        model='llama3.2', 
        messages=[{"role": "user", "content": inputs["question"]}]
    )
    return {"answer": response['message']['content']}

# 2. Define a simple Evaluator (grading rule)
def exact_match(run, example):
    # Compares your bot's answer to the golden reference answer
    prediction = run.outputs.get("answer", "").strip().lower()
    reference = example.outputs.get("answer", "").strip().lower()
    return {"score": 1 if prediction == reference else 0}

# 3. Run the Experiment
client = Client()
results = evaluate(
    predict, # The function to test
    data="XFinBench-Wealth-Management", # Your dataset name #updated with finance benchmark
    evaluators=[exact_match], # The grading rules
    experiment_prefix="llama3.2-test-run"
)

print("✅ Evaluation complete! Check LangSmith to see the scores.")

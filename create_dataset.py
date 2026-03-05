from langsmith import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client()

# 1. Define your "Golden" examples
examples = [
    {
        "inputs": {"question": "What is the capital of France?"},
        "outputs": {"answer": "The capital of France is Paris."}
    },
    {
        "inputs": {"question": "How do I install a library in Python?"},
        "outputs": {"answer": "You use the command 'pip install library_name'."}
    }
]

dataset_name = "My-Local-Bot-Test-Set"

# 2. Create the dataset
if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(dataset_name=dataset_name)
    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id
    )
    print(f"✅ Dataset '{dataset_name}' created!")
else:
    print(f"ℹ️ Dataset '{dataset_name}' already exists.")
import pandas as pd
from langsmith import Client
import os
from dotenv import load_dotenv

# Load your LangSmith API keys
load_dotenv()
client = Client()

# 1. Load the XFinBench validation set
# IMPORTANT: Make sure validation_set.csv is in the same folder as this script!
try:
    df = pd.read_csv("validation_set.csv")
    print("✅ Successfully loaded validation_set.csv")
except FileNotFoundError:
    print("❌ Error: Could not find 'validation_set.csv'. Check the file path!")
    exit()

# 2. Filter for Wealth Management capabilities
# SP = Scenario Planning (Strategic Advice)
# NM = Numerical Modelling (Math/Calculations)
wealth_df = df[df['fin_capability'].isin(['SP', 'NM'])].head(15)

# 3. Format the data for LangSmith
wealth_examples = []
for _, row in wealth_df.iterrows():
    wealth_examples.append({
        "inputs": {"question": row["question"]},
        "outputs": {"answer": str(row["ground_truth"])}
    })

# 4. Upload to LangSmith
dataset_name = "XFinBench-Wealth-Management"

if not client.has_dataset(dataset_name=dataset_name):
    client.create_dataset(
        dataset_name=dataset_name, 
        description="Wealth Management subset from XFinBench (Scenario Planning & Numerical Modeling)"
    )
    client.create_examples(
        inputs=[e["inputs"] for e in wealth_examples],
        outputs=[e["outputs"] for e in wealth_examples],
        dataset_name=dataset_name
    )
    print(f"✅ Successfully uploaded {len(wealth_examples)} wealth management cases to LangSmith!")
else:
    print(f"ℹ️ Dataset '{dataset_name}' already exists in LangSmith.")
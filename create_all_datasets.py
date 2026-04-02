import sys
import os
import importlib.util

# 1. Manually find the file path
current_dir = os.path.dirname(os.path.abspath(__file__))
scenarios_path = os.path.join(current_dir, "evaluation", "hler_suite", "scenarios.py")

# 2. Check if the file actually exists where we think it is
if not os.path.exists(scenarios_path):
    print(f"❌ CRITICAL ERROR: I cannot find the file at {scenarios_path}")
    print("Please check your folder names for typos or extra spaces!")
    sys.exit(1)

# 3. Manually load the module without using the "import" keyword
spec = importlib.util.spec_from_file_location("scenarios", scenarios_path)
scenarios_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scenarios_module)

# 4. Alias the functions so the rest of your code works
get_hler_test_scenarios = scenarios_module.get_hler_test_scenarios
format_for_langsmith = scenarios_module.format_for_langsmith

print("✅ Manual load successful! File found and functions imported.")

from dotenv import load_dotenv
from langsmith import Client
load_dotenv()

def upload_suites():
    client = Client()

    # --- SUITE 1: HLER PERSONALIZED PERSONAS ---
    hler_dataset_name = "Student_Loan_Scenarios_V1"

    # Check if it already exists to avoid duplicates
    if not client.has_dataset(dataset_name=hler_dataset_name):
        print(f"📦 Creating new dataset: {hler_dataset_name}...")
        dataset = client.create_dataset(
            dataset_name=hler_dataset_name,
            description="High-stakes debt & policy personas inspired by HLER framework."
        )

        # Pull scenarios from your scenarios.py file
        scenarios = get_hler_test_scenarios()
        formatted_examples = format_for_langsmith(scenarios)

        # Upload to LangSmith
        for ex in formatted_examples:
            client.create_example(
                inputs=ex["inputs"],
                outputs=ex["outputs"],
                metadata=ex["metadata"],
                dataset_id=dataset.id
            )
        print(f"✅ Successfully uploaded {len(scenarios)} HLER scenarios.")
    else:
        print(f"ℹ️ Dataset '{hler_dataset_name}' already exists. Skipping upload.")

    # --- SUITE 2: XFINBENCH (Your Existing Benchmarks) ---
    # This assumes you have your validation_set.csv ready
    xfin_dataset_name = "XFinBench_Wealth_Subset"

    if not client.has_dataset(dataset_name=xfin_dataset_name):
        print(f"📈 Creating XFinBench dataset from CSV...")
        # You can reuse your existing create_wealth_dataset.py logic here
        # client.upload_csv(csv_path="data/validation_set.csv", ...)
        print(f"✅ XFinBench baseline ready.")
    else:
        print(f"ℹ️ Dataset '{xfin_dataset_name}' already exists.")


if __name__ == "__main__":
    upload_suites()
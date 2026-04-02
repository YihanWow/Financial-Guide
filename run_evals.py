import argparse
import os
from dotenv import load_dotenv
from langsmith import Client
from evaluation.hler_suite.reviewer import HLERCustomEvaluator  # We'll create this

# from evaluation.benchmarks.xfinbench import XFinBenchEvaluator # For your existing logic

load_dotenv()


def run_experiment(suite_type):
    client = Client()

    if suite_type == "hler":
        print(f"🚀 Starting HLER-Inspired Evaluation (Personalized Finance)...")
        dataset_name = "Student_Loan_Scenarios_V1"
        evaluators = [HLERCustomEvaluator()]
        project_prefix = "HLER-Deep-Dive"

    elif suite_type == "xfin":
        print(f"📈 Starting XFinBench Baseline Evaluation (General Wealth Mgmt)...")
        dataset_name = "XFinBench_Wealth_Subset"
        # evaluators = [XFinBenchEvaluator()]
        project_prefix = "XFinBench-Baseline"

    # This runs the actual test in LangSmith
    # It pulls the 'predict' function from your existing chatbot.py
    from core.chatbot import predict

    results = client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory=predict,
        evaluation=evaluators,
        project_name=f"{project_prefix}-{os.getenv('MODEL_NAME', 'gpt-4')}"
    )

    print(f"✅ Experiment complete. View results in LangSmith under: {project_prefix}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Financial AI Evaluation Command Center")
    parser.add_argument(
        "--suite",
        choices=["hler", "xfin"],
        required=True,
        help="Choose the evaluation suite to run."
    )
    args = parser.parse_args()
    run_experiment(args.suite)
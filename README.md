# 💰 Financial Guide

A personal finance AI chatbot powered by a local Llama 3.2 model, with a dual-layer evaluation pipeline using rule-based profiling and LLM-as-a-judge scoring — all traced and benchmarked through LangSmith.

---

## 🧠 Overview

Financial Guide helps individual users plan their finances by providing personalized advice on student loan repayment strategies, emergency fund planning, tax optimization, and wealth management. The project includes two major components:

- **Chatbot** — A locally-run conversational AI (Llama 3.2 via Ollama) with full LangSmith tracing.
- **Evaluation Pipeline** — A two-layer quality assurance system:
  - **Rule-based profiling** (`profiling.py`): Deterministic checks for math accuracy, loan coverage, and policy alignment.
  - **LLM-as-a-judge** (`reviewer.py`): A structured `HLERCustomEvaluator` that scores responses across four rubric dimensions using GPT-4-turbo.

---

## 📁 Project Structure

```
Financial-Guide/
├── core/
│   └── chatbot.py              # Main chatbot with LangSmith tracing
├── data/
│   └── validation_set.csv      # XFinBench source data (Scenario Planning & Numerical Modelling)
├── evaluation/
│   ├── __init__.py
│   ├── benchmarks/
│   │   ├── create_wealth_dataset.py    # Uploads XFinBench wealth subset to LangSmith
│   │   └── xfinbench_evaluator.py      # Runs XFinBench evaluation experiment
│   └── hler_suite/
│       ├── __init__.py
│       ├── scenarios.py        # HLER financial personas for stress-testing
│       ├── profiling.py        # Deterministic rule-based evaluators
│       └── reviewer.py         # LLM-as-a-judge evaluator (HLER rubric)
├── create_all_datasets.py      # Uploads all evaluation suites to LangSmith
└── run_evals.py                # CLI entry point to run evaluation suites
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed locally with the `llama3.2` model pulled
- A [LangSmith](https://smith.langchain.com/) account and API key

### 1. Clone the repository

```bash
git clone https://github.com/your-username/financial-guide.git
cd financial-guide
```

### 2. Install dependencies

```bash
pip install ollama langsmith langchain python-dotenv pandas pydantic
```

### 3. Pull the Llama model via Ollama

```bash
ollama pull llama3.2
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=My-Local-Llama-Bot
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

---

## 🚀 Usage

### Run the Chatbot

Start an interactive financial planning session with LangSmith tracing enabled:

```bash
python chatbot.py
```

Example session:

```
--- Llama Chat: Traceable with LangSmith ---

You: I have $42,000 in student loans. How should I prioritize repayment?
Assistant: Based on your situation, I recommend the avalanche method...

You: exit
```

All conversations are automatically traced and visible in your LangSmith dashboard under the `My-Local-Llama-Bot` project.

---

### Upload Evaluation Datasets to LangSmith

Upload both evaluation suites (HLER personas + XFinBench) in one step:

```bash
python create_all_datasets.py
```

This will create two datasets in LangSmith:

| Dataset | Description |
|---|---|
| `Student_Loan_Scenarios_V1` | 4 high-stakes HLER financial personas |
| `XFinBench_Wealth_Subset` | Wealth management cases from XFinBench CSV |

To upload only the XFinBench wealth subset:

```bash
python create_wealth_dataset.py
```

---

### Run Evaluation Suites (Recommended)

`run_evals.py` is the main CLI entry point for running evaluations. Use the `--suite` flag to choose which suite to run:

**Run the HLER personalized finance evaluation:**

```bash
python run_evals.py --suite hler
```

This runs the 4 HLER stress-test personas from `Student_Loan_Scenarios_V1` through the `HLERCustomEvaluator` and logs results to LangSmith under `HLER-Deep-Dive-<MODEL_NAME>`.

**Run the XFinBench wealth management baseline:**

```bash
python run_evals.py --suite xfin
```

This runs the wealth management benchmark from `XFinBench_Wealth_Subset` and logs results under `XFinBench-Baseline-<MODEL_NAME>`.

> The model name used in the experiment label is controlled by the `MODEL_NAME` environment variable (defaults to `gpt-4`).

### Run the Legacy XFinBench Experiment

Alternatively, you can run the standalone XFinBench evaluator directly:

```bash
python xfinbench_evaluator.py
```

Results are logged to LangSmith under the experiment prefix `llama3.2-test-run`.

---

## 🔬 Evaluation Pipeline

### Layer 1 — Rule-Based Profiling (`profiling.py`)

Deterministic checks that run on every response before the LLM judge scores it:

| Function | What It Checks |
|---|---|
| `calculate_loan_accuracy()` | Detects hallucinated loan balances and verifies interest trajectory math |
| `profile_context_coverage()` | Checks that persona-specific keywords are addressed (e.g., PSLF, avalanche, emergency fund) |
| `verify_policy_alignment()` | Validates use of 2026-specific tax/loan terminology (SECURE Act 2.0, SAVE plan) |

### Layer 2 — LLM-as-a-Judge (`reviewer.py`)

The `HLERCustomEvaluator` uses GPT-4-turbo with structured output to grade responses across four rubric dimensions:

| Dimension | Description |
|---|---|
| **Identification Credibility** | Does the advice map to the user's specific debt/income constraints? |
| **Data Quality** | Is the advice mathematically sound? |
| **Policy Relevance** | Does the advice comply with 2026 tax/loan regulations? |
| **Novelty of Strategy** | Does the agent go beyond generic advice? |

A composite `hler_comprehensive_score` (0–1) is returned to LangSmith. Responses with any dimension scoring below 3 are flagged with `needs_revision: true`.

### HLER Test Personas (`scenarios.py`)

Four stress-test personas designed to probe the chatbot's edge cases:

| Persona | Tests |
|---|---|
| The High-Debt Graduate | Avalanche repayment math ($42k, 6.8% private loan) |
| The Public Service Professional | PSLF policy — warns against overpayment to maximize forgiveness |
| The Bay Area Survivalist | Emergency fund priority over debt payoff under high cost of living |
| The 2026 Tax Optimizer | Policy currency — ensures 2026 tax bracket and SAVE plan knowledge |

---

## 🔧 Configuration

| Environment Variable | Description |
|---|---|
| `LANGSMITH_API_KEY` | Your LangSmith API key |
| `LANGSMITH_TRACING` | Set to `true` to enable tracing |
| `LANGSMITH_PROJECT` | LangSmith project name (default: `My-Local-Llama-Bot`) |
| `MODEL_NAME` | Model label used in evaluation experiment names (default: `gpt-4`) |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure any new evaluation personas are added to `scenarios.py` with a corresponding `reference_logic` entry, and that new profiling checks are covered in `profiling.py`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

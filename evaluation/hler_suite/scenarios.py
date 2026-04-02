from typing import List, Dict, Any

def get_hler_test_scenarios() -> List[Dict[str, Any]]:
    """
    Returns a list of high-stakes financial personas designed to
    stress-test the AI's empathy, policy knowledge, and math accuracy.
    """
    return [
        {
            "persona_name": "The High-Debt Graduate (Avalanche Test)",
            "user_data": {
                "balance": 42000.0,
                "income": 55000.0,
                "high_interest_rate": 0.068,
                "persona_type": "Avalanche",
                "location": "Chicago",
                "rent": 1400.0,
                "debt_details": "Loan A: $5k @ 6.8% (Private), Loan B: $37k @ 3.4% (Federal)"
            },
            "reference_logic": "Must prioritize the 6.8% private loan. Paying $500/mo should clear Loan A in ~11 months."
        },
        {
            "persona_name": "The Public Service Professional (Policy Test)",
            "user_data": {
                "balance": 80000.0,
                "income": 60000.0,
                "high_interest_rate": 0.05,
                "persona_type": "PSLF",
                "employment": "501(c)(3) Non-profit",
                "goal": "Public Service Loan Forgiveness (PSLF)"
            },
            "reference_logic": "Must warn against overpayment. Strategy should focus on lowest possible IDR payments to maximize forgiveness after 120 payments."
        },
        {
            "persona_name": "The Bay Area Survivalist (Constraint Test)",
            "user_data": {
                "balance": 42000.0,
                "income": 95000.0,
                "high_interest_rate": 0.045,
                "persona_type": "Emergency",
                "location": "San Francisco",
                "rent": 3200.0,
                "savings": 0.0
            },
            "reference_logic": "Must prioritize Emergency Fund (3-6 months) over aggressive debt payoff due to high cost of living and zero current liquidity."
        },
        {
            "persona_name": "The 2026 Tax Optimizer (Compliance Test)",
            "user_data": {
                "balance": 15000.0,
                "income": 125000.0,
                "high_interest_rate": 0.04,
                "persona_type": "General",
                "tax_status": "Single Filer",
                "year": 2026
            },
            "reference_logic": "Must reference 2026 tax bracket shifts or SAVE plan updates to ensure the advice isn't using 2024 'hallucinated' policy."
        }
    ]

# This helper converts your list into a format LangSmith expects for upload
def format_for_langsmith(scenarios):
    return [
        {
            "inputs": {"user_data": s["user_data"]},
            "outputs": {"expected_logic": s["reference_logic"]},
            "metadata": {"persona": s["persona_name"]}
        }
        for s in scenarios
    ]
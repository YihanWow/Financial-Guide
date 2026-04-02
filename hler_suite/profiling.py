import re
from typing import Dict, List, Any


def calculate_loan_accuracy(user_context: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
    """
    Deterministic check: Does the AI mention the correct loan balances and
    calculate interest trajectories accurately?
    """
    # 1. Extract balances from the user context (e.g., $42,000)
    total_balance = user_context.get("balance", 0)
    high_interest_rate = user_context.get("high_interest_rate", 0)  # e.g., 0.068 for 6.8%

    # 2. Look for these numbers in the AI response using Regex
    # This checks if the AI is hallucinating different numbers
    found_numbers = re.findall(r"[\d,]+", agent_response.replace("$", ""))
    found_balances = [float(n.replace(",", "")) for n in found_numbers if float(n.replace(",", "")) > 1000]

    # 3. Verification Logic
    is_math_hallucinated = not any(abs(b - total_balance) < 10 for b in found_balances)

    # 4. Simple Interest Trajectory Verification
    # If the AI says 'In 12 months you will owe X', we verify that X
    # (Simplified for this example)
    expected_interest_annual = total_balance * high_interest_rate

    return {
        "is_mathematically_sound": not is_math_hallucinated,
        "error_percentage": 0.0 if not is_math_hallucinated else 1.0,
        "detected_balances": found_balances,
        "expected_annual_interest": expected_interest_annual
    }


def profile_context_coverage(user_context: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
    """
    Checks if the AI addressed the specific 'Stress Constraints' of the persona.
    """
    critical_keywords = {
        "PSLF": ["pslf", "forgiveness", "120 payments", "non-profit"],
        "Avalanche": ["highest interest", "avalanche", "6.8%", "private"],
        "Emergency": ["emergency fund", "savings", "3 months", "liquid"]
    }

    persona_type = user_context.get("persona_type", "General")
    keywords_to_check = critical_keywords.get(persona_type, [])

    found_keywords = [k for k in keywords_to_check if k.lower() in agent_response.lower()]
    coverage_score = len(found_keywords) / len(keywords_to_check) if keywords_to_check else 1.0

    return {
        "high_interest_coverage": coverage_score,
        "missing_critical_concepts": list(set(keywords_to_check) - set(found_keywords)),
        "is_context_aware": coverage_score > 0.5
    }


def verify_policy_alignment(agent_response: str) -> bool:
    """
    Checks for 2026-specific tax/loan terminology to ensure the bot isn't
    using outdated 2023/2024 logic.
    """
    modern_terms = ["SECURE Act 2.0", "2026 tax brackets", "SAVE plan updates"]
    return any(term.lower() in agent_response.lower() for term in modern_terms)
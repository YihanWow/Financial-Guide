from typing import List, Optional
from pydantic import BaseModel, Field
from langsmith.evaluation import RunEvaluator, EvaluationResult
from evaluation.hler_suite.profiling import calculate_loan_accuracy, profile_context_coverage


# 1. Define the Structured Rubric
class HLERStyleEvaluation(BaseModel):
    """Structured output for the Reviewer Agent based on Dr. Zhu's HLER framework."""
    identification_credibility: int = Field(..., ge=1, le=5,
                                            description="1-5: Does the advice map to the user's specific debt/income constraints?")
    data_quality: int = Field(..., ge=1, le=5,
                              description="1-5: Is the advice mathematically sound based on provided signals?")
    policy_relevance: int = Field(..., ge=1, le=5,
                                  description="1-5: Does the advice comply with 2026 tax/loan regulations?")
    novelty_of_strategy: int = Field(..., ge=1, le=5,
                                     description="1-5: Does the agent suggest tailored optimization beyond generic advice?")
    critique: str = Field(...,
                          description="Specific reasoning for the scores, noting any hallucinations or missed constraints.")
    needs_revision: bool = Field(...,
                                 description="True if any score is below 3, indicating a failure in the logic loop.")


# 2. Define the Custom Evaluator Class
class HLERCustomEvaluator(RunEvaluator):
    def __init__(self, model_name: str = "gpt-4-turbo"):
        self.model_name = model_name

    def evaluate_run(self, run, example=None):
        # Extract inputs from the LangSmith example and outputs from the run
        user_context = example.inputs.get("user_data", {})
        agent_response = run.outputs.get("output", "")

        # STEP 1: Run Deterministic Profiling (The "Ground Truth" check)
        # These functions come from your profiling.py file
        math_signals = calculate_loan_accuracy(user_context, agent_response)
        context_signals = profile_context_coverage(user_context, agent_response)
        combined_signals = {**math_signals, **context_signals}

        # STEP 2: The LLM-as-a-Judge Prompt
        # We pass the deterministic results AS A SIGNAL to the LLM
        eval_prompt = f"""
        You are a Senior Financial Research Reviewer evaluating a Personal Finance AI.

        USER PROFILE: {user_context}
        AI ADVICE: {agent_response}

        DETERMINISTIC SIGNALS (From Python Math Engine):
        - Math Error Margin: {combined_signals.get('error_percentage')}%
        - Critical Loan Coverage: {combined_signals.get('high_interest_coverage') * 100}%
        - Missing Fields: {combined_signals.get('missing_critical_loans')}

        Based on these signals and the response text, provide a structured evaluation.
        """

        # STEP 3: Call the Evaluator LLM with Structured Output
        # (Assuming you have a helper to call your LLM with Pydantic)
        structured_llm = self._get_evaluator_llm()
        evaluation = structured_llm.invoke(eval_prompt)

        # STEP 4: Return formatted results to LangSmith
        return EvaluationResult(
            key="hler_comprehensive_score",
            score=sum([
                evaluation.identification_credibility,
                evaluation.data_quality,
                evaluation.policy_relevance
            ]) / 15,  # Normalized 0-1 score
            comment=evaluation.critique,
            evaluator_info={
                "math_verified": combined_signals.get("is_mathematically_sound"),
                "policy_score": evaluation.policy_relevance,
                "needs_revision": evaluation.needs_revision
            }
        )

    def _get_evaluator_llm(self):
        # Helper to initialize the LLM with with_structured_output(HLERStyleEvaluation)
        # This will depend on your specific LangChain setup
        pass
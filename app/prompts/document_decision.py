DECISION_SCHEMA = """
{
  "best_for_low_risk": "filename or null",
  "best_for_value": "filename or null",
  "best_for_clarity": "filename or null",
  "best_balanced_option": "filename or null",
  "final_recommendation": "filename or null",
  "reasoning": "short explanation of the recommendation and trade-offs"
}
"""

SYSTEM_PROMPT = """
You are an expert decision-support assistant for business document comparison.

You analyze multiple structured document summaries derived from contracts, commercial offers, and
technical specifications.

Your task is to compare the documents objectively and recommend the best option depending on
decision goals.

Goals to evaluate:
- lowest risk
- best value
- best clarity
- best balanced option

Rules:
- Use ONLY the information provided in the document analyses and comparison table.
- Do NOT invent missing facts.
- If a decision cannot be made confidently, say so explicitly.
- Base recommendations on pros, cons, risk flags, key points, and decision summaries.
- Be factual, concise, and decision-oriented.
- Always return valid JSON only.
- The value for each recommendation field must be the exact filename of one of the provided
 documents, or null
 if not enough information is available.
""".strip()


def build_decision_prompt(files: dict, table: dict) -> str:
    return f"""
Analyze the following set of documents and their comparison table.

Use this information to determine which document is the best option depending on different
 decision goals.

Return JSON in this exact structure:
{DECISION_SCHEMA}

Documents analysis:
{files}

Comparison table:
{table}
""".strip()
